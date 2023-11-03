
#C:\Users\marco\OneDrive\Documenti\Pyt>streamlit run StreamGeneraTrig.py

import streamlit as st
import streamlit.components.v1 as components

st.title("Generatore di identità goniometriche")

st.markdown("Per generare una serie di esercizi con identità goniometriche da dimostrare seleziona il numero di esercizi e la complessità, poi clicka sul tasto 'genera'. Numeri alti comportano tempi di elaborazione maggiori.")

Livello = st.slider("Quale livello di complessità?",1,10,4)
Numero = st.slider("Quanti esercizi?",1,50,5)

Bottone = st.button("Genera")

Progresso = st.progress(0)
Progresso.empty()

footer="""<style>
.reportview-container .main .block-container{
   padding-bottom:5rem;    
} 
</style>
<div style="position:fixed; bottom:0;width:100%; color: #B9B9B9; background-color: white; height:1.5rem;padding:0">
   <p style="text-align:left">© 2022 - marcodisce@gmail.com</p>
</div>
"""
if not Bottone: 
   st.markdown(footer,unsafe_allow_html=True)  

#---simpy

from sympy import *
from sympy.parsing.sympy_parser import parse_expr
x, y, z = symbols('x y z')
k, m, n = symbols('k m n', integer=True)
Si, Co, Ta = symbols('Si Co Ta', cls=Function)
init_printing(use_unicode=True)

#-- funzioni

import random
out_file = open("output.txt","w")

def arg(stringa):
  return(str(stringa[stringa.find("(")+1:stringa.find(")")]))

def funz(stringa):
  return(stringa[0:stringa.find("(")])


def fine(stringa):
  return(stringa[len(stringa)-1])

def trig(stringa):
  stringa1=stringa
  stringa1=stringa1.replace("Si","sin")
  stringa1=stringa1.replace("Co","cos")
  stringa1=stringa1.replace("Ta","tan")
  return(stringa1)

def indMin(lista):
  idx = min(range(len(lista)), key = lambda i: lista[i])
  return(idx)

def compact(stringa):
  expr=parse_expr(stringa)
  alternative=[expr,simplify(expr),factor(expr),collect(expr,Si(x)),collect(expr,Co(x)),expand(expr)]
  lunghezze=[len(str(e)) for e in alternative]
  i=indMin(lunghezze)
  return(alternative[i])

def nestedness(e,stringa):
  posizione=stringa.index(e)
  k=0
  nest=0
  while k<posizione:
    if stringa[k]=="(":
      nest+=1
    if stringa[k]==")":
      nest-=1
    k+=1
  return(nest)

def cercaElemento(stringa,nest):
  elementi=[]
  opzioni=["1"]
  opzioni.extend(["Si("+x0+")" for x0 in ["x","2*x","x/2"]])
  opzioni.extend(["Co("+x0+")" for x0 in ["x","2*x","x/2"]])
  opzioni.extend(["Co("+x0+")**2" for x0 in ["x","2*x","x/2"]])
  opzioni.extend(["Si("+x0+")**2" for x0 in ["x","2*x","x/2"]])
  opzioni.extend(["Ta("+x0+")" for x0 in ["x","2*x","x/2"]])
  opzioni.extend(["Ta("+x0+")**2" for x0 in ["x","2*x","x/2"]])
  #opzioni=["Si(x)","Co(x)", "Co(x)**2", "Si(x)**2","Ta(x)","Ta(x)**2","1"]
  for i in range(0,9):
    if "1"+str(i) in stringa:
      if "1" in opzioni:
        opzioni.remove("1")
  for e in opzioni:
    if e in stringa and nestedness(e,stringa)==nest:
      elementi.append(e)
  if elementi!=[]:
    e=random.choice(elementi)
    return(e)
  else:
    return('null')

def doppio(stringa):
  expr=parse_expr(str(stringa))
  return(str(2*expr))

def meta(stringa):
  expr=parse_expr(str(stringa))
  return(str(expr/2))

def piccolo(stringa):
  flag=False
  if len(stringa)>1:
    if stringa[1]=="/":
      flag=True
  return(flag) 


