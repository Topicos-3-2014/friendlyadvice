# -*- coding: iso-8859-1 -*-
"""
Created on Wed Nov 05 15:30:39 2014

@author: fábioandrews
"""
from AfinidadeLikesEscolaELocalidades import AfinidadeLikesEscolaELocalidades 
from testeGuiPython import simpleapp_tk
import ageCompatibility
import mutualFriendsFacebook


#acha a compatibilidade entre amigos tudo junto: idade, localidade, escola... une tudo e dah uma nota para afinidade entre amigos
class AcharCompatibilidadeEntreAmigosTudoJunto:
     def __init__(self,ACCESS_TOKEN_FACEBOOK, gui_python):    
         self.achaAfinidadesLikesEscolaELocalidade = AfinidadeLikesEscolaELocalidades(ACCESS_TOKEN_FACEBOOK)
         self.todosOsAmigosDaPessoaDesteAccessToken = self.achaAfinidadesLikesEscolaELocalidade.meusAmigos         
         self.ACCESS_TOKEN_FACEBOOK = ACCESS_TOKEN_FACEBOOK
         self.gui_python = gui_python
        #acima temos um arranjo de strings com os nomes dos amigos da pessoa cujo facebook token foi fornecido         
         
     #Eu ja tenho todos os amigos da pessoa que tem o token do facebook. Agora, dado um amigo como entrada, verei quais sao os outros amigos com maior afinidade entre ele e os outros amigos   
     def calcularCompatibilidadeEntreEsseAmigoETodosOsMeusAmigos(self, amigoQueQueroAcharAmigosEmComum):
         self.amigosEAfinidadesLikes = self.achaAfinidadesLikesEscolaELocalidade.acharCompatibilidadeEntreLikesDePaginas(amigoQueQueroAcharAmigosEmComum)
         self.amigosEAfinidadesLocalidade = self.achaAfinidadesLikesEscolaELocalidade.acharCompatibilidadeEntreLocalidade(amigoQueQueroAcharAmigosEmComum)
         self.amigosEAfinidadesEscola = self.achaAfinidadesLikesEscolaELocalidade.acharCompatibilidadeEntreEscolas(amigoQueQueroAcharAmigosEmComum)
         self.amigosEAfinidadesIdade = ageCompatibility.achar_compatibilidade_por_idade(amigoQueQueroAcharAmigosEmComum,self.ACCESS_TOKEN_FACEBOOK)
         self.amigosEAfinidadesAmigosMutuos = mutualFriendsFacebook.achar_compatibilidade_por_amigos_mutuos(amigoQueQueroAcharAmigosEmComum,self.ACCESS_TOKEN_FACEBOOK)
         
         for umOutroAmigo in self.todosOsAmigosDaPessoaDesteAccessToken:
            if(umOutroAmigo != amigoQueQueroAcharAmigosEmComum):
                quantosCriteriosUmOutroAmigoCobre = 0.0 #se ele esta em um dos dicts obtidos, esse valor aumenta em 1             
                todasAsNotasSomadasDoOutroAmigo = 0.0  
                umOutroAmigoTemLikesEmComum = False #ele esta no dict de likes ou nao?
                umOutroAmigoTemLocalidadeEmComum = False
                umOutroAmigoTemEscolaEmComum = False
                umOutroAmigoTemIdadeEmComum = False
                umOutroAmigoTemAmigosMutuosEmComum = False
            
                if(umOutroAmigo in self.amigosEAfinidadesLikes.keys()):
                    umOutroAmigoTemLikesEmComum = True
                    quantosCriteriosUmOutroAmigoCobre =  quantosCriteriosUmOutroAmigoCobre + 1.0
                else:
                    quantosCriteriosUmOutroAmigoCobre =  quantosCriteriosUmOutroAmigoCobre + 1.0
                if(umOutroAmigo in self.amigosEAfinidadesLocalidade.keys()):
                    umOutroAmigoTemLocalidadeEmComum = True
                    quantosCriteriosUmOutroAmigoCobre =  quantosCriteriosUmOutroAmigoCobre + 1.0
                else:
                    quantosCriteriosUmOutroAmigoCobre =  quantosCriteriosUmOutroAmigoCobre + 1.0
                if(umOutroAmigo in self.amigosEAfinidadesEscola.keys()):
                    umOutroAmigoTemEscolaEmComum = True
                    quantosCriteriosUmOutroAmigoCobre =  quantosCriteriosUmOutroAmigoCobre + 1.0
                else:
                    quantosCriteriosUmOutroAmigoCobre =  quantosCriteriosUmOutroAmigoCobre + 1.0
                if(umOutroAmigo in self.amigosEAfinidadesIdade.keys()):
                    umOutroAmigoTemIdadeEmComum = True
                    quantosCriteriosUmOutroAmigoCobre =  quantosCriteriosUmOutroAmigoCobre + 1.0
                else:
                    quantosCriteriosUmOutroAmigoCobre =  quantosCriteriosUmOutroAmigoCobre + 1.0
                if(umOutroAmigo in self.amigosEAfinidadesAmigosMutuos.keys()):
                    umOutroAmigoTemAmigosMutuosEmComum = True
                    quantosCriteriosUmOutroAmigoCobre =  quantosCriteriosUmOutroAmigoCobre + 1.0
                else:
                    quantosCriteriosUmOutroAmigoCobre =  quantosCriteriosUmOutroAmigoCobre + 1.0
                
                self.gui_python.AdicionarTextoParaGui("!!!!!!!!!!!!!!!!!!!!!!!! NOVO AMIGO !!!!!!!!!!!!!!!!!!!")
                self.gui_python.AdicionarTextoParaGui(umOutroAmigo)         
            
                if(umOutroAmigoTemLikesEmComum == True):
                    todasAsNotasSomadasDoOutroAmigo = todasAsNotasSomadasDoOutroAmigo + self.amigosEAfinidadesLikes[umOutroAmigo].notaDeCompatibilidade
                    self.gui_python.AdicionarTextoParaGui("\\Likes em comum")
                    self.amigosEAfinidadesLikes[umOutroAmigo].imprimirDadosDeAmigoEmComum(self.gui_python)
                
                if(umOutroAmigoTemLocalidadeEmComum == True):
                    todasAsNotasSomadasDoOutroAmigo = todasAsNotasSomadasDoOutroAmigo + self.amigosEAfinidadesLocalidade[umOutroAmigo].notaDeCompatibilidade
                    self.gui_python.AdicionarTextoParaGui("\\Localidade em comum")
                    self.amigosEAfinidadesLocalidade[umOutroAmigo].imprimirDadosDeAmigoEmComum(self.gui_python)
            
                if(umOutroAmigoTemEscolaEmComum == True):
                    todasAsNotasSomadasDoOutroAmigo = todasAsNotasSomadasDoOutroAmigo + self.amigosEAfinidadesEscola[umOutroAmigo].notaDeCompatibilidade
                    self.gui_python.AdicionarTextoParaGui("\\Escolas em comum")
                    self.amigosEAfinidadesEscola[umOutroAmigo].imprimirDadosDeAmigoEmComum(self.gui_python)
            
                if(umOutroAmigoTemIdadeEmComum == True):
                    todasAsNotasSomadasDoOutroAmigo = todasAsNotasSomadasDoOutroAmigo + self.amigosEAfinidadesIdade[umOutroAmigo].notaDeCompatibilidade
                    self.gui_python.AdicionarTextoParaGui("\\Idade em comum")
                    self.amigosEAfinidadesIdade[umOutroAmigo].imprimirDadosDeAmigoEmComum(self.gui_python)
            
                if(umOutroAmigoTemAmigosMutuosEmComum == True):
                    todasAsNotasSomadasDoOutroAmigo = todasAsNotasSomadasDoOutroAmigo + self.amigosEAfinidadesAmigosMutuos[umOutroAmigo].notaDeCompatibilidade
                    self.gui_python.AdicionarTextoParaGui("\\Amigos mutuos em comum")
                    self.amigosEAfinidadesAmigosMutuos[umOutroAmigo].imprimirDadosDeAmigoEmComum(self.gui_python)
                
                self.gui_python.AdicionarTextoParaGui("\\\\\Nota Final")
                self.gui_python.AdicionarTextoParaGui(todasAsNotasSomadasDoOutroAmigo/quantosCriteriosUmOutroAmigoCobre)
            
 #OS TESTES
#achaCompatibilidade = AcharCompatibilidadeEntreAmigosTudoJunto("CAACEdEose0cBAAwXM0mXZCCXPvYdyhBoObmM3ecc0Qta3KhhDV8u5zSbjbNmZAT8beTZCPCwTghhqTPZCL67ZB3Wgf42nHkZCS5hLmlx9xu9lHGDntZBG3wA9RWGq4K95c7iZCUs4lo4FD363uL2E5MI9eszmgKseQ5HYjzadnw5C1Qa7ElXZCqYELhEhuNimx1YqctxlMzT5ZAr4VJ0LONnnE")
#nomeAmigo = "Fábio Phillip Rocha Marques"
#achaCompatibilidade.calcularCompatibilidadeEntreEsseAmigoETodosOsMeusAmigos(nomeAmigo)