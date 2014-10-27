# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 21:25:41 2014

@author: FábioPhillip
"""

# Copy and paste in the value you just got from the inline frame into this variable and execute this cell.
# Keep in mind that you could have just gone to https://developers.facebook.com/tools/access_token/
# and retrieved the "User Token" value from the Access Token Tool

ACCESS_TOKEN = 'CAACEdEose0cBANIxmlZB6X3CStguIaY8nSlkAxC8izKcDaqCooOvO18QnX8zXPdaRbzmjGk0sSkunznM9bXdZAF19svnMOpZAVnimnwRphcmtgtgZAsIx0FSmJRpNhBHYJVzHFNT3XcAjxC5xJXIHKs37ZB526r5ehkrAGZCqZC0ZARiZAmCwdwR6zHFJD1DPSPbDJrnqhFe917KHw1HnffhE'

import facebook # pip install facebook-sdk
import json
import time
from datetime import date
from datetime import datetime

# A helper function to pretty-print Python objects as JSON

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

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

print
print '---------------'
print 'birthday'
print '---------------'
friends = g.get_connections("me", "friends", fields="birthday, name")
for fr in friends['data']:
    if 'birthday' in fr:
        data_nascimento = fr['birthday']
        quantas_barras_na_data_de_nascimento = data_nascimento.count('/')
        if(quantas_barras_na_data_de_nascimento == 2):
            data_nascimento_convertido_em_date = datetime.strptime(data_nascimento, '%m/%d/%Y')
            idade_pessoa = calculate_age(data_nascimento_convertido_em_date)
            print fr['name'] + ' ' + fr['birthday'] + ' ' + str(idade_pessoa) + ' anos'
            
