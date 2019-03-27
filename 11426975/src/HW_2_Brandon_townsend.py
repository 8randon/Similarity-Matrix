# -*- coding: utf-8 -*-
"""
Created on Sat Mar 02 18:10:18 2019

@author: Brandon Townsend
"""

from timeit import timeit
import csv
import numpy as np
import pandas as pd
import time
from operator import itemgetter
     
        
start_time = time.time()
count = 0
p = 0
s = 0

movieID = []
userID = []

ud = {}

filename = './data/ratings.csv'
lastUser = '0'
col = -1

rows = np.empty(1)
columns = np.empty(1)
data = np.empty(1)

data = pd.read_csv(filename).values

md = {}
e=0

data = sorted(sorted(data,key=itemgetter(0)),key=itemgetter(1))

prevmov = data[0][1]
#print "===="
for i in data:
    if i[1] == prevmov:
        ud[i[0]]=float(i[2])
    else:
        md[prevmov] = dict(ud)
        ud.clear()
        prevmov=i[1]
        ud[i[0]] = float(i[2])

md[prevmov]=dict(ud)

#print "===="

df=pd.SparseDataFrame(md)

centarr = pd.SparseDataFrame(df-df.mean()).fillna(0)


simmat = pd.SparseDataFrame(np.dot(centarr.T,centarr))

n = np.linalg.norm(centarr,axis=0)
nt = np.linalg.norm(centarr.T,axis=1)

simmat = pd.DataFrame(simmat/n)
simmat = pd.DataFrame(simmat.T/nt)
kys = md.keys()
kys.sort()
simmat.columns=kys
simmat.index=kys


nbh = {}

for i in kys:
    
    nbh[i]=simmat[i].nlargest(6,keep='first')
    if nbh[i].get(i,0):
        nbh[i].drop(index=i)


estdict={}
tempdict={}
#print "===="

for key in kys:
    for usrky in centarr.index:
        if md[key].get(usrky,0)==0:
            c=0
            estimate=0
            sumnum=0.0
            sumdenom=0.0
            for movIndx in nbh[key].index:
                if c>=5:
                    break
                sumnum+=md[movIndx].get(usrky,0)*nbh[key][movIndx]
                if md[movIndx].get(usrky,0)!=0:
                    sumdenom+=nbh[key][movIndx]
                c+=1
            if sumdenom>0:
                estimate = sumnum/sumdenom
                tempdict[usrky] =estimate 
                
    if bool(tempdict):
        estdict[key]=dict(tempdict)
        tempdict.clear()
    
    
#print "===="
   
results = {}
estdf = pd.SparseDataFrame(estdict).T
estind = estdf.index

for i in centarr.index:
    results[i]=estdf[i].nlargest(5,keep='first').index.sort_values()
pd.SparseDataFrame(results).T.to_csv('./output.txt',columns=None, header=False, index=True, index_label=None,)
                 
end_time = time.time()        
 

Run_time=end_time-start_time
#print Run_time