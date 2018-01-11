##########################################################################
# Author: Danny Ly (RedKlouds)
# File Name: stocktwits.py
# Program Description: Mines the stocktwits data to store into a realtional
# database.
# Percondition:
# Postcondition:
#------------------------------------------------------------------------
# Creation Date: November 06, 2017
# Last Modified: Mon 06 Nov 2017 11:06:38 PM UTC
##########################################################################

class StockTwitsObj(dict):
    def __init__(self, stock_id=None,
    sequence_day=None,
    message_volume=None,
    bullish_percent = None,
    bearish_percent = None,
    num_watchers = None,
    price_performance = None,
    dow_performance = None,
    s_and_p_perforamnce = None,
    nasdaq_performance = None):
        super(StockTwitsObj, self).__init__()
        self['stock_id'] = stock_id #this is the primary key to the stock index
      
        self['sequence_day'] = sequence_day
        self['message_volume'] = message_volume
        self['bullish_percent'] = bullish_percent
        self['bearish_percent'] = bearish_percent
        self['num_watchers'] = num_watchers
        self['price_performance'] = price_performance
        self['dow_perforamnce'] = dow_performance
        self['s_and_p_perforamnce'] = s_and_p_performance
        self['nasdaq_perforamnce'] = nasdaq_perforamnce



