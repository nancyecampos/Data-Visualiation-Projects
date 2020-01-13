import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd
import pprint
import matplotlib.dates as mdates
import seaborn as sns
from flask import Flask, jsonify
import numpy as np

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)
conn = engine.connect()

# Define dates to use
# Find the latest date of record
newest = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

# Date 12 months before the last date of record
oldest = dt.date(2017, 8, 23) - dt.timedelta(days=365)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"Precipitation Data: /api/v1.0/precipitation<br/>"
        f"Station Data: /api/v1.0/stations<br/>"
        f"Temperature Obersvations: /api/v1.0/tobs<br/>"
        f"Enter a start date to get a temperature min, average, and max for that date: /api/v1.0/temp/&ltstart&gt, such as, /api/v1.0/temp/2017-04-24<br/>"
        f"Enter a start and end date to get a temperature min, average, and max for those dates: /api/v1.0/temp/&ltstart&gt/&ltend&gt, such as, /api/v1.0/temp/2017-04-24/2017-04-29"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitation data"""
    date_prcp = session.query(Measurement.date, func.avg(Measurement.prcp)).filter(Measurement.date>=oldest).group_by(Measurement.date).all()

    date_prcp_dict = []
    for date, prcp in date_prcp:
        date_prcp_dict.append({str(date): prcp})
    return jsonify(date_prcp_dict)


@app.route("/api/v1.0/stations")
def stations(): 
    """Return a list of stations from the dataset."""
    # Query stations
    station_names =  session.query(Measurement.station, Station.name).group_by(Measurement.station).all()
  
    # Convert list of tuples into normal list
    stations_list = list(np.ravel(station_names))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs(): 
    # Docstring
    """Return a JSON list of tobs for the previous year."""

    results = session.query(Measurement.date, func.avg(Measurement.tobs)). \
                filter(Measurement.date>=oldest). \
                group_by(Measurement.date).all()

    tobs_dict = []
    for date, temp in results:
        tobs_dict.append({str(date): temp})
    return jsonify(tobs_dict)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def start_end(start, end=newest):

    '''
    Return the minimum temperature, the average temperature, and the max temperature for a given start or start-end range
    '''

    start_date_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    if end == newest:
        end_date_dt = end
    else:
        end_date_dt = dt.datetime.strptime(end, '%Y-%m-%d')

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    temps = session.query(*sel). \
                filter(Measurement.date>=start_date_dt). \
                filter(Measurement.date<=end_date_dt).all()[0]
    
    results_list = [{"temp_min": temps[0]}, 
                    {"temp_avg": temps[1]}, 
                    {"temp_max": temps[2]}]
    return jsonify(results_list)

if __name__ == '__main__':
    app.run(debug=True)