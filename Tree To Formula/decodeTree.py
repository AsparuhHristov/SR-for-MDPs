# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 21:27:07 2017

@author: Paro
"""
from sympy import *

def replace(string):
    string=string.replace("div", "/")
    string=string.replace("sub", "-")
    string=string.replace("add", "+")
    string=string.replace("mul", "*")
    return string
    
def symbolRep(string):
    string=string.replace("X12", "(ser*((lambda/(mu_1*ser))^ser))")
    string=string.replace("X11", "(rho^(ser-c))")
    string=string.replace("X10", "((1-rho)*mu_2*(c+d))")
    string=string.replace("X9", "(1-rho)")
    string=string.replace("X8", "(ser*mu_1)")
    string=string.replace("X7", "facb")
    string=string.replace("X6", "rho")
    string=string.replace("X5", "d")
    string=string.replace("X4", "ser")
    string=string.replace("X3", "c")
    string=string.replace("X2", "mu_2")
    string=string.replace("X1", "mu_1")
    string=string.replace("X0", "lambda")
    return string

def symbolPyt(string):
    string=string.replace("facb", "X[:,7]")
    string=string.replace("rho", "X[:,6]")
    string=string.replace("d", "X[:,5]")
    string=string.replace("ser", "X[:,4]")
    string=string.replace("c", "X[:,3]")
    string=string.replace("mu_2", "X[:,2]")
    string=string.replace("mu_1", "X[:,1]")
    string=string.replace("lambda", "X[:,0]")
    return string

def lat(string):
    string=string.replace("X[:,7]","\frac{(c-1)!}{s!}")
    string=string.replace("X[:,6]","\rho")
    string=string.replace("X[:,5]","d")
    string=string.replace("X[:,4]","s")
    string=string.replace("X[:,3]","c")
    string=string.replace("X[:,2]","\mu_2")
    string=string.replace("X[:,1]","\mu_1")
    string=string.replace("X[:,0]","\lambda")
    return string

def oneIter(string):
    indexRep=string.find(",")
    if indexRep==-1:
        return string
    indexDiv=string[:indexRep].rfind("/(")
    indexMin=string[:indexRep].rfind("-(")
    indexPls=string[:indexRep].rfind("+(")
    indexMul=string[:indexRep].rfind("*(")
    toRep=max(indexDiv,indexMin,indexPls,indexMul)
    string=swap(string,indexRep,toRep)
    return string
    
    
def swap(string, i, j):
    stringT = list(string)
    stringT[i] = stringT[j]
    stringT[j] = ''
    return ''.join(stringT)

def fullIter(string):
    string=replace(string)
    while string!=oneIter(string):
        string=oneIter(string)
    
    return string

def getFormula(string):
    string=fullIter(string)[1:-1]
    stringGood=symbolRep(string)
    resultGood=simplify(stringGood)
    resultPython=symbolPyt(str(resultGood))
    print("\nFormula \n")
    print(resultPython)
    print("\nLatex Version \n")
    print(latex(resultGood))
    return resultGood,resultPython
