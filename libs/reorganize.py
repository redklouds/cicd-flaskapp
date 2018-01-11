###############################################################################
# Author: Danny Ly (RedKlouds)
# File Name: reorganizeDb.py
# Program Description:
# Percondition:
# Postcondition:
#------------------------------------------------------------------------------
# Creation Date: November 11, 2017
# Last Modified: Sat 11 Nov 2017 03:13:39 AM UTC
###############################################################################

import sqlite3, datetime

conn = sqlite3.connect('./stock_data.db')
cur = conn.cursor()

data = cur.execute("SELECT * FROM StockIndexs").fetchall()

#convert the dates

for row in data:
    #for each row
    #change the date
    date = row[2]
    if not (date.find('.') == -1):
    #if a period exist we want to remove it
        d = datetime.datetime.strptime(date, "%Y-%m-%d\
        %H:%M:%S.%f").strftime("%Y-%m-%d")
    else:
        #no period exist normalk
        d = datetime.datetime.strptime(date,"%Y-%m-%d\
        %H:%M:%S").strftime("%Y-%m-%d")
    cur.execute("INSERT INTO\
    StockTargets(symbol,timestamp,actual_percent,last_price,volume,target)VALUES(?,?,?,?,?,?)",(row[1],d,row[3],row[4],row[5],row[6]))

    conn.commit()
conn.close()
