import numpy as np
import pandas as pd
import matplotlib.pylab as plt 
import scipy.optimize as sci
import math

def heimagerd_spa(data,lengdspa):
    spa=[]
    v=0
    F1=0
    F2=0
    F3=0
    F4=0
    F5=0

    for i in range(21,len(data)+lengdspa):
        if len(data)=<(i-21):
            F1=spa[i-21]*0.1
        else
            F1=data[i-21]*0.1
        if len(data)=<(i-14)
            F2=spa[i-14]*0.25
        else
            F2=data[i-14]*0.25
        if len(data)=<(i-7)
            F3=spa[i-7]*0.4
        else
            F3=data[i-7]*0.4
        if len(data)=<(i-1)
            F4=spa[i-1]*0.15
        else
            F4=data[i-1]*0.15
        if len(data)=<(i-2)
            F2=spa[i-2]*0.1
        else
            F2=data[i-2]*0.1
        spa.append(F1+F2+F3+F4+F5)
    

    return spa
def opti(x):
    spa=triple_exponential_smoothing(M,7,x[0],x[1],x[2],14)

    return(MSE(M,spa))

def viku_dagar(spa,gogndagar):
    for i in range(len(gogndagar),len(spa)): 
        if  gogndagar[i-1]=='man':
            gogndagar.append('tri')
        if gogndagar[i-1]=='tri':
            gogndagar.append('mid')
        if gogndagar[i-1]=='mid':
            gogndagar.append('fim')
        if gogndagar[i-1]=='fim':
            gogndagar.append('fos')
        if gogndagar[i-1]=='fos':
            gogndagar.append('lau')
        if gogndagar[i-1]=='lau':
            gogndagar.append('sun')
        if gogndagar[i-1]=='sun':
            gogndagar.append('man')
    return (gogndagar)
def Timavigt(Data):
    man=Data[Data["dagur"] =='man']
    tri=Data[Data["dagur"] =='tri']
    mid=Data[Data["dagur"] =='mid']
    fim=Data[Data["dagur"] =='fim']
    fos=Data[Data["dagur"] =='fos']
    lau=Data[Data["dagur"] =='lau']
    sun=Data[Data["dagur"] =='sun']

    man_av=[]
    tri_av=[]
    mid_av=[]
    fim_av=[]
    fos_av=[]
    lau_av=[]
    sun_av=[]
    ma=man.simtol_inn.sum()
    tr=tri.simtol_inn.sum()
    mi=mid.simtol_inn.sum()
    fi=fim.simtol_inn.sum()
    fo=fos.simtol_inn.sum()
    la=lau.simtol_inn.sum()
    su=sun.simtol_inn.sum()
    for i in range(9,22):
        man_av.append(man[man["klukkustund"]==i].simtol_inn.sum())
        tri_av.append(tri[tri["klukkustund"]==i].simtol_inn.sum())
        mid_av.append(mid[mid["klukkustund"]==i].simtol_inn.sum())
        fim_av.append(fim[fim["klukkustund"]==i].simtol_inn.sum())
        fos_av.append(fos[fos["klukkustund"]==i].simtol_inn.sum())
        lau_av.append(lau[lau["klukkustund"]==i].simtol_inn.sum())
        sun_av.append(sun[sun["klukkustund"]==i].simtol_inn.sum())


    man_av[:]=[x/ma for x in man_av]
    tri_av[:]=[x/tr for x in tri_av]
    mid_av[:]=[x/mi for x in mid_av]
    fim_av[:]=[x/fi for x in fim_av]
    fos_av[:]=[x/fo for x in fos_av]
    lau_av[:]=[x/la for x in lau_av]
    sun_av[:]=[x/su for x in sun_av]

    return (man_av, tri_av, mid_av, fim_av,fos_av,lau_av,sun_av)
def dreifing_klst(Data,spa,gogndagar):
    (man,tri,mid,fim,fos,lau,sun)=Timavigt(Data)
    A=len(gogndagar)
    vikudag=viku_dagar(spa,gogndagar)
    timar=[]
    for i in range(A,len(spa)):
        if vikudag[i]=='man':
            timar.append([x*spa[i] for x in man])
        if vikudag[i]=='tri':
            timar.append([x*spa[i] for x in tri])
        if vikudag[i]=='mid':
            timar.append([x*spa[i] for x in mid])
        if vikudag[i]=='fim':
            timar.append([x*spa[i] for x in fim])
        if vikudag[i]=='fos':
            timar.append([x*spa[i] for x in fos])
        if vikudag[i]=='lau':
            timar.append([x*spa[i] for x in lau])
        if vikudag[i]=='sun':
            timar.append([x*spa[i] for x in sun])
    return(timar)


