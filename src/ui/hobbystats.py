# This file defines main stat processing code
# It is the main entry point for the program
import argparse
import sys

from LogReader import LogReader
from TripStats import TripStats
from MileageStats import MileageStats
from DateStats import DateStats
from StatPrinter import StatPrinter
from StatBarGraph import graph_stats_bar

# Usage string helper
def usage(tls, ms, ds):

    # Print the stat options
    print("Available stats:\n")
    print("-----Overall Trip Stats-----")
    for i, stat in enumerate(tls.funcs):
        print(f"{i}) {stat[0]}")

    print("-----Mileage Stats-----")
    for i, stat in enumerate(ms.funcs):
        print(f"{i}) {stat[0]}")

    print("-----Date Stats-----")
    for i, stat in enumerate(ds.funcs):
        print(f"{i}) {stat[0]}")

# This function is the main entry point for the program
def main():

    # Read generic date trip data
    lr = LogReader("logs")
    date_data = lr.read_logs()

    # Initial the stat processor classes
    tls = TripStats(date_data)
    ms = MileageStats(date_data)
    ds = DateStats(date_data)

    # Define the argparser and execute desired commands
    parser = argparse.ArgumentParser()
    parser.add_argument("--stat_type", help="The stat type: trip, mileage, date", choices=["trip", "mileage", "date"])
    parser.add_argument("--stat_index", type=int, help="The statistic number to process and display")
    parser.add_argument("--stats", action="store_true", help="List available stats and indexes")
    args = parser.parse_args()

    if args.stats:
        usage(tls, ms, ds)
        sys.exit(0)
    else:
        if not args.stat_type and not args.stat_index:
            print("Stat type and index required")
            sys.exit(1)

    tp = StatPrinter()
    if args.stat_type == "trip":
        stat_proc = tls.funcs[args.stat_index]
        data = stat_proc[1]()
        tp.print_kv_stats(stat_proc[0], data)
    if args.stat_type == "mileage":
        stat_proc = ms.funcs[args.stat_index]
        data = stat_proc[1]()
        tp.print_kv_stats(stat_proc[0], data)
    if args.stat_type == "date":
        stat_proc = ds.funcs[args.stat_index]
        data = stat_proc[1]()
        tp.print_kv_stats(stat_proc[0], data)

    # TEST
    #graph_stats_bar(tth, "Total Trips per Hobby", "Hobby name", "Total trips")

if __name__ == "__main__":

    main()
