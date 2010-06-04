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


help_message = '''
This is for accessing the Fever API (http://www.feedafever.com/api)
Currently it is only useful for retrieving Hot Items

Options:
-s, --server: specify the location of a fever installation  [required] 
-e, --email: specify the email associated with the installation [required]
-p, --password: specify the password [required]
-d, --days: specify days value [required]

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
    
    def hotItems(self):

        storyque = []

        paramString =  "&links&offset=0&range=" + str(self.getDays()) + "&page=1"
        self.setParams(paramString)

        url = str(self.getEndpoint())+str(self.getParams())

        myJson = json.load(urllib.urlopen(url,urllib.urlencode(self.getApiKey())))

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

        for item in storyque:
            print item.encode('utf8')


def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    #create a fb item
    fb = FeverBuddy("FeverBuddy")
    
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:s:e:p:d:vi", ["help", "output=","server=","email=","password=","days="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            elif option == "-i":
                hotitems = True
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
            fb.hotItems()
        
    except FeverBuddy, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
