import yfinance as yf
import csv

#data = yf.download("2330.TW", start='2023-01-01')
#data.to_csv('台積電.csv')


file = open('2330.csv',encoding='utf-8',mode='r',newline='')    
print(file.read())
file.close() #實體方法
print(file.closed) #實體attribute
csv_DictReader=csv.DictReader(file)