# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 21:25:41 2014

@author: FábioPhillip
"""

# Copy and paste in the value you just got from the inline frame into this variable and execute this cell.
# Keep in mind that you could have just gone to https://developers.facebook.com/tools/access_token/
# and retrieved the "User Token" value from the Access Token Tool

ACCESS_TOKEN = 'CAACEdEose0cBAGpVlbzUf2ZCaXFaa7v5ZAl2VQ9lYvZCu04mTB72lPfYQgvp95jcPmhnAstnH54o6qzoymvrKQrLpQ2qL0oBPzJ5dgofiWhmhqlcMZAkvX0Bt3wnZBNKolhJzwXmiWxW5pXIaKgAsJrQi3K3VEfXejFI1h3XkxSgIjX2o8RxJkyEg2RTQ5ClGE7IZB4bKLGuZBoEAYw6F1g'

import facebook # pip install facebook-sdk
import json

# A helper function to pretty-print Python objects as JSON

def pp(o): 
    print json.dumps(o, indent=1)
# Create a connection to the Graph API with your access token

g = facebook.GraphAPI(ACCESS_TOKEN)

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
print '---------------'
print 'Social Web'
print '---------------'
pp(g.request("search", {'q' : 'social web', 'type' : 'page'}))

print '----------all my friends likes------------'
friends = g.get_connections("me", "friends")['data']

likes = { friend['name'] : g.get_connections(friend['id'], "likes")['data'] 
          for friend in friends }

print likes