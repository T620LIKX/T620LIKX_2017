import numpy as np
import pandas as pd
import matplotlib.pylab as plt 
import scipy.optimize as sci
import math

def opti(x):
    spa=triple_exponential_smoothing(M,7,x[0],x[1],x[2],14)

    return(MSE(M,spa))



def MSE(M,spa):
    res=0
    for i in range(0,len(M)):
        res=res+math.sqrt((M[i]-spa[i])**2)
    return res/len(M)

def Dagar(gogn):
	res=[]
	for i in range(0,19):
		res.append(gogn[gogn["vikunumer"]==i].simtol_inn.sum())

	return res

def DagarM(gogn):
	res=[]
	for i in range(1,6):
		res.append(gogn[gogn["manudur"]==i].simtol_inn.sum())

	return(res)
def Vikur(gogn):
	res=[]
	for i in range(0,26):
		res.append(gogn[gogn["vikunumer"]==i].simtol_inn.sum())

	return(res)

#https://grisha.org/blog/2016/02/17/triple-exponential-smoothing-forecasting-part-iii/  Heimild fyrir 3 föll hér á eftir
def trend(data, x):
    res = 0
    for i in range(x):
        res =res+(data[i+x]-data[i])/x
    
    return (res / x)

def seasonal_fastar(data, x):
    seasonals = {}
    season_averages = []
    fjoldi_seasons =int(len(data)/x)
    for j in range(fjoldi_seasons):
        season_averages.append(sum(data[x*j:x*j+x])/x)
    
    for i in range(x):
        C = 0
        for j in range(fjoldi_seasons):
            C = C + data[x*j+i]-season_averages[j]
        seasonals[i] = C/fjoldi_seasons
    return seasonals

def triple_exponential_smoothing(data, x, alpha, beta, gamma, spa):
    result = []
    seasonals = seasonal_fastar(data, x)
    
    for i in range(len(data)+spa):
        if i == 0:
            smooth = data[0]
            t=trend(data, x)
            result.append(data[0])
            continue
        if i >= len(data):
            m = i - len(data) + 1
            result.append((smooth + m*t) + seasonals[i%x])
        else:
            val = data[i]
            last_smooth, smooth = smooth, alpha*(val-seasonals[i%x]) + (1-alpha)*(smooth+t)
            t = beta * (smooth-last_smooth) + (1-beta)*t
            seasonals[i%x] = gamma*(val-smooth) + (1-gamma)*seasonals[i%x]
            result.append(smooth+t+seasonals[i%x])
    return result


Data = pd.DataFrame()
Data=pd.read_excel('E:\likanX\DataA.xlsx', skiprows=3,parse_cols='B:P')  #skrá sett inn í pandas dataframe - athugið slóð að skrá er breytileg

#Breytum íslenskum stöfum í dálka nöfnum og línubil tekinn út 
cols = Data.columns
cols = cols.map(lambda x: x.replace(' ', '_').replace('á','a').replace('Á','A').replace('ð','d').replace('í','i').replace('ö','o').replace('ú','u').lower())
Data.columns = cols
#íslenskir stafir teknir úr daga dálki
dag = Data.dagur
dag =dag.map(lambda x: x.replace('ö','o').replace('á','a').replace('ð','d').replace('þ','t'))
Data.dagur=dag
Data=Data[Data["manudur"]<4]



M=[];
V=0;

for i in range(21,len(Data.index)):
	V=V+Data.loc[i,"simtol_inn"]
	if Data.loc[i,"klukkustund"]==21:
		M.append(V)
		V=0

lengd=7
alph=0.2
beta=0.2
gamma=0.2
spa=14

x=triple_exponential_smoothing(M,lengd,alph,beta,gamma,spa)
Z=[0.2,0.2,0.2]

res=sci.minimize(opti,Z)
Sopt=triple_exponential_smoothing(M,7,res.x[0],res.x[1],res.x[2],spa)
err=(MSE(M,Sopt))
plt.figure()
plt.plot(range(0,len(M)),M,marker='o',linestyle='-')

plt.plot(range(len(M),len(x)),x[len(M):], marker='o',linestyle='-',color='r')
plt.title("firsta spá alpa=0,2, beta=0,2 gamma=0,2")


plt.figure()

plt.plot(range(0,len(M)),M,marker='o',linestyle='-')
plt.errorbar(range(0,len(Sopt)),Sopt,yerr=err ,marker='o',linestyle='--')
plt.title("lámörkuð MSE skekkja")
plt.show()

plt.figure()
