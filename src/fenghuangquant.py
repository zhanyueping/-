

import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import numpy as np
import keras
import sys 
import pathlib
import os
import io

import urllib   #py3
from PIL import Image
import pickle
# import the relevant Keras modules
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras import *
from keras.models import load_model
import mpl_toolkits
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

from PerformanceIndex import GetMaxReverse,GetProfitPerYear,TransPriceList2ProfitList,GetWinningPercent

def load_csv_to_dict():
    alldata = {}
    csvspath = r"..\round1\round1"
    filelist = [(file, int(file.split('.')[0])) for file in os.listdir(csvspath)]
    filelist = sorted(filelist, key = lambda x : x[1])
    
    for (file,days) in filelist:
        filepath = os.path.join(csvspath,file)
        rhandle = open(filepath,'r')
        for line in rhandle.readlines():
#             print (line)
            items = line.split(',')
            if items[0] == 'code':
                continue
            stockcode = items[0]
            #没有该代码的数据
            if stockcode not in alldata:
                alldata[stockcode] = {}
                alldata[stockcode]['tradingstatus'] = []
                alldata[stockcode]['close'] = []
                for i in range(len(items) - 2):
                    factorname = "f%d"%(i + 1)
                    alldata[stockcode][factorname] = []
                    if days > 1:
#                         print(days)
                        for j in range(days - 1):
                            alldata[stockcode][factorname].append(0.0)
                for j2 in range(days - 1):
                    #没有上市
                    alldata[stockcode]['tradingstatus'].append(0.0)
                    alldata[stockcode]['close'].append(0.0)
            if len(alldata[stockcode]['tradingstatus']) < days - 1:
                stopdays = days - 1 - len(alldata[stockcode]['tradingstatus']) 
                print (days - 1,len(alldata[stockcode]['tradingstatus']),len(alldata['stock100980']['tradingstatus']))
                for j3 in range(stopdays):
                    alldata[stockcode]['tradingstatus'].append(0)
                    alldata[stockcode]['close'].append(alldata[stockcode]['close'][-1])
                    for i in range(len(items) - 2):
                        factorname = "f%d"%(i + 1)
                        alldata[stockcode][factorname].append(0.0)
            if len(alldata[stockcode]['tradingstatus']) == days - 1:
                alldata[stockcode]['tradingstatus'].append(1)
                alldata[stockcode]['close'].append(float(items[1]))
                for i in range(len(items) - 2):
                    factorname = "f%d"%(i + 1)
#                     print (stockcode,factorname,items[i + 2])
                    alldata[stockcode][factorname].append(float(items[i + 2]))
            else:
                print('something is wrong')
                return
#             print(alldata[stockcode]['close'])
        #end of file
    #end of dir
    
    dictfilepath = r"..\round1\round1\alldataditc.txt"
    try:
        whandle = open(dictfilepath,'wb')
        pickle.dump(alldata,whandle)
    except Exception:
        print ("write file error")
                    
                
                        
            
def divide_data(dictpath):
    rhandle = open(dictpath,'rb')         
    alldata = pickle.load(rhandle)  
    rhandle.close()
    errorcodes = []
    for stock in alldata.keys():
        closelist = alldata[stock]['close']
        for i in range(len(closelist) - 1):
            if float(closelist[i]) and (float(closelist[i + 1])/float(closelist[i]) - 1 ) * 100 > 10.5:
                print(float(closelist[i + 1])/float(closelist[i]) - 1)
                print(stock,closelist[:i+1],closelist[i+1:])
                print(stock,alldata[stock]['f1'][:i+1],alldata[stock]['f1'][i+1:])
                print(stock,alldata[stock]['f2'][:i+1],alldata[stock]['f2'][i+1:])
                errorcodes.append(stock)
                break
            
    whandle = open(dictpath,'wb')         
    pickle.dump(alldata,whandle)  
    pickle.dump(errorcodes,whandle) 
    rhandle.close()


def build_model(inputs, output_size, neurons, activ_func = "linear",
                dropout =0.25, loss="mae", optimizer="adam"):
    model = Sequential()

    model.add(LSTM(neurons, input_shape=(inputs.shape[1], inputs.shape[2])))
    model.add(Dropout(dropout))

    model.add(Dense(units=output_size))
    model.add(Activation(activ_func))

    model.compile(loss=loss, optimizer=optimizer)
    return model


def performance(netvaluelist,tradedates):
    maxReverse = GetMaxReverse(netvaluelist)
    


dictfilepath = r"..\round1\round1\alldataditc.txt"
divide_data(dictfilepath)          
        
        
        
# load_csv_to_dict()     
    