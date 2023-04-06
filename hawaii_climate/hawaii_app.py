# 1. import Flask and dependencies
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
engine = create_engine("sqlite:///C:/Users/Trade Bridge/Desktop/Module_10 challenge/Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement

##################################################
# Flask Setup
##################################################
app = Flask(__name__)

####################################################
# 1-List all the available routes
####################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to Hawai Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/<start>/<end><br/>"

    )
#######################################################
#2-last 12 months precipitation data
#######################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query last 12 months precipitation data
    results=session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date > dt.date(2016,8,23)).\
    order_by(Measurement.date.desc()).all()
    
    session.close()

    #Convert the query results to a dictionary

    last_year_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
                
        last_year_prcp.append(prcp_dict)

        
    return jsonify(last_year_prcp)

###########################################################
#3- Return a JSON list of stations from the dataset.
############################################################

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)


    # Query all stations

    results = session.query(Measurement.station).group_by(Measurement.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)
##################################################################
#4- Most active station dates and temperatures (last one year)
##################################################################

@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)

    #Query most active station's last year's temperature
    date=dt.datetime(2016, 8, 23)
    results=session.query(Measurement.station,Measurement.date,Measurement.tobs).\
    filter(Measurement.date > date).\
    filter(Measurement.station=="USC00519281").\
    order_by(Measurement.date.desc()).all()

    session.close()

    #return to a json list
    last_year_temp=list(np.ravel(results))
    return jsonify(last_year_temp)

##############################################################################################
# 5-min temperature, avg temperature,max temperature for a specified start date(a) and start-end dates range(b).
##############################################################################################

@app.route("/api/v1.0/start")
def tempstat_a():
    session = Session(engine)

    #a-Query station and average,min,max temperatures for a start date
    sts = [Measurement.station, 
       func.avg(Measurement.tobs), 
       func.max(Measurement.tobs), 
       func.min(Measurement.tobs)]

    start_date=dt.datetime(2015, 4, 30)

    results = session.query(*sts).\
    filter(Measurement.date>=start_date).\
    group_by(Measurement.station).\
    order_by(Measurement.station).all()
    results

    session.close()

    #return a json list
    start_day_temp=list(np.ravel(results))
    return jsonify(start_day_temp)

@app.route("/api/v1.0/start/end")
def tempstat_b():
    
    session = Session(engine)

    #b-Query station and average,min,max temperatures for a start and end date

    sts = [Measurement.station, 
       func.avg(Measurement.tobs), 
       func.max(Measurement.tobs), 
       func.min(Measurement.tobs)]

    start_date=dt.datetime(2010, 1, 1)
    end_date=dt.datetime(2016, 4, 30)
    results = session.query(*sts).\
    filter(Measurement.date>=start_date).\
    filter(Measurement.date<=end_date).\
    group_by(Measurement.station).\
    order_by(Measurement.station).all()

    results
    session.close()

    #return a json list
    start_end_day_temp=list(np.ravel(results))
    return jsonify(start_end_day_temp)


if __name__ == '__main__':
    app.run(debug=True)