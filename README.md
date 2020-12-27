# Airbnb listings in London during pandemic

## Installation
To be able to visualise geographic data, you should have geopandas library installed. Here is the Installation [Guide](https://geopandas.org/install.html)

For price prediction, you need to install XGBoost library. Follow the [link](https://xgboost.readthedocs.io/en/latest/build.html) for Installation Guide

## Project Motivation
For this project, I was interestested in using InsideAirbnb data from 2020 to better understand:

1.	How popular has AirBnB become in London? And how COVID-19 impacted the demand?

2.	How the demand changed in 2020 in comparison to previous year?

3.	How the number of active listings changed in 2020?

4.	What London boroughs were rated best?

5.	What are the most expensive areas in London during pandemic?


## Files description
- **Data_cleaning_notebook.ipynb** - Provides step by step process on data cleaning, dealing with missing data and preparing the dataset for machine learning

- **EDA** - Helps answer 5 questions above

- **Data_cleaning.py** - Function on data cleaning. More concise version of *Data_cleaning_notebook.ipynb* used on Price_Prediction.ipynb file

- **Price_Prediction.ipynb** - Runs the machine learning

## Results
The main findings of this code are summarised in a [post](https://yesbol.medium.com/what-do-airbnb-listings-look-like-during-pandemic-a52a35504a84)

## Conclusions
* COVID-19 pandemic has significantly impacted both the demand in short-term rentals and active listings. Interestingly, alarming increase in number of new confirmed cases did not stop people from renting the listings. In fact, we observed that the highest number of listings was seen at the time when the number of confirmed COVID-19 positive cases was one of the highest.

*	Airbnb listings are typically scored high. We saw that all boroughs, on average, are rated higher than 90%.

*	Central areas are typically more expensive than outer London

*	Top predictors for price were found to be room type, number of bedrooms, how many people the property can accommodate and number of bathrooms

