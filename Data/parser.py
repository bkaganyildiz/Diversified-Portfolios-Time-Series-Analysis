import csv
import sys
import os
import math
import xlsxwriter

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
sharpRatios = {}


files = [f for f in os.listdir('.') if os.path.isfile(f) ]
for f in files:
    if f == '.DS_Store' or f == 'parser.py' or f == 'results.csv':
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

def meanCalculater(key,i_d) :
    i=0
    total = 0
    mean = 0
    if i_d == 0 :
        for data in index_returns[key] :
            total += data[1]
            i += 1
        try :
            mean = total/i
        except :
            raise ZeroDivisionError()
    elif i_d == 1 :
        for data in stock_returns[key] :
            total += data[1]
            i += 1
        try :
            mean = total/i
        except :
            raise ZeroDivisionError()
    return mean

def calculateVars(keys) :
    i=0
    total = 0.0
    if "Index" in keys :
        mean = meanCalculater(keys,0)
        i = len(index_returns[keys])
        for data in index_returns[keys]:
            total += (data[1] - mean)*(data[1]-mean)
        index_variances[keys] = total/i
        index_risk[keys] = math.sqrt(total/i)
    elif "Index" not in keys :
        mean = meanCalculater(keys,1)
        i=len(stock_returns[keys])
        for data in stock_returns[keys]:
            total += (data[1] - mean)*(data[1]-mean)
        stock_variances[keys] = total/i
        stock_risk[keys] = math.sqrt(total/i)
def calculateSRs(key) :
    sm = meanCalculater(key,1)
    sharpRatios[key] =  sm/(stock_risk[key])
def calculateSRi(key) :
    im = meanCalculater(key,0)
    sharpRatios[key] =  im/(index_risk[key])
def calculateBetas(key1,key2) :
    total=0
    i=len(stock_returns[key1])
    ms = meanCalculater(key1,1)
    mi = meanCalculater(key2,0)
    var = index_variances[key2]
    for k in range(i) :
        rs = stock_returns[key1][k][1]
        ri = index_returns[key2][k][1]
        total += (rs-ms)*(ri-mi)
    cov = total/i
    betas[key1+"-"+key2.split(' - ')[1]] = (cov/var)
    alfas[key1+"-"+key2.split(' - ')[1]] = ms - (cov/var)*mi

for keys in investments :
    calculateOHLC(keys)
    calculateReturns(keys)
    calculateVars(keys)

for key123 in stock_returns :
    for key223 in index_returns :
        calculateBetas(key123,key223)
for key in stock_returns :
    calculateSRs(key)
for key in index_returns :
    calculateSRi(key)
print alfas
print betas
averageReturns = []
portRisk = []
for key in stock_returns :
    total = 0
    i = 0
    if key == 'GOOG' :
        for data in stock_returns[key] :
            total += 266*data[1]
            i += 1
        averageReturns.append((key,total/i))
    elif key == 'XOM' :
        for data in stock_returns[key] :
            total += 2297*data[1]
            i += 1
        averageReturns.append((key,total/i))
    elif key == 'WMT' :
        for data in stock_returns[key] :
            total += 2822*data[1]
            i += 1
        averageReturns.append((key,total/i))
    elif key == 'JNJ' :
        for data in stock_returns[key] :
            total += 1786*data[1]
            i += 1
        averageReturns.append((key,total/i))
    elif key == 'BHP' :
        for data in stock_returns[key] :
            total += 5235*data[1]
            i += 1
        averageReturns.append((key,total/i))
    else :
        continue

for key in stock_returns :
    total = 0
    i = 0
    mean = 0
    if key == 'GOOG' :
        for data in averageReturns  :
            if data[0] == 'GOOG' :
                mean = data[1]
        for data in stock_returns[key] :
            total += (266*data[1] - mean)*(266*data[1] - mean)
            i += 1
        portRisk.append((key,math.sqrt(total/i)))
    elif key == 'XOM' :
        for data in averageReturns  :
            if data[0] == 'XOM' :
                mean = data[1]
        for data in stock_returns[key] :
            total += (2297*data[1] - mean)*(2297*data[1] - mean)
            i += 1
        portRisk.append((key,math.sqrt(total/i)))
    elif key == 'WMT' :
        for data in averageReturns  :
            if data[0] == 'WMT' :
                mean = data[1]
        for data in stock_returns[key] :
            total += (2822*data[1] - mean)*(2822*data[1] - mean)
            i += 1
        portRisk.append((key,math.sqrt(total/i)))
    elif key == 'JNJ' :
        for data in averageReturns  :
            if data[0] == 'JNJ' :
                mean = data[1]
        for data in stock_returns[key] :
            total += (1786*data[1] - mean)*(1786*data[1] - mean)
            i += 1
        portRisk.append((key,math.sqrt(total/i)))
    elif key == 'BHP' :
        for data in averageReturns  :
            if data[0] == 'BHP' :
                mean = data[1]
        for data in stock_returns[key] :
            total += (5235*data[1] - mean)*(5235*data[1] - mean)
            i += 1
        portRisk.append((key,math.sqrt(total/i)))
    else :
        continue
