import csv
import sys
import os
import math

investments = {}
OHLC = {}
index_returns = {}
stock_returns = {}
index_variances = {}
index_risk = {}
stock_variances = {}
stock_risk = {}
betas = {}
alfas = {}

files = [f for f in os.listdir('.') if os.path.isfile(f) ]
for f in files:
    if f == '.DS_Store' or f == 'parser.py' :
        files.remove(f)
compositeFile = 'Composite.csv'
for f in files :
    with open(f) as csvfile:
        reader = csv.DictReader(csvfile)
        myDatas = []
        for row in reader:
            myDatas.append((row['Date'], row['Open'],row['High'], row['Low'],row['Close'], row['Volume'],row['Adj Close']))
        investments[f[0:-4]] = myDatas
def calculateOHLC(key) :
    OHLCarr = []
    for data in investments[key] :
        OHLCarr.append((data[0],((float(data[1])+float(data[2])+float(data[3])+float(data[4]))/4)))
    OHLC[key] = OHLCarr

def calculateReturns(keys) :
    myData = OHLC[keys]
    leng = len(myData)
    _returns = []
    for i in range(leng-1) :
        _returns.append((myData[i][0],((myData[i][1]-myData[i+1][1])/myData[i+1][1])))
    if "Index" in keys :
        index_returns[keys] = _returns
    else :
        stock_returns[keys] = _returns
def calculateVars(keys) :
    i=0
    total = 0
    if "Index" in keys :
        for data in index_returns[keys] :
            total += data[1]
            i += 1
        try :
            mean = total/i
        except :
            raise ZeroDivisionError()
        total = 0
        for data in index_returns[keys]:
            total += (data[1] - mean)*(data[1]-mean)
        index_variances[keys] = total/i
        index_risk[keys] = math.sqrt(total/i)
    else :
        for data in stock_returns[keys] :
            total += data[1]
            i += 1
        try :
            mean = total/i
        except :
            raise ZeroDivisionError()
        total = 0
        for data in stock_returns[keys]:
            total += (data[1] - mean)*(data[1]-mean)
        stock_variances[keys] = total/i
        stock_risk[keys] = math.sqrt(total/i)

def calculateCovs(key1,key2) :
    total=0
    i=0
    mean_stock = 0
    mean_index = 0
    for data in stock_returns[key1] :
        total += data[1]
        i += 1
    mean_stock = total/i
    total=0
    i=0
    for data in index_returns[key2] :
        total += data[1]
        i += 1
    mean_index = total/i
    total=0
    i=0
    if (len(stock_returns[key1])==len(index_returns[key2])) :
        print True
    else :
        print False
    #cov[key1+keys.split(' - ')[1]] = _beta
    print key1+key2.split(' - ')[1]
for keys in investments :
    calculateOHLC(keys)
    calculateReturns(keys)
    calculateVars(keys)

for key1 in stock_returns :
    for key2 in index_returns :
        calculateCovs(key1,key2)

print stock_risk
