import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


# Flask Setup

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all the percp data"""
    # Query all Percipitation data from the previous year
    percp_data=session.query(Measurement.date, Measurement.prcp).\
                        filter(Measurement.date > '2017-08-06').all()
    # Convert list of tuples into normal list
    percp_list = list(np.ravel(percp_data))

    return jsonify(percp_list)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all the Stations names"""
    # Query all station data
    station_names= session.query(Station.station)
    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_names))

    return jsonify(station_list)



@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all the Temperature data"""
    # Query all Temperature data from the previous year
    tobs_data=session.query(Measurement.date, Measurement.tobs).\
                        filter(Measurement.date > '2017-08-06').all()
    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(tobs_data))

    return jsonify(tobs_list)


if __name__ == '__main__':
    app.run(debug=True)
