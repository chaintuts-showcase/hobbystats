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
import threading
from npimporter import np

# Create a custom Thread class for multithreading log parsing
# It's IO bound, so we can get some performance gain from processing in multiple threads
class ReadThread(threading.Thread):

    def __init__(self, func, logfile, logtype, data):

        threading.Thread.__init__(self)

        self.func = func
        self.logfile = logfile
        self.logtype = logtype
        self.data = data

    def run(self):

        self.func(self.logfile, self.logtype, self.data)

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
        threads = []
        for logfile, logtype in self.log_file_info:
                if logtype == "mileage":
                    func = self.load_mileage_log
                elif logtype == "date":
                    func = self.load_date_log
                elif logtype == "tripcount":
                    func = self.load_trip_log
                else:
                    print(f"Error, invalid log type for logfile: {logfile}, {logtype}")
                t = ReadThread(func, logfile, logtype, data)
                t.start()
                threads.append(t)

        for t in threads:
            t.join()

        return data
    
    # Helper that loads mileage type logs
    # We'll go through several converstions here
    # First, load the date string using dateutil.parser.parse - it's the most flexible parser
    # This will create a Python datetime
    # Then, convert it to a Unix timestamp for later processing by cupy/numpy
    def load_mileage_log(self, logfile, logtype, data):

        with open(logfile) as f:
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
                    print("Bad data in {}: {}".format(logfile, row))
                    print(e)

        # Convert the list to a numpy array
        dates = np.array(dates, dtype="uint32")
        mileage = np.array(mileage, dtype="float32")

        # Load the parsed data into the global data dictionary
        data[self.pretty_hobby(logfile)] = { "dates" : dates, "mileage" : mileage, "type" : logtype }

    # Helper that loads date type logs
    def load_date_log(self, logfile, logtype, data):

        with open(logfile) as f:
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

        data[self.pretty_hobby(logfile)] = { "dates" : dates, "type" : logtype }
        return dates

    # Helper that loads trip counter type logs
    def load_trip_log(self, logfile, logtype, data):

        dates = []
        with open(logfile) as f:
            dr = csv.DictReader(f)
            for row in dr: 
                # Take the second half of the season as the year if dealing with a winter season
                years = row["Years"]
                if "/" in years:
                    year = row["Years"].split("/")[1]
                else:
                    year = years
                try:
                    trips = int(row["Trips"])
                except ValueError as e:
                    print(f"Bad trip value in log {logfile}")
                try:
                    # We may have a year range in the trip log, ex 2015-2019
                    # Parse this out and evenly distribute trips into the data
                    if "-" in year:
                        year_start = int(year.split("-")[0])
                        year_end = int(year.split("-")[1])
                        years_range = list(range(year_start, year_end + 1))
                    else:
                        years_range = [year]
                    for y in years_range:
                        year_dt = dateutil.parser.parse(str(y))
                        season_dates = [ year_dt.timestamp() ] * (trips // len(years_range))
                        dates.extend(season_dates)
                except ValueError as e:
                    print("Bad year in {}: {}".format(logfile, row["Years"]))

        # Convert the list to a numpy array
        dates = np.array(dates, dtype="uint32")

        data[self.pretty_hobby(logfile)] = { "dates" : dates, "type" : logtype }

    # Determine the type of hobby log we're dealing with
    # My logs have different formats:
    # Date and mileage data
    # Date and other data (like game stats, etc.)
    # Year, location, trip count (for snowsports, park MTB)
    def detect_type(self, logfile):

        with open(logfile) as f:
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
