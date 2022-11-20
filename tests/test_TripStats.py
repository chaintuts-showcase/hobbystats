# This file contains unit tests for some HobbyStats functionality
#
# Author: Josh McIntyre
#
import time

from npimporter import np
import TripStats

# Set up a basic data set
DATE = 1641013200 # Timestamp for Jan 1, 2022
SECONDS_PER_DAY = 86400
TEST_DATA = {   
                "test_activity": 
                {
                    "dates" : [ DATE, DATE + SECONDS_PER_DAY, DATE + (SECONDS_PER_DAY * 2) ],
                    "type" : "date"
                },
                
                "test_activity_2": 
                {
                    "dates" : [ DATE, DATE, DATE ],
                    "type" : "tripcount"
                },
                
            }
            
# Test statistics
def test_total_trips():
    ms = TripStats.TripStats(TEST_DATA)
    ret = ms.total_trips()

    assert ret["total trips"] == 6
    
def test_total_years():
    ms = TripStats.TripStats(TEST_DATA)
    ret = ms.total_years()

    assert ret["total years"] == 1
    
