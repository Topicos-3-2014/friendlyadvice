#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 21:58:31 2014

@author: FábioPhillip
"""

from DadosDeAmigoEmComum import DadosDeAmigoEmComum #deixar na mesma pasta
import facebook # pip install facebook-sdk
import json
import networkx as nx # pip install networkx
import requests # pip install requests

# Copy and paste in the value you just got from the inline frame into this variable and execute this cell.
# Keep in mind that you could have just gone to https://developers.facebook.com/tools/access_token/
# and retrieved the "User Token" value from the Access Token Tool

ACCESS_TOKEN = 'CAACEdEose0cBAFGip8ujPllVfirRb7khet0xGWAmhY619oVZC5YqJSfUztqcLteFQDhZCXTRMp3GuR5XyXcVwGKmbL2WiESBczLROSq6Al2lLi3RK57YYMscxZCVGpB5N7asDmSOOMVOxW33auZBjEEeTebFD78qxFHppUorx97WhmZAJxYSAiGrXjmx10gy96tpAnbXiSSPpYZByWiG8K'





def achar_compatibilidade_por_amigos_mutuos(nome_do_amigo_analizado):
    # Create a connection to the Graph API with your access token
    g = facebook.GraphAPI(ACCESS_TOKEN)
    friends = [ (friend['id'], friend['name'],)
                for friend in g.get_connections('me', 'friends')['data'] ]
    url = 'https://graph.facebook.com/me/mutualfriends/%s?access_token=%s'
    mutual_friends = {} 
    # This loop spawns a separate request for each iteration, so
    # it may take a while. Optimization with a thread pool or similar
    # technique would be possible.
    for friend_id, friend_name in friends:
        r = requests.get(url % (friend_id, ACCESS_TOKEN,) )
        response_data = json.loads(r.content)['data']
        mutual_friends[friend_name] = [ data['name'] 
                                    for data in response_data ]
    amigos_do_amigo_analizado = mutual_friends[nome_do_amigo_analizado]
    quantos_amigos_amigo_analizado_tem = len(amigos_do_amigo_analizado)
    notas_compatibilidade_com_meus_amigos = {}
    for friend_name in friends:
        soh_o_nome_de_um_amigo = friend_name[1]
        amigos_mutuos_de_um_amigo = mutual_friends[soh_o_nome_de_um_amigo] #array
        notas_compatibilidade_com_meus_amigos[soh_o_nome_de_um_amigo] = DadosDeAmigoEmComum(0, [])
    #print mutual_friends
    return notas_compatibilidade_com_meus_amigos


print achar_compatibilidade_por_amigos_mutuos("Valmiro Zuno Ribeiro")
    