betaPort = {}
alfaPort = {}
def calculateBetaforPortfolio(key1,key2,mult) :
    total=0
    i=len(stock_returns[key1])
    for data in averageReturns :
        if data[0] == key1 :
            ms = data[1]
    mi = meanCalculater(key2,0)
    var = index_variances[key2]
    for k in range(i) :
        rs = stock_returns[key1][k][1]*mult
        ri = index_returns[key2][k][1]
        total += (rs-ms)*(ri-mi)
    cov = total/i
    betaPort[key1+"-"+key2.split(' - ')[1]] = (cov/var)
    alfaPort[key1+"-"+key2.split(' - ')[1]] = ms - (cov/var)*mi
for key1 in stock_returns :
    for key2 in index_returns :
        if key1 == 'GOOG' :
            calculateBetaforPortfolio(key1,key2,266)
        elif key1 == 'XOM' :
            calculateBetaforPortfolio(key1,key2,2297)
        elif key1 == 'WMT' :
            calculateBetaforPortfolio(key1,key2,2822)
        elif key1 == 'JNJ' :
            calculateBetaforPortfolio(key1,key2,1786)
        elif key1 == 'BHP' :
            calculateBetaforPortfolio(key1,key2,5235)
        else :
            continue

results = '../results.csv'
workbook = xlsxwriter.Workbook('../results.xlsx')
worksheet = workbook.add_worksheet()
workbook2 = xlsxwriter.Workbook('../graph.xlsx')
worksheet2 = workbook2.add_worksheet()
bold = workbook.add_format({'bold': 1})
bold2 = workbook2.add_format({'bold': 1})
worksheet.set_column(1, 1, 20)
worksheet.set_column(2, 2, 20)
worksheet.set_column(3, 3, 20)
worksheet.set_column(5, 5, 20)
worksheet.set_column(7, 7, 20)
worksheet2.set_column(1, 1, 20)
worksheet2.set_column(2, 2, 20)
worksheet.write('A1', 'Name', bold)
worksheet.write('B1', 'Average Return', bold)
worksheet.write('C1', 'Risk', bold)
worksheet2.write('A1', 'Name', bold2)
worksheet2.write('B1', 'Average Return', bold2)
worksheet2.write('C1', 'Risk', bold2)
worksheet.write('E1', 'Beta Market Name', bold)
worksheet.write('F1', 'Beta', bold)
worksheet.write('G1', 'Alpha Market Name', bold)
worksheet.write('H1', 'Alpha', bold)
worksheet.write('D1', 'Sharpe Ratio', bold)
row = 1
col = 0
row2 = 1
for key in stock_returns :
    beta = []
    alfa = []
    for key2 in betas :
        if key == key2.split('-')[0] :
            beta.append((key2.split('-')[1],betas[key2]))
            alfa.append((key2.split('-')[1],alfas[key2]))
    worksheet.write_string(row,col,key)
    worksheet.write_number(row,col+1,meanCalculater(key,1))
    worksheet.write_number(row,col+2,stock_risk[key])
    worksheet2.write_string(row2,col,key)
    worksheet2.write_number(row2,col+1,meanCalculater(key,1))
    worksheet2.write_number(row2,col+2,stock_risk[key])
    row2 += 1
    worksheet.write_number(row,col+3,sharpRatios[key])
    i=0
    for i in range(len(beta)) :
        worksheet.write_string(row+i,col+4,beta[i][0])
        worksheet.write_number(row+i,col+5,beta[i][1])
        worksheet.write_string(row+i,col+6,alfa[i][0])
        worksheet.write_number(row+i,col+7,alfa[i][1])
    row += i+1
#chart = workbook.add_chart({'type': 'dots'})
chart = workbook2.add_chart({'type': 'scatter'})
chart.labels = '=Sheet1!A2:A11'
chart.add_series({
    'values': '=Sheet1!B2:B11',
    'categories':   '=Sheet1!C2:C11',
    'series': {'labels': True},

})
chart.set_title ({'name': 'Sharpe Ratio'})
chart.set_x_axis({'name': 'Risk'})
chart.set_y_axis({'name': 'Average Returns'})
worksheet2.insert_chart('E2', chart)
workbook2.close()
workbook.close()
with open(results,'w') as csvfile :
    fieldnames = ['Name','Average Return','Risk','Beta Market Name','Beta','Alpha Market Name','Alpha','Sharpe Ratio']
    writer = csv.DictWriter(csvfile,fieldnames=fieldnames,dialect='excel-tab')
    writer.writeheader()
    for key in stock_returns :
        beta = []
        alfa = []
        for key2 in betas :
            if key == key2.split('-')[0] :
                beta.append((key2.split('-')[1],betas[key2]))
                alfa.append((key2.split('-')[1],alfas[key2]))
        writer.writerow({'Name': key,'Average Return':meanCalculater(key,1), 'Risk': stock_risk[key] ,'Beta' : beta[0][1],'Beta Market Name' : beta[0][0] ,'Alpha' :alfa[0][1] ,'Sharpe Ratio' : sharpRatios[key],'Alpha Market Name' : alfa[0][0]})
        for i in range(1,len(beta)) :
            writer.writerow({'Name': '','Average Return':'', 'Risk': '' ,'Beta Market Name' : beta[i][0],'Alpha Market Name' : alfa[i][0],'Beta' : beta[i][1] ,'Alpha' :alfa[i][1] ,'Sharpe Ratio' : ''})
