import pandas as pd
def clean_dataset(df):
    df = pd.read_csv('data/listings.csv')
    # drop columns where most of values are missing
    to_drop = [
                'listing_url', 'scrape_id', 'name', 'description', 
               'neighborhood_overview', 'picture_url',
               'host_url', 'host_name', 'host_location', 'host_about', 'host_thumbnail_url', 
               'host_verifications', 'neighbourhood', 'neighbourhood_group_cleansed',
               'bathrooms', 'calendar_updated', 'calendar_last_scraped', 
               'license', 'host_picture_url', 
               'host_neighbourhood', 'host_response_time', 'maximum_nights_avg_ntm', 
               'minimum_minimum_nights', 'minimum_maximum_nights',
               'maximum_minimum_nights', 'minimum_maximum_nights', 'maximum_maximum_nights',
               'minimum_nights_avg_ntm', 'has_availability', 'calculated_host_listings_count_shared_rooms'
               ]
    
    listings = df.drop(to_drop, axis=1)
    # Replace columns with categorical values t and f with 1 and 0
    listings = listings.replace({'f': 0, 't': 1})
    # Lambda function to remove special characters and convert to float
    strip_and_convert = lambda col: col.str.extract('(\d+)', expand=False).astype(float, errors='ignore')
    # strip_and_convert function wil be applied on the below columns
    cols_to_numeric = ['host_response_rate', 'host_acceptance_rate', 'bathrooms_text', 'price']
    listings[cols_to_numeric] = listings[cols_to_numeric].apply(strip_and_convert)
    # Rename bathrooms_text column
    listings = listings.rename(columns={'bathrooms_text': 'bathrooms'})
    listings = listings.dropna(subset=['host_since', 'host_is_superhost', 'host_listings_count', 'host_has_profile_pic', 'host_identity_verified'], axis=0)
    
    # Convert to datetime object
    listings['last_scraped'] = pd.to_datetime(listings['last_scraped'])
    listings['host_since'] = pd.to_datetime(listings['host_since'])
    
    # Calculoate the difference in days
    listings['days_host_since'] = (listings['last_scraped'] - listings['host_since']).dt.days
    
    prob = listings['property_type'].value_counts(normalize=True)
    # Setting a threshold. This threshold means that if the frequency of the property types that is less than this value, they will be categorised as Other
    threshold = 0.005
    mask = prob > threshold
    tail_prob = prob.loc[~mask].sum()
    prob = prob.loc[mask]
    prob['Other'] = tail_prob
    
    # Replace with Other if the frequency of the category is below set threshold (we set it at 0.005, refer to above) 
    listings.loc[~listings['property_type'].isin(prob.index.drop('Other')), 'property_type'] = 'Other'
    
    fill_median = lambda col: col.fillna(col.median())
    listings[['bathrooms', 'bedrooms', 'beds']] = listings[['bathrooms', 'bedrooms', 'beds']].apply(fill_median)
    
    # Convert to datetime object
    listings['first_review'] = pd.to_datetime(listings['first_review'])
    listings['last_review'] = pd.to_datetime(listings['last_review'])
    
    # Calculate number of days between review date and the date the dataset was scrapped
    listings['days_since_first_review'] = (listings['last_scraped'] - listings['first_review'])
    listings['days_since_last_review'] = (listings['last_scraped'] - listings['last_review'])
    bins = pd.to_timedelta([0, 182, 365, 730, 1460, max(listings['days_since_first_review'])], unit='days')
    labels = ['0-6 months',
               '6-12 months',
               '1-2 years',
               '2-3 years',
               '4+ years']
    def categorise_col(col_name, new_col, bins, labels):
        listings[new_col] = pd.cut(listings[col_name], bins, labels=labels)
        listings[new_col] = listings[new_col].astype('str')
        listings[new_col] = listings[new_col].str.replace('nan', 'No reviews')
        listings[new_col] = listings[new_col].astype('category')
        
    categorise_col('days_since_first_review', 'days_since_first_review_cats', bins, labels)
    bins2 = pd.to_timedelta([0, 14, 60, 182, 365, 730, max(listings['days_since_last_review'])], unit='days')
    labels2 = ['0-2 weeks', '2-8 weeks', '2-6 months', '6-12 months', '1 year', '2+ years']
    
    categorise_col('days_since_last_review', 'days_since_last_review_cats', bins=bins2, labels=labels2)
    listings['days_since_last_review_cats'].isnull().sum();
    
    # Categorising columns out of 10
    review_cols_10 = ['review_scores_accuracy',
           'review_scores_cleanliness', 'review_scores_checkin',
           'review_scores_communication', 'review_scores_location',
           'review_scores_value']
    new_cols_10 = [s + "_cats" for s in review_cols_10]
    bins3 = [0, 8, 9, 10]
    labels3 = ['0-8/10', '9/10', '10/10']
    
    for i, col in enumerate(review_cols_10):
        categorise_col(col, new_cols_10[i], bins=bins3, labels=labels3)
    
    # Categorising column out of 10
    categorise_col('review_scores_rating', 'review_scores_rating_cat', 
                   bins=[0, 80, 95, 100], 
                   labels=['0-79/100', '80-94/100', '95-100/100'])
    
    ## Dealing with outliers in prices
    listings = listings[listings['price'] < 400]
    
    import time
    import re
    
    def one_hot_encode_amenities(df):
        '''
        INPUT: 
        df - Original dataframe
        OUTPUT: 
        df_amenities - One-hot encoded dataframe of amenities
        
        Create dummies from list of amenities
        
        '''
        
        def clean_amenities(row):
            '''
            Remove special characters and split the strings
            '''
            row = re.sub('[^A-Za-z,]+', '_', row).split(",")
            return row
        
        df['amenities'] = df['amenities'].apply(clean_amenities)
        # Create columns from list of amenities
        df_amenities = df.amenities.str.join('|').str.get_dummies().add_prefix('amenity')
        # Include only those amenities that are found in >5% of the listings
        df_amenities = df_amenities[df_amenities.columns[df_amenities.sum() > 0.05 * len(df_amenities)]]
        
        return df_amenities
    
    amenities_df = one_hot_encode_amenities(listings)
    #Concatenate dataframes
    listings = pd.concat([listings, amenities_df], axis=1)
    fill_mean = lambda col: col.fillna(col.mean())
    listings[['host_response_rate', 'host_acceptance_rate', 'reviews_per_month']] = listings[['host_response_rate', 'host_acceptance_rate', 'reviews_per_month']].apply(fill_mean)
    
    return listings

