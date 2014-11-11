# coding: iso-8859-1 -*-
"""
Created on Wed Oct 22 15:59:34 2014

@author: FábioPhillip
"""

class DadosDeAmigoEmComum:
    def __init__(self,notaCompatibilidade, coisasEmComumDosAmigos):
        self.notaDeCompatibilidade = notaCompatibilidade
        self.coisasEmComum = coisasEmComumDosAmigos# coisasWmComum eh uma lista de tópicos, amigos etc. em comum

    def getNotaDeCompatibilidade(self):
        return self.notaDeCompatibilidade

    def setNotaDeCompatibilidade(self, novanotaDeCompatibilidade):
        self.notaDeCompatibilidade = novanotaDeCompatibilidade

    def setCoisasEmComum(self, novocoisasEmComum):
        self.coisasEmComum = novocoisasEmComum

    def getCoisasEmComum(self):
        return self.coisasEmComum
        
    def imprimirDadosDeAmigoEmComum(self):
        print '---------------'
        print "nota de compatibilidade=", self.notaDeCompatibilidade
        print '---------------'
        print '---------------'
        print "coisas(likes, amigos) em comum entre eles:"
        print "["
        for elementoEmCoisasEmComum in self.coisasEmComum:
            print elementoEmCoisasEmComum.encode(encoding='utf_8',errors='ignore'),","
        
        print "]"
        #print self.coisasEmComum
        print '---------------'