def grande(stringa):
  flag=False
  if len(stringa)>1:
    if stringa[0]=="2":
      flag=True
  return(flag) 

def espandi(stringa):
  expr=parse_expr(stringa)
  return(str(expand(expr)))

def complica(stringa1):
  stringa=espandi(stringa1)
  #stringa=stringa1
  a=cercaElemento(stringa,0)
  if a=="null":
    a=cercaElemento(stringa,1)
  output=stringa
  x0=arg(a)
  if (funz(a)=="Si" and fine(a)==")"):
    opzioni=["(Ta("+x0+")*Co("+x0+"))"]
    if not piccolo(x0):
      opzioni.extend(["(2*(Si("+meta(x0)+"))*(Co("+meta(x0)+")))","(2*(Ta("+meta(x0)+"))/(1+Ta("+meta(x0)+")**2))"])
    rimpiazzo=random.choice(opzioni)
    output=stringa.replace(a,rimpiazzo,1)
  if (funz(a)=="Co" and fine(a)==")"):
    opzioni=["(Si("+x0+")/Ta("+x0+"))"]
    if not piccolo(x0):
      extensions=["((Co("+meta(x0)+"))**2-(Si("+meta(x0)+"))**2)","(1-2*(Si("+meta(x0)+"))**2)","(2*(Co("+meta(x0)+"))**2-1)","((1-Ta("+meta(x0)+")**2)/(1+Ta("+meta(x0)+")**2))"]
      opzioni.extend([random.choice(extensions)])
      #opzioni.extend(["(Co("+meta(x0)+")**2-Si("+meta(x0)+")**2)","(1-2*Si("+meta(x0)+")**2)","(2*Co("+meta(x0)+")**2-1)"])
    rimpiazzo=random.choice(opzioni)
    output=stringa.replace(a,rimpiazzo,1)
  if (funz(a)=="Si" and fine(a)=="2"):
    opzioni=[random.choice(["(1-Co("+x0+")**2)","((Ta("+x0+")**2)*(Co("+x0+")**2))"])]#,"((Ta("+x0+")**2)/(1+Ta("+x0+")**2))"])]
    #opzioni=[random.choice(["(1-Co("+x0+")**2)","((Ta("+x0+")**2)*(Co("+x0+")**2))","((Ta("+x0+")**2)/(1+Ta("+x0+")**2))"])]
    if not grande(x0):
      opzioni.extend(["((1-Co("+doppio(x0)+"))*(1/2))"])
    rimpiazzo=random.choice(opzioni)
    output=stringa.replace(a,rimpiazzo,1)
  if (funz(a)=="Co" and fine(a)=="2"):
    opzioni=[random.choice(["(1-Si("+x0+")**2)","(1/(1+Ta("+x0+")**2))"])]
    if not grande(x0):
      opzioni.extend(["((1+Co("+doppio(x0)+"))*(1/2))"])
    rimpiazzo=random.choice(opzioni)
    output=stringa.replace(a,rimpiazzo,1)
  if (funz(a)=="Ta" and fine(a)==")"):
    opzioni=["(Si("+x0+")/Co("+x0+"))"]
    if not grande(x0):
      opzioni.extend(["(Si("+doppio(x0)+")/(Co("+doppio(x0)+")+1))","((1-Co("+doppio(x0)+"))/(Si("+doppio(x0)+")))"])
    if not piccolo(x0):
      opzioni.extend(["((2*Ta("+meta(x0)+")/(1-Ta("+meta(x0)+")**2)))"])
    rimpiazzo=random.choice(opzioni)
    output=stringa.replace(a,rimpiazzo,1)
  if (funz(a)=="Ta" and fine(a)=="2"):
    opzioni=["((Si("+x0+")**2)/(Co("+x0+")**2))"]
    if not grande(x0):
      opzioni.extend(["((1-Co("+doppio(x0)+"))/(1+Co("+doppio(x0)+")))"])
    rimpiazzo=random.choice(opzioni)
    output=stringa.replace(a,rimpiazzo,1)
  if a=="1":
    opzioni=["(Co(2*x)+2*(Si(x)**2))","(Si(x)**2+Co(x)**2)"]
    rimpiazzo=random.choice(opzioni)
    output=stringa.replace("1",rimpiazzo,1)
  output=str(compact(output))
  return(output)

