# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 21:49:24 2014

@author: fábioandrews
"""
import facebook
from DadosDeAmigoEmComum import DadosDeAmigoEmComum 

class CalculaAfinidadeEntreAmigos:
    def __init__(self,ACCESS_TOKEN_FACEBOOK):
        self.token_do_facebook = ACCESS_TOKEN_FACEBOOK
        self.meusAmigos = []
        self.amigosECoisasQueGostam = dict()
        self.amigosELocalidades = dict()
        self.pegarMeusAmigosECoisasQueElesGostam(ACCESS_TOKEN_FACEBOOK)
        self.pegarAmigosELocalidades(ACCESS_TOKEN_FACEBOOK)
        self.pegarAmigosEEscolas(ACCESS_TOKEN_FACEBOOK)

    def pegarMeusAmigosECoisasQueElesGostam(self,ACCESS_TOKEN_FACEBOOK):
        g = facebook.GraphAPI(ACCESS_TOKEN_FACEBOOK)
        meusAmigosESeusIds = g.get_connections("me", "friends")['data'] #eh um hashmap com o nome do amigo sendo a chave e o id dele como valor
        
        
        likesDeMeusAmigosComCategoriasDataECoisasInuteis = { friend['name'] : g.get_connections(friend['id'], "likes")['data'] for friend in meusAmigosESeusIds }
        #a funcao acima retorna meus amigos associados as coisas que gostam, mas nao eh apenas o nome daquilo que gostam, tem data, categoria etc
        
        chaves_de_likes = likesDeMeusAmigosComCategoriasDataECoisasInuteis.keys() #a chaves_de_likes eh um arranjo com nomes de meus amigos
        amigos_e_likes_simplificados = dict() #criarei um hashmap que simplifica meus amigos e seus likes. So preciso do nome do amigo associado a todos os likes dele

        for nomeAmigo in chaves_de_likes:
            likes_de_um_amigo = likesDeMeusAmigosComCategoriasDataECoisasInuteis[nomeAmigo]
            for umLike in likes_de_um_amigo:
                umLikeSimplificado = umLike['name']
                nomeAmigoEmUTf8 = nomeAmigo.encode("utf-8") #estava retornando u'stringqualquer' se eu nao fizesse isso. Eh um tipo diferente de string normal
                umLikeSimplificadoEmUtf8 = umLikeSimplificado.encode("utf-8")
                if(nomeAmigoEmUTf8 not in amigos_e_likes_simplificados.keys()):
                    amigos_e_likes_simplificados[nomeAmigoEmUTf8] = [umLikeSimplificadoEmUtf8]
                else:
                    amigos_e_likes_simplificados[nomeAmigoEmUTf8].append(umLikeSimplificadoEmUtf8);
                
        self.amigosECoisasQueGostam = amigos_e_likes_simplificados                
        self.meusAmigos = self.amigosECoisasQueGostam.keys()
    
    def pegarAmigosELocalidades(self,ACCESS_TOKEN_FACEBOOK):
        g = facebook.GraphAPI(ACCESS_TOKEN_FACEBOOK)
        amigosELocalizacoesComplexo = g.get_connections("me", "friends", fields="location, name")
        amigos_e_localidades = dict() #eh um dictionary que relaciona o nome de um amigo com a localidade dele       
        for fr in amigosELocalizacoesComplexo['data']:
            if 'location' in fr:
                #print fr['name'] + ' ' + fr['location']["name"] #location eh um dictionary com chaves id e name, referentes a uma localidade
                nomeAmigoUtf8 = fr['name'].encode("utf-8")  
                localidadeUtf8 = fr['location']["name"].encode("utf-8")
                amigos_e_localidades[nomeAmigoUtf8] = localidadeUtf8 #location eh um dictionary com chaves id e name, referentes a uma localidade
        self.amigosELocalidades = amigos_e_localidades

    #no final dessa funcao, eu tenho um dict tipo assim: {'Felipe Dantas Moura': ['High School%Instituto Maria Auxiliadora', 'College%Spanish Courses Colegio Delibes', 'College%Federal University of Rio Grande do Norte'],...}
    def pegarAmigosEEscolas(self,ACCESS_TOKEN_FACEBOOK):
        g = facebook.GraphAPI(ACCESS_TOKEN_FACEBOOK)
        amigosEEscolasComplexo = g.get_connections("me","friends",fields="education, name")
        amigos_e_escolas = dict() #eh um dictionary que relaciona o nome de um amigo com as escolas dele, Pode ter duas: college ou high school, por isso o valor nesse dict serah um arranjo tipo ["High School%Maria Auxilidadora","college%Federal University of Rio Grande do Norte"]               
        for fr in amigosEEscolasComplexo['data']:
            if 'education' in fr:
                nomeAmigoUtf8 = fr['name'].encode("utf-8")
                arranjoEducation = fr['education'] #uma pessoa pode ter varios high school ou college e tb pode ter graduate school
                arranjoEducacaoMeuAmigo = []                
                for elementoArranjoEducation in arranjoEducation:
                    nomeEscola = elementoArranjoEducation['school']['name'].encode("utf-8")
                    tipoEscola = elementoArranjoEducation['type'].encode("utf-8") #pode ser high school ou college ou Graduate school. College eh a faculdade
                    arranjoEducacaoMeuAmigo.append(tipoEscola + "%" + nomeEscola)
                amigos_e_escolas[nomeAmigoUtf8] = arranjoEducacaoMeuAmigo
        self.amigosEEscolas = amigos_e_escolas

    #dado um amigo, eu irei receber tipo {giovanni:DadosDeAmigoEmComum}, onde giovanni eh amigo de meuAmigo
    #e DadosDeAmigoEmComum terah a nota associada e um arranjo com os likes que giovanni tem em comum com meuAmigo
    def acharCompatibilidadeEntreLikesDePaginas(self,meuAmigo):
        pessoasDeMesmoInteresseDeMeuAmigoEQuaisInteresses = dict()
        for outroAmigo in self.amigosECoisasQueGostam.keys():
            if(outroAmigo != meuAmigo):
                #os amigos sao diferentes. Vamos ver se tem likes iguais
                likesEmComumEntreOsDois = []
                for umLikeMeuAmigo in self.amigosECoisasQueGostam[meuAmigo]:
                    for umLikeOutroAmigo in self.amigosECoisasQueGostam[outroAmigo]:
                        if(umLikeMeuAmigo == umLikeOutroAmigo):
                            #achamos um like em comum entre um Amigo e outro Amigo
                            likesEmComumEntreOsDois.append(umLikeMeuAmigo)
                if(len(likesEmComumEntreOsDois) > 0):
                # ha algo em comum entre os dois amigos e eles sao diferentes
                    pessoasDeMesmoInteresseDeMeuAmigoEQuaisInteresses[outroAmigo] = likesEmComumEntreOsDois
        
        #ate agora eu tenho tipo {giovanni:['games','musica']} giovanni eh compativel com meuAmigo
        #hora de calcular pontuacoes
        quantasCoisasMeuAmigoGosta = len(self.amigosECoisasQueGostam[meuAmigo])
        pessoasCompativeisComMeuAmigoSegundoLikes = dict() #o retorno da funcao
        for amigoParecidoComMeuAmigo in pessoasDeMesmoInteresseDeMeuAmigoEQuaisInteresses.keys():
            quantasCoisasEmComumEntreMeuAmigoEAmigoParecidoComMeuAmigo = len(pessoasDeMesmoInteresseDeMeuAmigoEQuaisInteresses[amigoParecidoComMeuAmigo])
            nota = (10.0 * quantasCoisasEmComumEntreMeuAmigoEAmigoParecidoComMeuAmigo) / quantasCoisasMeuAmigoGosta
            dadosDeAmigoEmComumAmigoParecido = DadosDeAmigoEmComum(nota,pessoasDeMesmoInteresseDeMeuAmigoEQuaisInteresses[amigoParecidoComMeuAmigo])
            pessoasCompativeisComMeuAmigoSegundoLikes[amigoParecidoComMeuAmigo] = dadosDeAmigoEmComumAmigoParecido
        return pessoasCompativeisComMeuAmigoSegundoLikes
    
    def acharCompatibilidadeEntreLocalidade(self,meuAmigo):
        #print self.amigosELocalidades
        pessoasDeMesmaLocalidadeDeMeuAmigoEQualLocalidade = dict()
        for outroAmigo in self.amigosELocalidades.keys():
            if(outroAmigo != meuAmigo):
                #os amigos sao diferentes. Vamos ver se tem mesma localidade
                if(self.amigosELocalidades[outroAmigo] == self.amigosELocalidades[meuAmigo]):
                    # ha algo em comum entre os dois amigos e eles sao diferentes
                    pessoasDeMesmaLocalidadeDeMeuAmigoEQualLocalidade[outroAmigo] = self.amigosELocalidades[outroAmigo]
        
        #ate agora eu tenho tipo {giovanni:'natal'} giovanni eh compativel com meuAmigo
        #hora de calcular pontuacoes
        pessoasCompativeisComMeuAmigoSegundoLocalidade = dict() #o retorno da funcao
        for amigoParecidoComMeuAmigo in pessoasDeMesmaLocalidadeDeMeuAmigoEQualLocalidade.keys():
            nota = 10.0 
            dadosDeAmigoEmComumAmigoParecido = DadosDeAmigoEmComum(nota,pessoasDeMesmaLocalidadeDeMeuAmigoEQualLocalidade[amigoParecidoComMeuAmigo])
            pessoasCompativeisComMeuAmigoSegundoLocalidade[amigoParecidoComMeuAmigo] = dadosDeAmigoEmComumAmigoParecido
        return pessoasCompativeisComMeuAmigoSegundoLocalidade
        
    def acharCompatibilidadeEntreEscolas(self,meuAmigo):
        pessoasDeMesmasEscolasDeMeuAmigoEQuaisEscolas = dict()
        for outroAmigo in self.amigosEEscolas.keys():
            if(outroAmigo != meuAmigo):
                #os amigos sao diferentes. Vamos ver se tem escolas iguais
                escolasEmComumEntreOsDois = []
                for umaEscolaMeuAmigo in self.amigosEEscolas[meuAmigo]:
                    for umaEscolaOutroAmigo in self.amigosEEscolas[outroAmigo]:
                        if(umaEscolaMeuAmigo == umaEscolaOutroAmigo):
                            #achamos uma escola em comum entre um Amigo e outro Amigo
                            escolasEmComumEntreOsDois.append(umaEscolaMeuAmigo)
                if(len(escolasEmComumEntreOsDois) > 0):
                # ha algo em comum entre os dois amigos e eles sao diferentes
                    pessoasDeMesmasEscolasDeMeuAmigoEQuaisEscolas[outroAmigo] = escolasEmComumEntreOsDois
        #ate agora eu tenho tipo {giovanni:['High School%Instituto Maria Auxiliadora', 'College%UFRN - Universidade Federal do Rio Grande do Norte']} giovanni eh compativel com meuAmigo
        #hora de calcular pontuacoes
        quantasEscolasMeuAmigoCursou = len(self.amigosEEscolas[meuAmigo])
        pessoasCompativeisComMeuAmigoSegundoEscolas = dict() #o retorno da funcao
        for amigoParecidoComMeuAmigo in pessoasDeMesmasEscolasDeMeuAmigoEQuaisEscolas.keys():
            quantasEscolasEmComumEntreMeuAmigoEAmigoParecidoComMeuAmigo = len(pessoasDeMesmasEscolasDeMeuAmigoEQuaisEscolas[amigoParecidoComMeuAmigo])
            nota = (10.0 * quantasEscolasEmComumEntreMeuAmigoEAmigoParecidoComMeuAmigo) / quantasEscolasMeuAmigoCursou
            dadosDeAmigoEmComumAmigoParecido = DadosDeAmigoEmComum(nota,pessoasDeMesmasEscolasDeMeuAmigoEQuaisEscolas[amigoParecidoComMeuAmigo])
            pessoasCompativeisComMeuAmigoSegundoEscolas[amigoParecidoComMeuAmigo] = dadosDeAmigoEmComumAmigoParecido
        return pessoasCompativeisComMeuAmigoSegundoEscolas
            
#os testes...
calculaAfinidades = CalculaAfinidadeEntreAmigos('CAACEdEose0cBAHsQafaZCxAMZAl4ZC9d4Un7g3hZAwrne5g2lrXT0GpjZARPW7meVEV9m7IOj5yDfLN0y2AUbKx2oQCnnrZB0lCivfLbsbHbY7LncNDntG8TjYrhiTenJBdlB8MKUaH2qDwoPc7jZAMFHLEhcW4S0oPk4TrqR6jHjW0d3ZCnZAINLa7UiiCJP6btMUY5Sg7GQPuZA9X03tu1QwBUDkKrRajLgZD')
"""amigosDePhillipEmComum = calculaAfinidades.acharCompatibilidadeEntreLikesDePaginas("Fábio Phillip Rocha Marques")
#faltou pegar o jeito de imprimir esse resultado de phillip

