import numpy as np
import pandas as pd
import matplotlib.pylab as plt 
from sqlalchemy import create_engine
#Línur sem eru kommentaðar út innihalda kóða þar sem hver notandi þarf að gera breytingar
def movingaverage(df):
	vikur = int(input('Hversu margar vikur viltu? '))
	dagar = vikur*5
	endir = df["Símtöl inn"].count()
	byrjun = endir-dagar
	summa = 0
	for i in range (byrjun, endir):
		#print(df.loc[i,['Símtöl inn']])
		summa = summa + df.loc[i,['Símtöl inn']]
	spa = summa/vikur
	return spa


df = pd.DataFrame()
df = pd.read_excel('/Users/vesteinnsigurjonsson/Desktop/HR/6Vor 2017/Líkan X/T620LIKX_2017/Python/DataA.xlsx', skiprows=3,parse_cols='B:P'.lower()) 

spa = movingaverage(df)

#df.append(pd.DataFrame([spa],columns=str("Símtöl inn")))
print('I naestu viku munu liklega %d simtol berast' %(spa) )
print('Á hverjum degi munu %d simtol berast' %(spa/7))

