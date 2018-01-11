###############################################################################
# Author: Danny Ly (RedKlouds)
# File Name: stock_util.py
# Program Description:
# Percondition:
# Postcondition:
#------------------------------------------------------------------------------
# Creation Date: November 11, 2017
# Last Modified: Sat 11 Nov 2017 09:23:56 AM UTC
###############################################################################

import datetime
from datetime import timedelta

def strToDatetime(timedate):
    """ 
    Takes a datetime in the format YYYY-MM-DD HH:MM:SS
    Edited: YYYY-MM-DD
    """
    x = datetime.datetime.strptime(timedate,"%Y-%m-%d")
    return x


def makeDateDict(symbol, timestamp, days):
    """
    Returns a dictionary with each key being the timestamp
    in the format { MMDDYYYY:{
                            'day': #,
                            'neutCnt': #,
                            'bullCnt': #,
                            'bearCnt': #,
                            'symbol': sym
                            },
                    MMDDYYY: {
                            'day': #,
                            'neutCnt': #,
                            'bullCnt': #,
                            'bearCnt': #,
                            'symbol': sym
                            }
                }
    timestamp parameter expected as in format YYYY-MM-DD
    USAGE: Given the CURRENT TARGET DATE, go back N days, 
    NOT including the target date
    -> This function ONLY return a dict of N days back
    NOT including Weekends sat,sun
    --> PARAMS: timestampp: datetime Object
    --> get the neutral tweets out of the date range
    by subtracingbull and bears from total
    """
    resultDict = dict()
    day = 1
    numDays = 1
    last_day = 0
    while(len(resultDict) != days):
        #check if weekday
        day_to_check = timestamp - timedelta(days=numDays)
        if not day_to_check.weekday() >= 5:
          
            time_stamp = day_to_check.strftime("%Y-%m-%d")

            #weekday 5 is sat, 4 is friday
            #initalize the dictionary
            resultDict[time_stamp] = {'day':days-day,
                                      'totalTweets':0,
                                      'bullCnt':0,
                                      'bearCnt':0,
                                      'symbol':symbol}
            day +=1 #increment to the next day, database record
            #last_day = time_stamp #returns YYYY-MM-DD last dayi
            #return a last day datetime object
            last_day = day_to_check
        numDays +=1 #increment the counter for number of days to go back
        #and check
    return resultDict, last_day


def testMakeDictDate():
    now = datetime.datetime.strptime("2017-11-10","%Y-%m-%d")
    rDict,lastDay = makeDateDict('Danny',now, 10)
    print("Dict: %s\nLast Day: %s" % (rDict, lastDay))


if __name__ == '__main__':
    testMakeDictDate()
