import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import csv 
from sqlalchemy import create_engine

def movingaverage(df,vikur):
	dagar = vikur*7
	endir = df["Símtöl inn"].count()
	byrjun = endir-dagar
	summa = 0
	for i in range (byrjun, endir):
		#print(df.loc[i,['Símtöl inn']])
		summa = summa + df.loc[i,['Símtöl inn']]
	spa = summa/vikur
	return spa

def movingaverage2(df, byrja, enda):
	cumsum = 0
	for i in range (byrja,enda):
		cumsum = cumsum + df.loc[i,['Símtöl inn']]
	spa = cumsum/(enda-byrja)
	return spa

df = pd.DataFrame()
df = pd.read_excel('/Users/vesteinnsigurjonsson/Desktop/HR/6Vor 2017/Líkan X/T620LIKX_2017/Python/DataA.xlsx', skiprows=3,parse_cols='B:P'.lower()) 


byrjun = 3
endir = df["Símtöl inn"].count()
lis = []

for i in range (byrjun,endir):
	spa = 0
	spa = movingaverage2(df,i-3,i)
	lis.append(spa)

tuple(lis)
df.set_index(['Símtöl inn']).to_records().tolist()

plt.plot(lis,'b')
plt.plot(df["Símtöl inn"],'r')
plt.ylabel('Símtöl')
plt.xlabel('Dagar')
plt.show()




#M=[];
#V=0;
#for i in range(21,len(df.index)):
#	V=V+df.loc[i,"Símtöl inn"]
#	if df.loc[i,"Klukkustund"]==21:
#		M.append(V)
#		V=0

#spagildi = movingaverage(df,3)

#print(spagildi)





