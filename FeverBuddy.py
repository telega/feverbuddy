#!/usr/bin/env python
# encoding: utf-8
"""
FeverBuddy.py

Created by Thomas Allen on 2010-06-04.
Copyright (c) 2010 __telega.org__. All rights reserved.
"""

import sys
import getopt
import json
import hashlib
import urllib
import time


help_message = '''
This is for accessing the Fever API (http://www.feedafever.com/api)
Currently it is only useful for retrieving Hot Items

Options:
-s, --server        : specify the location of a fever installation  [required] 
-e, --email         : specify the email associated with the installation [required]
-p, --password      : specify the password [required]
-d, --days          : specify days value
-i                  : print hot items
-r                  : print last refresh (minutes ago)

Example Usage:
python FeverBuddy.py -s mydomain.com/fever -e me@mydomain.com -p password -d 2 -i
'''


class FeverBuddy(Exception):
    def __init__(self, msg):
        self.msg = msg

    def setEndpoint(self,endpoint):
        #sets the endpoint of the fever installation ie. base directory
        self.endpoint = "http://"+endpoint+"/?api"

    def getEndpoint(self):
        return self.endpoint

    def setEmail(self,email):
        self.email = email

    def getEmail(self):
        return self.email

    def setPassword(self,password):
        self.password = password

    def getPassword(self):
        return self.password

    def setApiKey(self):
        #creates the md5 hash from the email and password for POSTing to fever. Requried for Authentication.
        self.apikey = {"api_key":hashlib.md5(str(self.getEmail())+':'+str(self.getPassword())).hexdigest()}

    def getApiKey(self):
        return self.apikey

    def setParams(self,*params):
       	self.params = ""

        for elem in params:
       	    self.params = self.params + str(elem)
    
    def getParams(self):
       	return self.params
    
    def setDays(self,days):
        self.days = days
        
    def getDays(self):
        return self.days
        
    def setUrl(self):
        self.url = str(self.getEndpoint())+str(self.getParams())
    
    def getUrl(self):
        return self.url
        
    def getJson(self):
        self.feverJson = json.load(urllib.urlopen(self.getUrl(),urllib.urlencode(self.getApiKey())))
        return self.feverJson   
    
    def getHotItems(self):
        "get Hot Items from fever, returns a list"
        storyque = []
        
        myJson = self.getJson()

        x = 0

        for links in myJson['links']:
            temperature = str(round(myJson['links'][x]['temperature'],1))
            ct = storyque.count(temperature)

            if ct > 0:
                storyque.insert((storyque.index(temperature)+2),myJson['links'][x]['title'])

            elif ct == 0:
                storyque.append(temperature)
                storyque.append('-----')
                storyque.append(myJson['links'][x]['title'])

            x=x+1
        
        return storyque
        
    
    def printHotItems(self,storyque=[]):
        "should be called in conjunction with getHotItems()"
        for item in storyque:
            print item.encode('utf8')

    
    def getLastRefresh(self):
        myJson = self.getJson()
        
        #time of last refresh
        rtime = time.localtime(int(myJson["last_refreshed_on_time"]))
        #current time
        ntime = time.localtime()
        #figure out roughly how many minutes ago
        self.lastRefresh = ((ntime[0]-rtime[0])*525948) + ((ntime[3]-rtime[3])*60) +(ntime[4]-rtime[4])
        
        return self.lastRefresh
    
    def printLastRefresh(self):
        print "Last Refresh: %d minutes ago" %self.getLastRefresh()
        

def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    
    #default values for some options
    verbose = False
    hotitems = False
    lastrefresh = False
    
    
    #create a fb item
    fb = FeverBuddy("FeverBuddy")
    
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:s:e:p:d:vir", ["help", "output=","server=","email=","password=","days="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            elif option == "-i":
                hotitems = True
            elif option == "-r":
                lastrefresh = True
            elif option in ("-h", "--help"):
                raise FeverBuddy(help_message)
            elif option in ("-o", "--output"):
                output = value 
            elif option in ("-s","--server"):
                fb.setEndpoint(value)
            elif option in ("-e","--email"):
                fb.setEmail(value)
            elif option in("-p","--password"):
                fb.setPassword(value)
            elif option in("-d","--days"):
                fb.setDays(value)
       
        #set remaining options as raw fever parameters
        fb.setParams(args)

        #take action
        fb.setApiKey()
        
        if hotitems == True:
            fb.setParams("&links&offset=0&range=",fb.getDays(),"&page=1")
            fb.setUrl()
            fb.printHotItems(fb.getHotItems())
        elif lastrefresh == True:
            fb.setParams("")
            fb.setUrl()
            fb.printLastRefresh()
        
    except FeverBuddy, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
