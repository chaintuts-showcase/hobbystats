# This file contains code that pretty-prints processed stats
#
# Author: Josh McIntyre
#

class StatPrinter:

     # Print a generic divider
     def print_divider(self):
         print("----------")

     # This function prints a summary statistic
     def print_summary_stats(self, format_string, data):
         self.print_divider()
         print(format_string.format(data))

     # This function prints stats that are in a list of key, value pairs
     def print_kv_stats(self, format_string, data):
         self.print_divider()
         for key, value in data.items():
             print(format_string.format(key, value))

