# -*- coding: utf-8 -*-
"""
Created on Mon Nov 03 15:39:01 2014

@author: FábioPhillip
"""

#!/usr/bin/python
# coding: utf-8

import facebook
import urllib
import urlparse
import subprocess
import warnings

# Hide deprecation warnings. The facebook module isn't that up-to-date (facebook.GraphAPIError).
warnings.filterwarnings('ignore', category=DeprecationWarning)


# Parameters of your app and the id of the profile you want to mess with.
FACEBOOK_APP_ID     = '1492384741023161'
FACEBOOK_APP_SECRET = '83476e8740c87f9a4689a2c9da63b158'
FACEBOOK_PROFILE_ID = '1492384741023161' #mesmo de APP_ID


# Trying to get an access token. Very awkward.
oauth_args = dict(client_id     = FACEBOOK_APP_ID,
                  client_secret = FACEBOOK_APP_SECRET,
                  grant_type    = 'client_credentials')
oauth_curl_cmd = ['curl',
                  'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)]
oauth_response = subprocess.Popen(oauth_curl_cmd,
                                  stdout = subprocess.PIPE,
                                  stderr = subprocess.PIPE).communicate()[0]

try:
    oauth_access_token = urlparse.parse_qs(str(oauth_response))['access_token'][0]
    #print oauth_access_token
    token_adquirido = facebook.get_app_access_token(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)    
    print token_adquirido
    g = facebook.GraphAPI(token_adquirido)

    # Execute a few sample queries

    print '---------------'
    print 'Me'
    print '---------------'
    pp(g.get_object('me'))
    print
    print '---------------'
    print 'My Friends'
    print '---------------'
    pp(g.get_connections('me', 'friends'))
    print
    print '---------------'
    print 'Cassio'
    print '---------------'
    pp(g.get_object('100003138583807'))
    print

except KeyError:
    print('Unable to grab an access token!')
    exit()

facebook_graph = facebook.GraphAPI(oauth_access_token)


# Try to post something on the wall.
