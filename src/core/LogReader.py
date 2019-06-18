# This file defines classes a class for reading hobby data from file and putting
# it into a standard format format later processing
#
# Author: Josh McIntyre
#
import csv
import os
import datetime
import dateutil.parser
import logging
from npimporter import np

# Define a generic/high level log reader class
# This class will pull in all the logs in a specified dir and pull out
# dates/years for later processing
class LogReader:

    # Initialize the hobby reader with the log directory
    def __init__(self, logdir):

        # Fetch log info for later processing
        self.logdir = logdir
        self.get_logs()

    # Get all the logs from the specified directory
    def get_logs(self):

        all_entries = os.listdir(self.logdir)
        files = [ os.path.join(self.logdir, _) for _ in all_entries if os.path.isfile(os.path.join(self.logdir, _)) ]

        log_file_info = []
        for f in files:
            log_file_info.append( ( f, self.detect_type(f) ))

        self.log_file_info = log_file_info

    # Read logs by processing each individually and loading the relevant
    # data for each log in to a dictionary of numpy lists
    # This will be a "standard format" the processor can read
    #
    # Ex:
    # {
    #   "trail_mtb" : {
    #                    "dates" : [ timestamp, timestamp2, timestamp3 ],
    #                    "mileage" : [ miles1, miles2, miles3 ],
    #                    "type" : "mileage"
    #                 }
    #   "snowsports" : {
    #                     "dates" : [ timestamp, timestamp2, timestamp3 ],
    #                     "type" : "tripcount"
    #                  }
    # }
    #
    # Specific dates will be used as possible, but for trip counter
    # only logs, we'll just use the year for every trip taken, like
    # 3 trips = 3 2019 timestamps in the list
    # We'll be using timestamps for this, and dateutil.parser uses today at midnight
    # if only the year is included. This shouldn't effect most stats.
    def read_logs(self):

        data = {}
        for logfile, logtype in self.log_file_info:

            # Get a prettier title for the hobby to use as the dict key
            pretty_hobby = self.pretty_hobby(logfile)

            # Use the appropriate helper to load the standard format data
            if logtype == "mileage":
                ret_data = self.load_mileage_log(logfile)
                data[pretty_hobby] = { "dates" : ret_data[0], "mileage" : ret_data[1], "type" : logtype } 
            elif logtype == "date":
                data[pretty_hobby] = { "dates" : self.load_date_log(logfile), "type" : logtype }
            elif logtype == "tripcount":
                data[pretty_hobby] = { "dates" : self.load_trip_log(logfile), "type" : logtype }
                
        return data

    # Helper that loads mileage type logs
    # We'll go through several converstions here
    # First, load the date string using dateutil.parser.parse - it's the most flexible parser
    # This will create a Python datetime
    # Then, convert it to a Unix timestamp for later processing by cupy/numpy
    def load_mileage_log(self, logfile):

        with open(logfile, encoding='cp1252') as f:
            dr = csv.DictReader(f)
            dates = []
            mileage = []
            for row in dr:
                try:
                    date_dt = dateutil.parser.parse(row["Date"])
                    dates.append(date_dt.timestamp())

                    miles = row["Distance (mi)"]
                    mileage.append( float(miles) )
                except ValueError as e:
                    logging.error("Bad data in {}: {}".format(logfile, row))

        # Convert the list to a numpy array
        dates = np.array(dates, dtype="uint32")
        mileage = np.array(mileage, dtype="float32")

        return (dates, mileage)

    # Helper that loads date type logs
    def load_date_log(self, logfile):

        with open(logfile, encoding='cp1252') as f:
            dr = csv.DictReader(f)
            dates = []
            for row in dr:
                try:
                    date_dt = dateutil.parser.parse(row["Date"])
                    dates.append(date_dt.timestamp())
                except ValueError as e:
                    print("Bad date in {}: {}".format(logfile, row["Date"]))

        # Convert the list to a numpy array
        dates = np.array(dates, dtype="uint32")

        return dates

    # Helper that loads trip counter type logs
    def load_trip_log(self, logfile):

        dates = []
        with open(logfile, encoding='cp1252') as f:
            dr = csv.DictReader(f)
            for row in dr: 
                # Take the first half of the season as the year if dealing with a winter season
                years = row["Years"]
                if "/" in years:
                    year = row["Years"].split("/")[1]
                else:
                    year = years
                trips = int(row["Trips"])
                try:
                    year_dt = dateutil.parser.parse(year)
                    season_dates = [ year_dt.timestamp() ] * trips
                    dates.extend(season_dates)
                except ValueError as e:
                    print("Bad year: {}".format(row["Years"]))

        # Convert the list to a numpy array
        dates = np.array(dates, dtype="uint32")

        return dates

    # Determine the type of hobby log we're dealing with
    # My logs have different formats:
    # Date and mileage data
    # Date and other data (like game stats, etc.)
    # Year, location, trip count (for snowsports, park MTB)
    def detect_type(self, logfile):

        with open(logfile, encoding='cp1252') as f:
            dr = csv.DictReader(f)
            try:
                fn = dr.fieldnames
            except Exception as e:
                print("Error determining type for log {}: ".format(logfile))
                return "unknown"

            if "Distance (mi)" in fn:
                return "mileage"
            elif "Years" in fn:
                return "tripcount"
            elif "Date" in fn:
                return "date"
            else:
                return "unknown"

    # Pretty hobby name from the file path
    def pretty_hobby(self, logfile):

        strip_path = logfile.split("/")[-1]
        strip_path = strip_path.split("\\")[-1]
        strip_ext = strip_path.replace(".csv", "")
        strip_under = strip_ext.replace("_", " ")
        title = strip_under.title()

        return title
