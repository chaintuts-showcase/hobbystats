# This code defines classes for calculating mileage statistics for hobbies
# This will take data pulled from logs by the log reader and process it
#
# Author: Josh McIntyre
#
from npimporter import np

# Time delta defs for doing raw unix timestamp operations
SECONDS_IN_YEAR = 31536000

# This class defines processing methods for mileage statistics
class MileageStats:

    # Load the data on initialization
    def __init__(self, date_data):

        self.date_data = date_data

    # Define individual methods for processing each desired statistic

    # Total mileage and years overall
    def total_mileage(self):

        # Format data - collapse all datestamps into one array
        all_raw_mileage = []
        all_raw_dates = []
        for sport, data in self.date_data.items():
            # Only look at hobbies with mileage data
            if "mileage" in data.keys():
                all_raw_mileage.extend(data["mileage"])
                all_raw_dates.extend(data["dates"])
        all_data_mileage = np.array(all_raw_mileage, dtype="float32")
        all_data_dates = np.array(all_raw_dates, dtype="uint32")

        # Total trips - just get the size of the array
        total_mileage = all_data_mileage.sum()
        float_mileage = float(total_mileage)
        rounded_mileage = round(float_mileage, 2)

        # Total years - sort and subtract the latest from the oldest datestamp
        # Then, divide by seconds per year to get the total years logged
        all_data_dates.sort()
        diff = all_data_dates[-1] - all_data_dates[0]
        years = int( diff / SECONDS_IN_YEAR )

        ret = { "total_mileage" : rounded_mileage, "total_years" : years }
        return ret


    # Total mileage for each hobby
    def total_mileage_hobby(self):
        return self.samm_mileage_hobby("sum")

    # Average mileage for each hobby
    def avg_mileage_hobby(self):
        return self.samm_mileage_hobby("avg")

    # Maximum mileage for each hobby
    def max_mileage_hobby(self):
        return self.samm_mileage_hobby("max")

    # Minimum mileage for each hobby
    def min_mileage_hobby(self):
        return self.samm_mileage_hobby("min")

    # We can use a generic method for dealing with SAMM (Sum, Avg, Min, Max) statistics
    def samm_mileage_hobby(self, desired_stat):

        ret = {}
        for hobby, data in self.date_data.items():

            # Don't process non-mileage logs
            if data["type"] != "mileage":
                continue

            if desired_stat == "sum":
                raw_stat = data["mileage"].sum()
            elif desired_stat == "avg":
                raw_stat = np.mean(data["mileage"])
            elif desired_stat == "max":
                raw_stat = data["mileage"].max()
            elif desired_stat == "min":
                raw_stat = data["mileage"].min()
            else:
                raise Exception("Invalid desired stat: should be sum, avg, max, min")

            float_stat = float(raw_stat)
            rounded_sum = round(float_stat, 2)

            ret[hobby] = rounded_sum

        return ret

