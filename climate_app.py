# Import Flask
from flask import Flask, jsonify

# Dependencies and Setup
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

# Database Setup
#Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect Database
Base = automap_base()
# Reflect the Tables
Base.prepare(engine, reflect=True)

# Save References to Each Table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Session (Link) From Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes

# Home Route
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Calculate the Date 1 Year Ago from the Last Data Point in the Database
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        #Retrieve the Last 12 Months of Precipitation Data Selecting Only the date and prcp Values
        precipitation_data = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all()
        # Convert List of Tuples Into a Dictionary
        precipitation_data_dic = dict(precipitation_data)
        # Return JSON Representation of Dictionary
        return jsonify(precipitation_data_dic)

# Station Route
@app.route("/api/v1.0/stations")
def stations():
        # Return list of stations from the dataset
        stations_data = session.query(Station.station, Station.name).all()
        # Convert List of Tuples Into Normal List
        station_list = list(stations_data)
        # Return JSON List of Stations from the Dataset
        return jsonify(station_list)

# TOBs Route
@app.route("/api/v1.0/tobs")
def tobs():
        # Calculate the Date 1 Year Ago from the Last Data Point in the Database
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Retrieve the Last 12 Months of date and prcp Precipitation Data
        tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all()
        # Convert List of Tuples Into List
        tobs_list = list(tobs_data)
        # Return JSON List of Temperature Observations (tobs) for the Previous Year
        return jsonify(tobs_list)

# Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_day_list = list(start_day)
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
        return jsonify(start_day_list)

# Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_end_day_list = list(start_end_day)
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
        return jsonify(start_end_day_list)

# Define Main Behavior
if __name__ == '__main__':
    app.run(debug=True)






