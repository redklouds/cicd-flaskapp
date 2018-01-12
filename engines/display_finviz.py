###############################################################################
# Author: Danny Ly (RedKlouds)
# File Name: display_finviz.py
# Program Description:
# Percondition:
# Postcondition:
#------------------------------------------------------------------------------
# Creation Date: January 12, 2018
# Last Modified: Fri 12 Jan 2018 08:53:07 AM UTC
###############################################################################


from finviz import FinViz

def showLeft():

    x = FinViz()
    print(x)
    return x.getTrends()
