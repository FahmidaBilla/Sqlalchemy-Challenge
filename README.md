# Sqlalchemy-Challenge: Climate Data Analysis of Honolulu, Hawaii and API 

Sqlalchemy-Challenge is consisted of analysis of the climate data, which includes exploring the climate data, Precipitation Analysis, Station Analysis and creatin API SQLite connection and landing page.  

# Part 1: Analyze and Explore the Climate Data

For performing the analysis and exploring the climate data we used climate.ipynb and hawaii.sqlite provided as resources. Analysis was done by using Python and SQLAlchemy to connect to SQLite database. Measurement and Station classes were derived using SQLAlchemy automap_base() function from the tables provided. By inspecting the classes, I was able to find the details of the column names and type of each class. After exploring the date,I linked Python to the database by creating a SQLAlchemy session.

## Precipitation Analysis

Precipitation analysis is consisted of the following steps:

1. Find the most recent date in the dataset.

2. Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.

3. Select only the "date" and "prcp" values.

4. Load the query results into a Pandas DataFrame, and set the index to the "date" column.

5. Sort the DataFrame values by "date".

6. Plot the Dataframe using matplotlib.




7. Used Pandas to find summary statistics for the precipitation data, where mean = 0.177279 and std. dev = 0.461190





## Station Analysis

Station Analysis includes these following steps:

1. Design a query to calculate the total number of stations in the dataset.

2. Design a query to find the most-active stations (that is, the stations that have the most rows) by listing the stations and observation counts in descending order. Station ID USC00519281 have the greatest number of observations.

3. Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query. The most-active station id had lowest temperature : 54.0, highest temperature : 85.0  and average temperature : 71.66.

4. Design a query to get the previous 12 months of temperature observation (TOBS) data by filtering the station thaat has greates no of observations, performing query for the previous 12 months of TOBS data for that station and plotting the result as a histogram. 




5. Closing session.


# Part 2: Design Your Climate App

After the initial analysis have been completed, I designed a Flask API  based on the queries which has been saved as app.py. The steps were done as below:

1. /
    - Start at the homepage.
    - List all the available routes.

2. /api/v1.0/precipitation
    - Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date  as the key and prcp as the value.
    - Return the JSON representation of your dictionary.

3. /api/v1.0/stations
    - Return a JSON list of stations from the dataset.


4. /api/v1.0/tobs
    - Query the dates and temperature observations of the most-active station for the previous year of data.
    - Return a JSON list of temperature observations for the previous year.

5. /api/v1.0/<start> and /api/v1.0/<start>/<end>
    - Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
    - For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    - For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.














