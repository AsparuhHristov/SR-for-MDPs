"""
Created on Tue Feb 27 13:40:45 2018

@author: hristov

This class translates the output of the SR algorithm to a readable mathematical
formula. More precisely, the output of the SR algorithm is a evolutionary 
program.


This class also simplifies the expression by using the sympy package.
"""

from sympy import *
init_printing(use_unicode=True)

def GetFormula(SR):
    
    """
    The main function to get the formula from the symbolic regression object
    
    """
    
    # Get the string of the tree from the object
    tree_string = str(SR._program)
    
    # Substitute the operators
    oper_string = ReplaceOperators(tree_string)
    
    # Open the brackets (from tree to formula)
    simplified = FullIterator(oper_string) [1:-1]
    
    simplified=simplify(string)
    print("\nFormula \n")
    print(simplified)
    print("\nLatex Version \n")
    print(latex(simplified))

    return simplified

def ReplaceOperators(tree_string):
    
    """
    Translates the mathematical operators
    
    >>> ReplaceOperators("sqrt(mul(X3, X1))")
    "sqrt(*(X3, X1))"            
    >>> ReplaceOperators("mul(sub(X3, mul(X2, X1)), div(X0, X1))")
    "*(-(X3, *(X2, X1)), /(X0, X1))"
    
    """
        
    tree_string = tree_string.replace("div", "/")
    tree_string = tree_string.replace("sub", "-")
    tree_string = tree_string.replace("add", "+")
    tree_string = tree_string.replace("mul", "*")
    
    return tree_string

def OneIteration(oper_string):
    
    """
    One iteration at a time! Gets the first "," and substitutes it with the
    corresponding binary mathematical operation.
    The input should be a string in which the mathematical operators are
    already translated
    
    >>> OneIteration("*(-(X3, *(X2, X1)), /(X0, X1))")
    '*((X3- *(X2, X1)), /(X0, X1))'
    >>> OneIteration('((X3- (X2* X1))* (X0/ X1))')
    '((X3- (X2* X1))* (X0/ X1))'
    
    """
    
    # Find the index of the ","
    index_replace = oper_string.find(",")
    
    # Check if there is a possibility to make the iteration
    if index_replace==-1:
        return oper_string
    
    # Find which mathematical operation it is and the corresponding index
    indexDiv = oper_string[:index_replace].rfind("/(")
    indexMin = oper_string[:index_replace].rfind("-(")
    indexPls = oper_string[:index_replace].rfind("+(")
    indexMul = oper_string[:index_replace].rfind("*(")
    math_operator = max(indexDiv,indexMin,indexPls,indexMul)
    
    oper_string = Swap(oper_string, index_replace, math_operator)
    
    return oper_string

def FullIterator(oper_string):
    
    """
    Performs OneIteration function until all the brackets are "opened".
    
    >>> FullIterator("*(-(X3, *(X2, X1)), /(X0, X1))")
    '((X3- (X2* X1))* (X0/ X1))'
    >>> FullIterator('((X3- (X2* X1))* (X0/ X1))')
    '((X3- (X2* X1))* (X0/ X1))'
    
    """
    
    oper_string = ReplaceOperators(oper_string)
    while oper_string != OneIteration(oper_string):
        oper_string = OneIteration(oper_string)
    
    return oper_string    

def Swap(string, i, j):
    
    """
    Simple swap function...
    
    """
    
    stringT = list(string)
    stringT[i] = stringT[j]
    stringT[j] = ''
    
    return ''.join(stringT)