def convertiWolf(stringa1):
  stringa=stringa1
  stringa=stringa.replace("**","^")
  stringa=stringa.replace("x)","x]")
  stringa=stringa.replace("x/2)","x/2]")
  stringa=stringa.replace("sin(","Sin[")
  stringa=stringa.replace("cos(","Cos[")
  stringa=stringa.replace("tan(","Tan[")
  stringa=stringa.replace("Si(","Sin[")
  stringa=stringa.replace("Co(","Cos[")
  stringa=stringa.replace("Ta(","Tan[")
  return(stringa)

def accorciaDim(lista):
  N=len(lista)
  k0=lista.index("1",0,len(lista))
  for k in range(k0+1,N):
    lista.pop()
  k=0
  while k<len(lista)-1:
    h=k+1
    while h<len(lista):
      if lista[k]==lista[h]:
      #if lista[k]==lista[h] or compact(lista[k]+"-"+lista[k])==0:
      #if latex(parse_expr(trig(lista[k])))==latex(parse_expr(trig(lista[h]))):
        #print(lista[k]==lista[h],lista[k]+"\n"+lista[h]+"\n--\n")
        lista1=lista[0:k]
        lista2=lista[h:N]
        lista=lista1+lista2
      h+=1
    k+=1
  return(lista)
      

#--funzione generatrice

def generaListaEsercizi(n,l):
    listaEsercizi=[]
    listaSoluzioni=[]
    while(len(listaEsercizi)<n):
        a="1"
        soluzione=["1"]
        trovato=False
        while trovato==False: #180
          a=complica(a)
          #print(len(str(a)))
          incrementino=(len(str(a))/(20+15*l))*100/n
          Progresso.progress(min(100,int(100*len(listaEsercizi)/n+incrementino)))
          soluzione.append(a)
          if len(str(a))>40+30*l:
            a="1"
          if len(str(a))>20+15*l: #120
            if compact(a) not in listaEsercizi:
              trovato=True
              listaEsercizi.insert(0,compact(a))
              listaSoluzioni.insert(0,soluzione)          
    Progresso.progress(100)
    return([listaEsercizi,listaSoluzioni])

if Bottone:
    Lista=generaListaEsercizi(Numero,Livello)
    L=Lista[0]
    Progresso.empty()
    testo="## Esercizi generati:  \n ###  \n"
    for i in range(0,Numero):
        es=L[i]
        #radioList.append(st.radio(str(i+1)+". $\\displaystyle "+latex(parse_expr(trig(str(es))))+"=1$\n\n\n"))
        testo=testo+str(i+1)+". $\\displaystyle "+latex(parse_expr(trig(str(es))))+"=1$\n\n\n"
    st.markdown(testo)
    testo="Codice LaTeX:\n\\begin{enumerate}\n"
    for i in range(0,Numero):
        es=L[i]
        testo=testo+"\\item $\\displaystyle "+latex(parse_expr(trig(str(es))))+"=1$\n"
    testo=testo+"\\end{enumerate}"    
    st.code(testo)
    testo="Codice Wolfram:\n"
    for i in range(0,Numero):
        es=L[i]
        testo=testo+str(i+1)+". "+convertiWolf(trig(str(es)))+"==1\n"
    st.code(testo)

    soluzione=""
    for k in range(0,Numero):
      soluzione=soluzione+"### Passaggi esercizio n."+str(k+1)+"\n"
      Sol=Lista[1]
      Sol[k].reverse()
      Sol1=accorciaDim(Sol[k])
      if Sol1!=["1"]:
        for passaggio in Sol1:
          #print(passaggio)
          soluzione=soluzione+"$\\displaystyle "+latex(parse_expr(trig(str(passaggio))))+"=1$\n\n\n"
      else:
        soluzione+="Vedi soluzione precedente\n"
    st.markdown(soluzione)
    st.markdown(footer,unsafe_allow_html=True)
    #st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    #st.markdown('<p style="color: grey;">© 2022 - marcodisce@gmail.com</p>', unsafe_allow_html=True)

  
    
    
    
