# coding: iso-8859-1 -*-
"""
Created on Wed Oct 22 15:59:34 2014

@author: FábioPhillip
"""
from types import StringType

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
        
    def imprimirDadosDeAmigoEmComum(self, gui_python):
        from testeGuiPython import simpleapp_tk
        gui_python.AdicionarTextoParaGui('---------------')
        gui_python.AdicionarTextoParaGui("nota de compatibilidade=" + str(self.notaDeCompatibilidade))
        gui_python.AdicionarTextoParaGui('---------------')
        gui_python.AdicionarTextoParaGui('---------------')
        gui_python.AdicionarTextoParaGui("coisas(likes, amigos) em comum entre eles:")
        gui_python.AdicionarTextoParaGui("[")
        if(isinstance(self.coisasEmComum, StringType)):
            gui_python.AdicionarTextoParaGui(self.coisasEmComum)
        else:
            for elementoEmCoisasEmComum in self.coisasEmComum:
                gui_python.AdicionarTextoParaGui(str(elementoEmCoisasEmComum) + ",")
        
        gui_python.AdicionarTextoParaGui("]")
        #print self.coisasEmComum
        print '---------------'