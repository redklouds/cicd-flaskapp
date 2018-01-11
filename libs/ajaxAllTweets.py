###############################################################################
# Author: Danny Ly (RedKlouds)
# File Name: ajaxscrp.py
# Program Description: This program is designed to scrape all the sentiment data
# fom the domain, this is the iteration version 3 which is the most scalable
# solution yet, version 1, describes making a single selenium scrawler, which
# imitates user actions, through chromedriver, testing, this version features,
# using ajax calls for quick look up and search, aswell as faster parsing, we
# first search out StockTarget atabase for each stock, then calculate the N
# weekdays we want to record the stocktwits sentiment on, and scrap the counts
# of data, then add them into a StockTrend database using forigne keys to link
# the trend data with the target stock data 
# Percondition:
# Postcondition:
#------------------------------------------------------------------------------
# Creation Date: November 10, 2017
# Last Modified: Sat 11 Nov 2017 08:20:26 AM UTC
###############################################################################

import json, requests, re, time, datetime, sqlite3, sys, threading, queue
from bs4 import BeautifulSoup
sys.path.insert(0,'./libs')
from stockutil import makeDateDict
from progressbar import ProgressBar


class ScrapThread(threading.Thread):
    def __init__(self, threadID, name, que):
        threading.__init__(self)


class StockTweet(dict):
    def __init__(self,usr = None,sentiment = None,timestamp = None,msg = None):
        super(StockTweet, self).__init__()
        self['user'] = usr
        self['sentiment'] = sentiment
        self['timestamp'] = timestamp
        self['message'] = msg



def initParameters(sym):
    """Given the symbol, this function looks for streamID
    and First MAX parameters,
    RETURNS: a tuple with (streamID,MAXID)
    """
    base_url = 'https://stocktwits.com/symbol/%s?q=%s' %\
    (sym.upper(),sym.upper())
    req = requests.get(base_url)
    soup = BeautifulSoup(req.text,'html5lib')
    streamID = getStreamID(soup)
    lastMaxID = getFirstMax(soup)
    return streamID,lastMaxID

def getStreamID(soup):
    streamID = soup.find('ol',{'class':'stream-list'})['data-stream']
    ref = streamID[streamID.index('-')+1:]
    return ref

def getFirstMax(soup):
    loOb = soup.find('ol',{'class':'stream-list'})
    messages = loOb.find_all('li')
    last_maxID = 0
    for i in messages:
        #this method of arsing allows some random html escape characers
        #to exist namly &quot; to exist on SOME elements
        pstr = i.__str__().replace("&quot;",'"')
        find = re.findall("data-src=[(\\\')(\")](.*?)[(\\\')(\")]><",pstr)
        if len(find) == 0:
            print(pstr)
            continue
        _d = json.loads(find[0])
        usr = _d['user']['username']
        name = _d['user']['name']
        id = _d['id']
        msg = _d['body']
        last_maxID = id
        #print('\nusr:%s, name%s\nid:%s\nMessage:%s\n\n' %(usr,name,id,msg))
    return last_maxID 



