# This code defines classes for calculating overall date/trip statistics for multiple hobbies
# This will take data pulled from logs by the log reader and process it
#
# Author: Josh McIntyre
#
from npimporter import np
import math
import datetime

# Time delta defs for doing raw unix timestamp operations
SECONDS_IN_YEAR = 31536000

# This class defines processing methods for date/trip statistics
class TripStats:

    # Load the data on initialization
    def __init__(self, all_data):

        # Get the date data
        date_data = {}
        print(all_data)
        for hobby, data_dict in all_data.items():
            date_data[hobby] = data_dict["dates"]

        self.date_data = date_data

        # Register the functions with titles
        self.funcs = [
                        ( "Overall {}: {}", self.total_trips ),
                        ( "Overall {}: {}", self.total_years ),
                        ( "Total trips for hobby {}: {}", self.total_trips_per_hobby ),
                        ( "Total trips in {}: {}", self.total_trips_per_year ),
                        ( "Percentage active days per year {}: {}%", self.pct_active_year ),
                        ( "Percentage of total trips for {}: {}%", self.pct_hobby_total ),
                        ( "Percentage of total trips in {}: {}%", self.pct_year_total ),
                    ]

    # Define individual methods for processing each desired statistic

    # Total trips and total years
    def total_trips(self):

        # Format data - collapse all datestamps into one array
        all_raw = []
        for sport, dates in self.date_data.items():
            all_raw.extend(dates)
        all_data = np.array(all_raw, dtype="uint32")

        # Total trips - just get the size of the array
        total_trips = all_data.size

        ret = { "total trips" : total_trips}
        return ret

    # Total years
    def total_years(self):
        
        # Format data - collapse all datestamps into one array
        all_raw = []
        for sport, dates in self.date_data.items():
            all_raw.extend(dates)
        all_data = np.array(all_raw, dtype="uint32")

        # Total years - sort and subtract the latest from the oldest datestamp
        # Then, divide by seconds per year to get the total years logged
        all_data.sort()
        diff = all_data[-1] - all_data[0]
        years = int( diff / SECONDS_IN_YEAR )

        ret = { "total years" : years }
        return ret

    # Total trips per hobby
    def total_trips_per_hobby(self):

        ret = {}
        for sport, data in self.date_data.items():
            ret[sport] = data.size

        return ret

    # Total trips per year
    def total_trips_per_year(self):

        # Format data - collapse all datestamps into one array
        all_raw = []
        for sport, dates in self.date_data.items():
            all_raw.extend(dates)
        all_data = np.array(all_raw, dtype="uint32")

        # Get year from each timestamp
        year_data = [ datetime.date.fromtimestamp(date).year for date in all_data ]

        # Get the count of each year
        years, counts = np.unique(year_data, return_counts=True)
        ret = {}
        for i in range(0, len(years)):
            # Strange bug with cupy - years[i] is considered an unhashable type
            ret[int(years[i])] = counts[i]

        return ret

    # Percentage of active days per year
    def pct_active_year(self):

        year_data = self.total_trips_per_year()

        ret = {}
        for year, trips in year_data.items():
            pct = (trips / 365) * 100
            ret[year] = round(pct, 2)

        return ret


    # Percentage hobby total
    def pct_hobby_total(self):

        total_trips = self.total_trips()["total trips"]

        ret = {}
        for sport, data in self.date_data.items():
            pct = (data.size / total_trips) * 100
            ret[sport] = round(pct, 2)

        return ret

    # Percentage year total
    def pct_year_total(self):

        total_trips = self.total_trips()["total trips"]
        year_data = self.total_trips_per_year()

        ret = {}
        for year, trips in year_data.items():
            pct = (trips / total_trips) * 100
            ret[year] = round(pct, 2)

        return ret
