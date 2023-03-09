import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# 2. Return the JSON representation or Precipitation analysis

@app.route("/api/v1.0/precipitation")
def precipitation():

    #Convert the query results from your precipitation analysis (i.e. retrieve only 
    # the last 12 months of data) to a dictionary using date as the key and prcp as the value.
     # Create our session (link) from Python to the DB
    session = Session(engine)


    # Calculate the date one year from the last date in data set.

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Find the most recent date in the data set.
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
    # Query:
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).\
        order_by(Measurement.date).all()

    session.close()

    # Create dictionary
    date_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        date_prcp.append(prcp_dict)
        
    return jsonify(date_prcp)


# 3. Return a JSON list of stations

@app.route("/api/v1.0/stations")
def station():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Design a query to calculate the total number stations in the dataset
    stations = session.query(Station.id, Station.station, Station.name).all()

    session.close()
    
    # Create station list

    stations_list = []
    for id, station, name in stations:
        station_dict = {}
        station_dict['id'] = station
        station_dict['station'] = id
        station_dict['name'] = name
        stations_list.appent(station_dict)


    return jsonify(stations_list)


# 4. Return a JSON list of tem

@app.route("/api/v1.0/tobs")
def tobs():

     # Create our session (link) from Python to the DB
    session = Session(engine)

    active_station = session.query(Measurement.station, func.count(Measurement.station)).\
                group_by(Measurement.station).\
                order_by((func.count(Measurement.station)).desc()).all()
    
    most_active_station = active_station[0]

    print(f"{most_active_station} is the most active station")

    # Calculate the date one year from the last date in data set.

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    station_temperature = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= query_date).\
    filter(Measurement.station == most_active_station).\
    order_by(Measurement.date).all()

    session.close()

    # Create Temp list
    temp_list = []
    for date, tobs in station_temperature:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temp"] = tobs
        temp_list.append(temp_dict)
    
    # Return JSON for most active station

    return jsonify(temp_list)


# 5. Return a JSON list of the minimum temperature, 
# the average temperature, and the maximum temperature for a specified start or start-end range.

# Specific start date
@app.route("/api/v1.0/<start>")
def start(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [Measurement.station,
       func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]
    
    start_date_temp = session.query(*sel).\
        filter(func.strftime("%Y-%D-%M", Measurement.date) >= start).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all
    

    session.close()
    

    # Make list of temperature for start date
    start_end_temp_values = []
    for min, max, avg, date in start_date_temp:
        start_end_dict = {}
        start_end_dict["Min_Temp"] = min
        start_end_dict["Max_Temp"] = max
        start_end_dict["Avg_Temp"] = avg
        start_end_dict["Date"] = date
        start_end_temp_values.append(start_end_dict)

    # Return JSON for start date
        
    return jsonify(start_end_temp_values)

# Specific start-end date

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [Measurement.station,
       func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]
    
    start_date_temp = session.query(*sel).\
        filter(func.strftime("%Y-%D-%M", Measurement.date) >= start).\
        filter(func.strftime("%Y-%D-%M", Measurement.date) <= end).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all
    
    session.close()
    

    # Make list of temperature for start date
    start_end_temp_values = []
    for min, max, avg, date in start_date_temp:
        start_end_dict = {}
        start_end_dict["Min_Temp"] = min
        start_end_dict["Max_Temp"] = max
        start_end_dict["Avg_Temp"] = avg
        start_end_dict["Date"] = date
        start_end_temp_values.append(start_end_dict)

    # Return JSON for start date
        
    return jsonify(start_end_temp_values)


#############################################################

if __name__ == '__main__':
    app.run(debug=True)




