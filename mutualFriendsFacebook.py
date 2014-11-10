# coding: iso-8859-1 -*-
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

ACCESS_TOKEN = 'CAACEdEose0cBACZAtcfQFeRK0fnwtGozQXkjZCMjOeFC4Et5LTZCGjdkw6gUpZBJahfKedF9iGNu4b2Y7CbF0ZC0lmtIyhtIp9eRAO7hZCha3HQLkZCraZAXYPm6ZAEr80k5pq7hqBdcmFKzRyhZA39MRWOZCfhRplNlkYVx9An4DUagoO7ZBELz8b3ZCFxVY8G6cJLvFtTlaXpt19CF2cUKZBjXDv'


def achar_compatibilidade_por_amigos_mutuos_todos_os_amigos():
    g = facebook.GraphAPI(ACCESS_TOKEN)
    friends = [ (friend['id'], friend['name'],)
                for friend in g.get_connections('me', 'friends')['data'] ]
    for friend_name in friends:
        soh_o_nome_de_um_amigo = friend_name[1]
        print "%%%%%%%%%%%%%%%%% Meu amigo ", soh_o_nome_de_um_amigo ,"%%%%%%%%%%%%%%%%%%%%%%" 
        notas_de_compatibilidade_com_amigos =  achar_compatibilidade_por_amigos_mutuos(soh_o_nome_de_um_amigo)
        for nomes_de_amigos in notas_de_compatibilidade_com_amigos.keys():
            print "<<<<<<<<<<<<<>>>>>>>>>>>>>>>>"    
            print "<<<<<<<<<<<<<>>>>>>>>>>>>>>>>"
            print "Amigo Comparado:", nomes_de_amigos
            print "<<<<<<<<<<<<<>>>>>>>>>>>>>>>>"
            notas_de_compatibilidade_com_amigos[nomes_de_amigos].imprimirDadosDeAmigoEmComum()
            print "<<<<<<<<<<<<<>>>>>>>>>>>>>>>>"
        print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        
        
    


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
    notas_compatibilidade_com_meus_amigos = {}
    for friend_name in friends:
        soh_o_nome_de_um_amigo = friend_name[1]
        soh_o_nome_de_um_amigo_unicode = soh_o_nome_de_um_amigo.encode('utf-8')
        if(soh_o_nome_de_um_amigo_unicode != nome_do_amigo_analizado):
             amigos_mutuos_de_um_amigo = mutual_friends[soh_o_nome_de_um_amigo] #array
             #notas_compatibilidade_com_meus_amigos[soh_o_nome_de_um_amigo] = DadosDeAmigoEmComum(0, [])
             lista_amigos_em_comum = []        
             for um_amigo_do_amigo_analizado in amigos_do_amigo_analizado:
                 for um_amigo_mutuo_de_um_amigo_qualquer in amigos_mutuos_de_um_amigo:
                     if(um_amigo_do_amigo_analizado == um_amigo_mutuo_de_um_amigo_qualquer):
                         um_amigo_em_comum_utf8 = um_amigo_do_amigo_analizado.encode('utf-8')
                         lista_amigos_em_comum.append(um_amigo_em_comum_utf8)
             #achados todos os amigos em comum, vamos calcular a nota de compatibilidade por amigos mutuos
             quantos_amigos_amigo_analizado_tem = len(amigos_do_amigo_analizado)
             quantos_amigos_em_comum = len(lista_amigos_em_comum)
             notaDeCompatibilidade = (10 *   quantos_amigos_em_comum) / quantos_amigos_amigo_analizado_tem
             #e adicionar uma nova entrada no dicionário de compatibilidade do cara com meus amigos
             novaEntradaDadosDeAmigoEmComum = DadosDeAmigoEmComum(notaDeCompatibilidade, lista_amigos_em_comum)
             notas_compatibilidade_com_meus_amigos[soh_o_nome_de_um_amigo] = novaEntradaDadosDeAmigoEmComum
    
    #print mutual_friends
    return notas_compatibilidade_com_meus_amigos





print "%%%%%%%%%%%%%%%%% Meu amigo Fabio Andrews %%%%%%%%%%%%%%%%%%%%%%"    
notas_de_compatibilidade_com_amigos =  achar_compatibilidade_por_amigos_mutuos("Fábio Andrews Rocha Marques")
for nomes_de_amigos in notas_de_compatibilidade_com_amigos.keys():
    print "<<<<<<<<<<<<<>>>>>>>>>>>>>>>>"    
    print "<<<<<<<<<<<<<>>>>>>>>>>>>>>>>"
    print "Amigo Comparado:", nomes_de_amigos
    print "<<<<<<<<<<<<<>>>>>>>>>>>>>>>>"
    notas_de_compatibilidade_com_amigos[nomes_de_amigos].imprimirDadosDeAmigoEmComum()
    print "<<<<<<<<<<<<<>>>>>>>>>>>>>>>>"
