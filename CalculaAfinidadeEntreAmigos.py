# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 21:49:24 2014

@author: fábioandrews
"""
import facebook
from DadosDeAmigoEmComum import DadosDeAmigoEmComum 

class CalculaAfinidadeEntreAmigos:
    def __init__(self,ACCESS_TOKEN_FACEBOOK):
        self.meusAmigos = []
        self.amigosECoisasQueGostam = dict()
        self.pegarMeusAmigosECoisasQueElesGostam(ACCESS_TOKEN_FACEBOOK)

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
            nota = (10 * quantasCoisasEmComumEntreMeuAmigoEAmigoParecidoComMeuAmigo) / quantasCoisasMeuAmigoGosta
            dadosDeAmigoEmComumAmigoParecido = DadosDeAmigoEmComum(nota,pessoasDeMesmoInteresseDeMeuAmigoEQuaisInteresses[amigoParecidoComMeuAmigo])
            pessoasCompativeisComMeuAmigoSegundoLikes[amigoParecidoComMeuAmigo] = dadosDeAmigoEmComumAmigoParecido
        return pessoasCompativeisComMeuAmigoSegundoLikes
#os testes...
calculaAfinidades = CalculaAfinidadeEntreAmigos('CAACEdEose0cBAAKicasZA0GxuDxbOUXVfML7nXgjU67mSRvLOE910KKcUE7mZANYDKLbno9rGuX4CpAS4BXJJk49EiRV4DjAE2YJu5SjWEwXV6ZBN0fMr0SbZCTRn7YLscfGbBjHJZAPYCSpRZCqi5BbgqhRsN7F2o908uZBr0zUl3vAuNWzhHppwbkxFZBxw9pZCCwnaLZBFBb9feIwPbrr2P')
amigosDePhillipEmComum = calculaAfinidades.acharCompatibilidadeEntreLikesDePaginas("Fábio Phillip Rocha Marques")
#faltou pegar o jeito de imprimir esse resultado de phillip
print amigosDePhillipEmComum