def MSE(M,spa):
    res=0
    for i in range(0,len(M)):
        res=res+math.sqrt((M[i]-spa[i])**2)
    return res/len(M)

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
    res = []
    seasonals = seasonal_fastar(data, x)
    
    for i in range(len(data)+spa):
        if i == 0:
            smooth = data[0]
            t=trend(data, x)
            res.append(data[0])
            continue
        if i >= len(data):
            m = i - len(data) + 1
            res.append((smooth + m*t) + seasonals[i%x])
        else:
            val = data[i]
            last_smooth, smooth = smooth, alpha*(val-seasonals[i%x]) + (1-alpha)*(smooth+t)
            t = beta * (smooth-last_smooth) + (1-beta)*t
            seasonals[i%x] = gamma*(val-smooth) + (1-gamma)*seasonals[i%x]
            res.append(smooth+t+seasonals[i%x])
    return res


Data = pd.DataFrame()
Data=pd.read_excel('e:\likanX\DataA.xlsx', skiprows=3,parse_cols='B:P')  #skrá sett inn í pandas dataframe - athugið slóð að skrá er breytileg

#Breytum íslenskum stöfum í dálka nöfnum og línubil tekinn út 
cols = Data.columns
cols = cols.map(lambda x: x.replace(' ', '_').replace('á','a').replace('Á','A').replace('ð','d').replace('í','i').replace('ö','o').replace('ú','u').lower())
Data.columns = cols
#íslenskir stafir teknir úr daga dálki
dag = Data.dagur
dag =dag.map(lambda x: x.replace('ö','o').replace('á','a').replace('ð','d').replace('þ','t'))
Data.dagur=dag
DataV=Data
Data=Data[Data["manudur"]<5]


M=[]
V=0
Date=[]
Datafull=[]
vikudagur=[]
vikudagur2=[]
for i in range(0,len(Data.index)):
    V=V+Data.loc[i,"simtol_inn"]
    if Data.loc[i,"klukkustund"]==21:
        M.append(V)
        V=0
        Date.append(Data.loc[i,"dagsetning"])
        vikudagur.append(Data.loc[i,"dagur"])
V=0
for i in range(0,len(DataV.index)):
    V=V+DataV.loc[i,"simtol_inn"]
    if DataV.loc[i,"klukkustund"]==21:
        Datafull.append(V)
        V=0
        vikudagur2.append(DataV.loc[i,"dagur"])
alph=0.2
beta=0.2
gamma=0.2
spalengd=14
x=triple_exponential_smoothing(M,7,alph,beta,gamma,spa)
Z=[0.2,0.2,0.2]

res=sci.minimize(opti,Z, method='Nelder-Mead')
Sopt=triple_exponential_smoothing(M,7,res.x[0],res.x[1],res.x[2],spa)
err=(MSE(M,Sopt))

plt.figure()
plt.plot(range(0,len(M)),M,marker='o',linestyle='-')

plt.plot(range(len(M),len(x)),x[len(M):], marker='o',linestyle='-',color='r')
plt.title("firsta spá alpa=0,2, beta=0,2 gamma=0,2")


plt.figure()

plt.plot(range(0,len(Datafull)),Datafull,marker='o',linestyle='-')
plt.errorbar(range(0,len(Sopt)),Sopt,yerr=err ,marker='o',linestyle='--')
plt.title("lámörkuð MSE skekkja")



Tima_dreifing=dreifing_klst(Data,Sopt,vikudagur)
titlestring='Þreföldveldisjöfnun:Símaálag yfir vinnudagin spá dagur nr: '
for i in range(0,len(Tima_dreifing)):
    plt.figure()
    plt.plot(range(9,len(Tima_dreifing[i])+9),Tima_dreifing[i])
    r=titlestring+ repr(i+1)
    plt.title(r)
    plt.axis([9,21,0, 120])
plt.show()

spahal=heimagerd_spa(M,spa)
plt.figure
errspah=MSE(M[21:],spahal)
print=(errspah)
plt.plot(range(21,len(spahal)+21),spahal)
plt.plot(range(0,len(Datafull)),Datafull)
plt.show()