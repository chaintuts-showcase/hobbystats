# This file contains unit tests for some HobbyStats functionality
#
# Author: Josh McIntyre
#
import time

from npimporter import np
import MileageStats

# Set up a basic data set
now = time.time()
SECONDS_PER_DAY = 86400
TEST_DATA = {   
                "test_activity": 
                {
                    "dates" : [ now, now + SECONDS_PER_DAY, now + (SECONDS_PER_DAY * 2) ],
                    "mileage" : np.array([ 2.0, 2.0, 5.0 ], dtype="float32"),
                    "type" : "mileage"
                }
            }
            
# Test statistics
def test_total_mileage():
    ms = MileageStats.MileageStats(TEST_DATA)
    ret = ms.total_mileage()

    assert ret["total mileage"] == 9.0
    
def test_total_mileage_hobby():
    ms = MileageStats.MileageStats(TEST_DATA)
    ret = ms.total_mileage_hobby()

    assert ret["test_activity"] == 9.0

def test_avg_mileage_hobby():
    ms = MileageStats.MileageStats(TEST_DATA)
    ret = ms.avg_mileage_hobby()

    assert ret["test_activity"] == 3.0
    
def test_min_mileage():
    ms = MileageStats.MileageStats(TEST_DATA)
    ret = ms.min_mileage_hobby()

    assert ret["test_activity"] == 2.0
    
def test_max_mileage():
    ms = MileageStats.MileageStats(TEST_DATA)
    ret = ms.max_mileage_hobby()

    assert ret["test_activity"] == 5.0