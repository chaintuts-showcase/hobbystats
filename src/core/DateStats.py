# This code defines classes for calculating overall date/trip statistics for multiple hobbies
# This will take data pulled from logs by the log reader and process it
#
# Author: Josh McIntyre
#
from npimporter import np
import math
import datetime

# Time delta defs for doing raw unix timestamp operations
SECONDS_IN_DAY = 86400

# This class defines processing methods for date statistics
class DateStats:

    # Load the data on initialization
    def __init__(self, all_data):

        # Get the date data
        date_data = {}
        for hobby, data_dict in all_data.items():
            if data_dict["type"] == "date":
                date_data[hobby] = data_dict["dates"]

        self.date_data = date_data

        # Register the functions with titles
        self.funcs = [
                        ( "Overall {} : {}", self.multi_activity_days ),
                        ( "Average days between trips for {}: {}", self.average_days_between ),
                        ( "Max days between trips for {}: {}", self.max_days_between ),
                    ]

    # Define individual methods for processing each desired statistic

    # Multi-activity days
    def multi_activity_days(self):

        # Format data - collapse all datestamps into one array
        all_raw = []
        for sport, dates in self.date_data.items():
            all_raw.extend(dates)
        all_data = np.array(all_raw, dtype="uint32")

        # Find multi-activity days
        unique, counts = np.unique(all_data, return_counts=True)
        counts_multi = [ _ for _ in counts if _ > 1 and _ < 4 ]
        multi_days = len(counts_multi)

        ret = { "multi trip days" : multi_days }
        return ret

    # Average day between trips
    def average_days_between(self):

        ret = {}
        for sport, data in self.date_data.items():
            data = np.sort(data)
            diffs = np.diff(data)
            avg = np.average(diffs)
            ret[sport] = math.floor(avg / SECONDS_IN_DAY)

        return ret
        
    # Max days between trips
    def max_days_between(self):

        ret = {}
        for sport, data in self.date_data.items():
            data = np.sort(data)
            diffs = np.diff(data)
            max = np.max(diffs)
            ret[sport] = math.floor(max / SECONDS_IN_DAY)

        return ret