print "!!!!!!!!!!!!!!!amigos com mesmos likes de meu amigo Fábio Phillip!!!!!!!!!!!!!!!"
for amigoEmComum in amigosDePhillipEmComum.keys():
    print "######" , amigoEmComum
    amigosDePhillipEmComum[amigoEmComum].imprimirDadosDeAmigoEmComum();"""

"""amigosDePhillipEmComumLocalidades = calculaAfinidades.acharCompatibilidadeEntreLocalidade("Fábio Phillip Rocha Marques")
print "!!!!!!!!!!!!!!!amigos com mesma localidade de meu amigo Fábio Phillip!!!!!!!!!!!!!!!"
for amigoEmComum in amigosDePhillipEmComumLocalidades.keys():
    print "######" , amigoEmComum
    amigosDePhillipEmComumLocalidades[amigoEmComum].imprimirDadosDeAmigoEmComum();"""

print "!!!!!!!!!!!!!!!!! ESCOLAS DE FÁBIO PHILLIP !!!!!!!!!!!!!!!!!"
print calculaAfinidades.amigosEEscolas["Fábio Phillip Rocha Marques"]
amigosDePhillipEmComumEscolas = calculaAfinidades.acharCompatibilidadeEntreEscolas("Fábio Phillip Rocha Marques")
print "!!!!!!!!!!!!!!!amigos com mesmas escolas de meu amigo Fábio Phillip!!!!!!!!!!!!!!!"
for amigoEmComum in amigosDePhillipEmComumEscolas.keys():
    print "######" , amigoEmComum
    amigosDePhillipEmComumEscolas[amigoEmComum].imprimirDadosDeAmigoEmComum();