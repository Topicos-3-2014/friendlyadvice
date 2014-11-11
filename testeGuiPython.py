#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
"""
Created on Mon Nov 10 22:14:47 2014

@author: FábioPhillip
"""
import Tkinter

#TUTORIAL : http://sebsauvage.net/python/gui/
class simpleapp_tk(Tkinter.Tk):

    access_token = "CAACEdEose0cBAL0jZBheRtdGJhBnMl77MuWrlBWDZAZBDZBNVXTawH6CXKr3ZBkui0INV69sp6sPLXKpVOiN2nYZCcaHTjWRK0GWPw88n1lG7zMoEYIHUUaqvbCt7qTZC4bct4ZAaeIxgOjRmbjWIPgIsrZABAUXZBt5dsUR7HebhJah9fEBZCPh1fT7ZBoFtgrhGHmaEujsbeSUCZCfsS8ZBSo5EY"    
    # Use this as a flag to indicate if the box was clicked.    
    
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        
    

    def initialize(self):
        self.grid()
        
        self.label_campo_access_token = Tkinter.Label(self, text="Access Token:")
        self.label_campo_access_token.grid(column=0,row=0)
        
        self.label_campo_nome_amigo = Tkinter.Label(self, text="Nome do Amigo:")
        self.label_campo_nome_amigo.grid(column=0,row=1)
            
        
        self.accessTokenVariable = Tkinter.StringVar()
        self.campoAccessToken = Tkinter.Entry(self,textvariable=self.accessTokenVariable)#Entry é um nome de Textfield da tela
        self.campoAccessToken.grid(column=1,row=0,sticky='EW')#EW é pra ele grudar nas edges       
        #self.campoAccessToken.set(u"Entre com seu access token")                
        
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)#Entry é um nome de Textfield da tela
        self.entry.grid(column=1,row=1,sticky='EW')#EW é pra ele grudar nas edges
        self.entry.bind("<Return>", self.OnPressEnter)#dispara onPressEnter quando enter é pressionado no ttext field              
        
        button = Tkinter.Button(self,text=u"Ver compatibilidade!",
                                command=self.OnButtonClick,cursor="circle")#botao clicavel dispara onButtonClick
        button.grid(column=2,row=0, rowspan=2)
        self.labelVariable = Tkinter.StringVar()
        #label = Tkinter.Label(self,textvariable=self.labelVariable, # label que usa variável labelVariable como texto
                              #anchor="w",fg="white",bg="black", height=35, width=55)#NOVO WIDTH E HEIGHT FIXO
        #PESQUISAR COMO SE ADD SCROLLBAR PRA LABEL, SE TEM COMO OU ADD LABEL EM WINDOW E AIH BOTAR SCROLLBAR
        self.texto = Tkinter.Text(self, fg="white",bg="black", height=35, width=55)
        self.texto.grid(column=0,row=2,columnspan=3,sticky='EW')
        # create a Scrollbar and associate it with txt
        scrollb = Tkinter.Scrollbar(self, command=self.texto.yview)
        scrollb.grid(row=2, column=2, sticky='nsew')
        self.texto['yscrollcommand'] = scrollb.set        
        
        #label.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.labelVariable.set(u"Hello !")
        self.grid_columnconfigure(0,weight=1)#estica a coluna 1 mesmo com resize da janela
        self.resizable(True,True)#soh ppode resize horizontalmente! vertical nao pode
        self.update()
        self.geometry(self.geometry())          
        self.entry.focus_set()#textfield foca
        self.entry.selection_range(0, Tkinter.END)
        
        self.grid_columnconfigure(1, weight=1)

    
    
    
    def OnButtonClick(self):
        #self.labelVariable.set( self.labelVariable.get() + "\n" + self.entryVariable.get()+" (You clicked the button)" ) #muda o texto da labelVariable com o valor de entryVariable
        #self.texto.insert(Tkinter.END, self.entryVariable.get() + "\n")
        from AcharCompatibilidadeEntreAmigosTudoJunto import AcharCompatibilidadeEntreAmigosTudoJunto
        achaCompatibilidade = AcharCompatibilidadeEntreAmigosTudoJunto(self.accessTokenVariable.get(), self)        
        achaCompatibilidade.calcularCompatibilidadeEntreEsseAmigoETodosOsMeusAmigos(self.entryVariable.get())        
        self.entry.focus_set()#seleciona o texto todo assim que o usuário aperta botão ou enter
        self.entry.selection_range(0, Tkinter.END)        
        
    def OnPressEnter(self,event):
        #self.labelVariable.set( self.labelVariable.get() + "\n" + self.entryVariable.get()+" (You pressed ENTER)" ) #muda o texto da labelVariable com o valor de entryVariable
        #self.texto.insert(Tkinter.END, self.entryVariable.get() + "\n")
        from AcharCompatibilidadeEntreAmigosTudoJunto import AcharCompatibilidadeEntreAmigosTudoJunto
        achaCompatibilidade = AcharCompatibilidadeEntreAmigosTudoJunto(self.accessTokenVariable.get(), self)        
        achaCompatibilidade.calcularCompatibilidadeEntreEsseAmigoETodosOsMeusAmigos(self.entryVariable.get())        
        self.entry.focus_set()#seleciona o texto todo assim que o usuário aperta botão ou enter
        self.entry.selection_range(0, Tkinter.END)
    
    def AdicionarTextoParaGui(self, texto_adicionar):
        texto_add_em_string = str(texto_adicionar)
        self.texto.insert(Tkinter.END, texto_add_em_string + "\n")
        self.entry.focus_set()#seleciona o texto todo assim que o usuário aperta botão ou enter
        self.entry.selection_range(0, Tkinter.END)
    

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Friendly Advice')
    app.mainloop()    