def sentimentMiner():
    #########################################################################
    #initalize the db connection
    connect = sqlite3.connect('./stock_data.db')
    cur = connect.cursor()

    tweet_conn = sqlite3.connect('./tweetCollection.db')
    tweet_cur = tweet_conn.cursor()
    ##########################################################################
    #set up the url, and the header for requests
    url = \
    'https://stocktwits.com/streams/poll?stream=symbol&max=%s&stream_id=%s&substream=top&item_id=%s'
    header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36', 
            'X-Requested-With':'XMLHttpRequest'
            }
    sql = "SELECT * FROM StockTargets ORDER BY timestamp DESC;"
    #sql = "SELECT * FROM StockTargets WHERE stock_id >= 22397"
    #query by backwards so newsest days going back
    db_data = cur.execute(sql).fetchall()

    #finished using this db
    connect.close()
    ##########################################################################
    numPagesScraped = 0

    prog_bar = ProgressBar()
    for row in prog_bar(db_data):
        print('working on %s' %row[1])
        #for each row
        sym = row[1]
        #make datetime object
        date = datetime.datetime.strptime(row[2],"%Y-%m-%d")
        #set up the scraper
        
        try:
            (streamId, maxId) = initParameters(sym)
        except Exception as e:
            print("Record doesnt exsit in stocktwits\nSym: %s %s: " % (sym,e))
            continue
        print(sym,streamId)


        #initalize the counter dictionary
        #return tweetDict, and last date in YYYY-MM-DD
        (tweetD, last_date) = makeDateDict(sym,date,10)
        
        #initalize the stream-list, stocktwits
        go_to = url % (maxId,streamId, streamId)

        #print("URL %s" % go_to)
        #get the AJAX requests, which is in JSON, then convert to json obj
        stream_data = json.loads(requests.get(go_to, headers = header).text)
        #last_stream_date =\
        #stream_data['messages'][len(stream_data)-1]['created_at']
        
        print("[STATUS] %s" % stream_data['response']['status'])
        #compare two datetime objects, if the current objects last date is
        #greater than the last object out of bounds or there is not more to
        #read, then lets move onto the next symbol to scrap
        #^^^^^^^^*******************************************^^^^^^^^^^^^^^
        #do a comparison on the fly with the NEW UPDATED DATA Object form bottom
        #while loop
        #print("[TEST] Scraping %s" % sym)
        #while there is still some pages to read and our dates' have not
        #overlapped the last day we are recording, lets keep iterating
        #this iteration works by updating the 'stream-data' variable at the end
        #of each loop and reusing the object
        while (stream_data['more']):
            #check if the current datetime exist in the hash, *prevent extra
            #parsing
            #get the timedate object
            for item in stream_data['messages']:
                #scrap the 30 elements
                
                #make a datetime object to compare
                #we compare the string as the key values
                key_date = datetime.datetime.strptime(item['created_at'],'%a, %d %b %Y\
                %H:%M:%S -%f').strftime('%Y-%m-%d')
                #YYYY-MM-DD conver toi
                current_tweet_date =\
                datetime.datetime.strptime(item['created_at'], "%a, %d %b %Y\
                %H:%M:%S -%f")
                
                usr_name = item['user']['username']
                _name = item['user']['name']
                user_id = item['user']['id']
                msg_id = item['id']
                msg_timestamp = key_date
                body = item['body']
                if not item['sentiment'] is None:
                    sentiment = item['sentiment']['name']
                else:
                    sentiment = item['sentiment']
                num_likes = item['total_likes']
                num_reshares = item['total_reshares']
                ############################
                # Unlike mining for specific tweets using a data structure like
                # a hash map, we will use no such thing, we will simply insert
                # as we seek
                #################################
                tweet_cur.execute("INSERT INTO targetTweetsNotThreaded(\
                                                    st_user_name,\
                                                    st_name,\
                                                    st_user_id,\
                                                    st_msg_id,\
                                                    st_timestamp,\
                                                    st_message_body,\
                                                    st_sentiment,\
                                                    st_num_likes,\
                                                    st_num_reshared) VALUES\
                                                    (?,?,?,?,?,?,?,?,?)\
                            ",(usr_name, _name, user_id, msg_id, msg_timestamp,
                            body,sentiment, num_likes, num_reshares))
                tweet_conn.commit()
            ##############################################################
            # SECTION TO MVE THE AJAX PAGES FORWARD
            ######################################################
            #update data_strea
            #update the stream with a new AJAX CALL to REPLACE the existing
            #ajax data, this is done by giving the streamID orginated above,
            # AND THEN the maxID of the LAST post in the current panel
            last_id =\
            stream_data['messages'][len(stream_data['messages'])-1]['id']
            #make the ajax call with the new streamid LAST post id
            next_url = url % (last_id,streamId,streamId)
            stream_data = json.loads(requests.get(next_url, headers =\
            header).text)
            #numPagesScraped += len(stream_data['messages'])
            time.sleep(1)
        #now we need to update our database and insert into the db
        #TODO call executeall
            #the nuetral count, meaning the counts that does not have a bull or
            #bearish can be computed by totalTweets - (bull - bear)
    tweet_conn.close()
#main()
sentimentMiner()
