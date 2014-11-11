# coding: iso-8859-1 -*-
"""
Created on Mon Nov 03 11:14:35 2014

@author: FábioPhillip
"""

# Copy and paste in the value you just got from the inline frame into this variable and execute this cell.
# Keep in mind that you could have just gone to https://developers.facebook.com/tools/access_token/
# and retrieved the "User Token" value from the Access Token Tool


from DadosDeAmigoEmComum import DadosDeAmigoEmComum #deixar na mesma pasta
import facebook # pip install facebook-sdk
import json
from datetime import date
from datetime import datetime

# A helper function to pretty-print Python objects as JSON

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def pp(o): 
    print json.dumps(o, indent=1)
# Create a connection to the Graph API with your access token


# RETORNA SOH ALGUNS AMIGOS: AQUELES QUE DISSERAM SUA IDADE NO FACEBOOK
# RETORNA A NOTA ASSOCIADA E A DIFERENCA ENTRE IDADES COMO DADO EXTRA
def achar_compatibilidade_por_idade(nome_do_amigo_analizado, ACCESS_TOKEN):
    g = facebook.GraphAPI(ACCESS_TOKEN)
    friends = g.get_connections("me", "friends", fields="birthday, name")
    notas_compatibilidade_amigos_por_idade = {}    
    idades_amigos = {}
    for fr in friends['data']:
        if 'birthday' in fr:
            data_nascimento = fr['birthday']
            quantas_barras_na_data_de_nascimento = data_nascimento.count('/')
            if(quantas_barras_na_data_de_nascimento == 2):
                data_nascimento_convertido_em_date = datetime.strptime(data_nascimento, '%m/%d/%Y')
                idade_pessoa = calculate_age(data_nascimento_convertido_em_date)
                #print fr['name'] + ' ' + fr['birthday'] + ' ' + str(idade_pessoa) + ' anos'
                nome_amigo = fr['name']
                idade_amigo = idade_pessoa
                nome_amigo_utf8 = nome_amigo.encode('utf_8')
                idades_amigos[nome_amigo_utf8] = idade_amigo
    #jah sei a idade dos meus amigos. vamos agora comprar com a idade do meu amigo passado como parametro
    #isso se, eh claro, meu amigo tem idade especificada...
    if(nome_do_amigo_analizado in idades_amigos.keys()):
        idade_amigo_analizado = idades_amigos[nome_do_amigo_analizado]
        for amigo_de_idade_especificada in idades_amigos.keys():
            idade_de_amigo_qualquer = idades_amigos[amigo_de_idade_especificada]
            diferenca_entre_idades = 0
            if(idade_de_amigo_qualquer > idade_amigo_analizado):
                diferenca_entre_idades = idade_de_amigo_qualquer - idade_amigo_analizado
            else:
                diferenca_entre_idades = idade_amigo_analizado - idade_de_amigo_qualquer
            nota_de_compatibilidade = 0
            if(diferenca_entre_idades <= 5):
                nota_de_compatibilidade = 10
            elif(diferenca_entre_idades <= 10):
                nota_de_compatibilidade = 7
            elif(diferenca_entre_idades <= 15):
                nota_de_compatibilidade = 5
            elif(diferenca_entre_idades <= 20):
                nota_de_compatibilidade = 3
            else:
                nota_de_compatibilidade = 0
            texto_diferenca_entre_idades = 'Esses dois são diferentes em ' + str(diferenca_entre_idades) + ' ano(s)'
            novaEntradaDadosDeAmigoEmComum = DadosDeAmigoEmComum(nota_de_compatibilidade, texto_diferenca_entre_idades)
            notas_compatibilidade_amigos_por_idade[amigo_de_idade_especificada] = novaEntradaDadosDeAmigoEmComum
    return notas_compatibilidade_amigos_por_idade


"""print "%%%%%%%%%%%%%%%%% Meu amigo Fábio Andrews Rocha Marques %%%%%%%%%%%%%%%%%%%%%%"    
notas_de_compatibilidade_com_amigos =  achar_compatibilidade_por_idade("Fábio Phillip Rocha Marques")
for nomes_de_amigos in notas_de_compatibilidade_com_amigos.keys():
    print "<<<<<<<<<<<<<>>>>>>>>>>>>>>>>"    
    print "<<<<<<<<<<<<<>>>>>>>>>>>>>>>>"
    print "Amigo Comparado:", nomes_de_amigos
    print "<<<<<<<<<<<<<>>>>>>>>>>>>>>>>"
    notas_de_compatibilidade_com_amigos[nomes_de_amigos].imprimirDadosDeAmigoEmComum()"""

    
        
        