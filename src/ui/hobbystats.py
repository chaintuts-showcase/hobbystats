# This file defines main stat processing code
# It is the main entry point for the program
from LogReader import LogReader
from TripStats import TripStats
from MileageStats import MileageStats
from StatPrinter import StatPrinter

# This function is the main entry point for the program
def main():

    # Read generic date trip data
    lr = LogReader("logs")
    date_data = lr.read_logs()

    # Process overall stats
    tls = TripStats(date_data)
    tt = tls.total_trips()
    tth = tls.total_trips_per_hobby()
    tty = tls.total_trips_per_year()
    pht = tls.pct_hobby_total()
    pyt = tls.pct_year_total()

    # Process mileage stats
    ms = MileageStats(date_data)
    tm = ms.total_mileage()
    tmh = ms.total_mileage_hobby()
    amh = ms.avg_mileage_hobby()
    mxmh = ms.max_mileage_hobby()
    mnmh = ms.min_mileage_hobby()

    # Print with a pretty printer
    tp = StatPrinter()
    tp.print_summary_stats("Total trips overall: {}", tt["total_trips"])
    tp.print_summary_stats("Total years logged: {}", tt["total_years"])
    tp.print_kv_stats("Total trips for {}: {}", tth)
    tp.print_kv_stats("Total trips in {}: {}", tty)
    tp.print_kv_stats("Percentage of total trips for {}: {}%", pht)
    tp.print_kv_stats("Percentage of total trips for {}: {}%", pyt)
    tp.print_summary_stats("Total mileage overall: {}", tm["total_mileage"])
    tp.print_summary_stats("Total years logged: {}", tm["total_years"])
    tp.print_kv_stats("Total miles for {}: {}", tmh)
    tp.print_kv_stats("Average miles for {}: {}", amh)
    tp.print_kv_stats("Maximum miles for {}: {}", mxmh)
    tp.print_kv_stats("Minimum miles for {}: {}", mnmh)

if __name__ == "__main__":

    main()
