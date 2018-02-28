# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 13:18:00 2017

@author: Paro
"""
import numpy as np
import MDP
import pickle
import TreeDecoder
from gplearn.genetic import SymbolicRegressor

    """
    The main program that generates a closed-form expression for MDPs.
    It uses the symbolic regression technique. Training data is generated
    via solving the MDPs with the corresponding module. Hereby, we use the
    already generated input data.
    """
    
def RunMain(name, SR_metric, weights, sqrt, rho, rand_state):
    X_train, y_train, g_train, X_test, y_test, g_test = GenerateData(rho)
    SR = RunSR(X_train, y_train, X_test, weights, SR_metric, sqrt, rand_state)
    y_pred, g_pred, g_single, g_errors = EvalutePredicted(SR, X_test, g_test)
    SaveOutput(SR, g_pred, name)
    formula = TreeDecoder(SR)
    return SR, y_pred, g_pred, g_single, g_errors

def GenerateData(rho):
    data = np.genfromtxt('results.csv', delimiter=' ')
    data = data[(data[:,6]>0)&(data[:,2]==1)]
    X = data[:,2:7]
    y = data[:,7]
    g = data[:,8]
    
    X_test, y_test, g_test = GenerateTestData(X,y,g,rho)
    X_train, y_train, g_train = GenerateTrainData(X,y,g,rho)
    
    return X_train, y_train, g_train, X_test, y_test, g_test

def GenerateTestData(X,y,g,rho):
    testIndxs = (np.round(X[:,1],3)==2.4) | (np.round(X[:,1],3)==6.0) | (np.round(X[:,1],3)==10.8)
    X_test = X[testIndxs,:]
    if rho == 1: 
        X_test = np.column_stack((X_test,X_test[:,0]*((1/X_test[:,1])/2+(X_test[:,2]+X_test[:,3])/2)))
    if rho == 2: 
        X_test = np.column_stack((X_test,X_test[:,0]/X_test[:,1],X_test[:,0]*(X_test[:,2]+X_test[:,3])))
    if rho == 3: 
        X_test = np.column_stack((X_test,X_test[:,0]*((1/X_test[:,1])/2+(X_test[:,2]+X_test[:,3])/2)))
        X_test = np.column_stack((X_test,X_test[:,4]*X_test[:,3]+X_test[:,2]))

    y_test = y[testIndxs]
    g_test = g[testIndxs]
    return X_test,y_test,g_test

def GenerateTrainData(X,y,g,rho):
    indxs = (np.round(X[:,1],3)==2.4) | (np.round(X[:,1],3)==7.2) | (np.round(X[:,1],3)==9.6) | (np.round(X[:,1],3)==12.0)
    indxsRest = (np.round(X[:,1],3)==3.6) | (np.round(X[:,1],3)==4.8) | (np.round(X[:,1],3)==8.4)
    
    X_train = X[indxs,:]
    y_train = y[indxs]
    g_train = g[indxs]
    
    X_scale_down = X_train.copy()
    X_scale_up = X_train.copy()
    X_train = X[indxsRest,:]
    
    X_scale_down[:,0:2] = X_scale_down[:,0:2]*100
    X_scale_down[:,2:4] = X_scale_down[:,2:4]/100
    
    X_scale_up[:,0:2] = X_scale_up[:,0:2]/100
    X_scale_up[:,2:4] = X_scale_up[:,2:4]*100
    
    X_train = np.concatenate((X_train, X_scale_down, X_scale_up))
    if rho == 1: 
        X_train = np.column_stack((X_train,X_train[:,0]*((1/X_train[:,1])/2+(X_train[:,2]+X_train[:,3])/2)))
    if rho == 2: 
        X_train = np.column_stack((X_train,X_train[:,0]/X_train[:,1],X_train[:,0]*(X_train[:,2]+X_train[:,3])))
    if rho == 3:
        X_train = np.column_stack((X_train,X_train[:,0]*((1/X_train[:,1])/2+(X_train[:,2]+X_train[:,3])/2)))
        X_train = np.column_stack((X_train,X_train[:,4]*X_train[:,3]+X_train[:,2]))
        
    y_train = np.concatenate((y[indxsRest], y_train, y_train))
    g_train = np.concatenate((g[indxsRest], g_train, g_train))
    return X_train, y_train, g_train

def GenerateWeights(X_train, weights):
    if weights==1:
        weights_vector = np.power(X_train[:,0]*((1/X_train[:,1])/2+(X_train[:,2]+X_train[:,3])/2),np.mod(X_train[:,4],51))
        for i in range(len(weights_vector)//50):
            sum_weights = np.sum(weights_vector[i*50:(i+1)*50])
            weights_vector[i*50:(i+1)*50] = weights_vector[i*50:(i+1)*50]/sum_weights
    else:
        weights_vector = (51-np.mod(X_train[:,4],51))**2
    return weights_vector
        
def RunSR(X_train, y_train, X_test, weights, SR_metric, sqrt, rand_state):
    operators_set=['add', 'sub', 'mul', 'div']
    if sqrt==1: operators_set = operators_set + ['sqrt']
    SR = SymbolicRegressor(population_size=5000,
                           generations=20, stopping_criteria=0.01,
                           p_crossover=0.65, p_subtree_mutation=0.1,
                           p_hoist_mutation=0.05, p_point_mutation=0.1,
                           max_samples=1, verbose=0, function_set = operators_set,
                           parsimony_coefficient=0.001, random_state=rand_state, init_depth=(2,6),
                           tournament_size=20,metric = SR_metric)
    if weights>0:
        weights_vector = GenerateWeights(X_train, weights)
        SR.fit(X_train, y_train, weights_vector)
    else:
        SR.fit(X_train, y_train)
    print(SR._program)
    return SR

def EvalutePredicted(SR, X_test, g_test):
    M=50
    N=30
    c1=1
    c2=1
    g_pred = []
    g_single = []
    
    y_pred=SR.predict(X_test)
    
    n = X_test.shape[0]
    for i in range(n//50):
        (lam,mu1,a,b)=X_test[i*50,:4]
        g_single=np.append(g_single, g_test[i*50])
        params = (M,N,c1,c2,lam,mu1,a,b)
        functionPredicted = MDP.ComposeF(np.append([0],y_pred[i*50:(i+1)*50]))
        f, newV, gMax = MDP.MDPSolver(params, f=functionPredicted)
        g_pred = np.append(g_pred,gMax)
        
    g_errors = np.divide(np.abs(g_single - g_pred),g_single)*100
    print(np.round(np.percentile(g_errors,[50,90,95,99,99.99]),2))
    return y_pred, g_pred, g_single, g_errors

def runProgram(X_train,y_train,w):
    SymbolicRegressor(population_size=5000,
                           generations=25, stopping_criteria=0.01,
                           p_crossover=0.65, p_subtree_mutation=0.1,
                           p_hoist_mutation=0.05, p_point_mutation=0.1,
                           max_samples=0.9, verbose=1, function_set=['add', 'sub', 'mul', 'div','sqrt'],
                           parsimony_coefficient=0.01, random_state=1, init_depth=(3,6),
                           tournament_size=10,metric='mean absolute error')

def SaveOutput(SR, g_pred, name):
    print(name)
    with open(name+".pkl", 'wb') as f:
        pickle.dump(SR, f)
    np.save(name, g_pred)
