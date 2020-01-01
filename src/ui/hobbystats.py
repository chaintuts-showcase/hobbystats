# This file defines main stat processing code
# It is the main entry point for the program
from LogReader import LogReader
from TripStats import TripStats
from MileageStats import MileageStats
from DateStats import DateStats
from StatPrinter import StatPrinter
from StatBarGraph import graph_stats_bar

# This function is the main entry point for the program
def main():

    # Read generic date trip data
    lr = LogReader("logs")
    date_data = lr.read_logs()

    # Process overall stats
    tls = TripStats(date_data)
    tls_data = []
    for title, func in tls.funcs:
        tls_data.append(( title, func() ))

    # Process mileage stats
    ms = MileageStats(date_data)
    ms_data = []
    for title, func in ms.funcs:
        ms_data.append(( title, func() ))
        
    # Process date stats
    ds = DateStats(date_data)
    ds_data = []
    for title, func in ds.funcs:
        ds_data.append(( title, func() ))

    # Print with a pretty printer
    tp = StatPrinter()
    for title, data in tls_data:
        tp.print_kv_stats(title, data)
    for title, data in ms_data:
        tp.print_kv_stats(title, data)
    for title, data in ds_data:
        tp.print_kv_stats(title, data)
    
    # TEST
    #graph_stats_bar(tth, "Total Trips per Hobby", "Hobby name", "Total trips")

if __name__ == "__main__":

    main()
