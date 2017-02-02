import numpy as np
import pandas as pd
import matplotlib.pylab as plt 
import scipy.optimize as sci
import math

def Moving_Average(data,lengdspa):
    spa=[]
    F1=0
    F2=0
    F3=0
    # ef dagur er ekki til í gögnum þá notum við spána til að "svindla"
    for i in range(21,len(data)+lengdspa):
        if len(data)<(i-21):
            F1=spa[i-21-21]    #ástæðan fyrir auka  -21 er að spá listinn er 21 staki styttri en gögnin
        else:                   
            F1=data[i-21]
        if len(data)-1<(i-14):
            F2=spa[i-14-21]
        else:
            F2=data[i-14]
        if len(data)-1<(i-7):
            F3=spa[i-7-21]
        else:
            F3=data[i-7]
        spa.append((F1+F2+F3)/3)
    return spa
def weighted_Moving_Average(data,lengdspa):
    spa=[]
    F1=0
    F2=0
    F3=0
    # ef dagur er ekki til í gögnum þá notum við spána til að "svindla"
    for i in range(21,len(data)+lengdspa):
        if len(data)<(i-21):
            F1=spa[i-21-21]*0.2    #ástæðan fyrir auka  -21 er að spá listinn er 21 staki styttri en gögnin
        else:                   
            F1=data[i-21]*0.2
        if len(data)-1<(i-14):
            F2=spa[i-14-21]*0.3
        else:
            F2=data[i-14]*0.3
        if len(data)-1<(i-7):
            F3=spa[i-7-21]*0.5
        else:
            F3=data[i-7]*0.5
        spa.append((F1+F2+F3))
    return spa


#heimagerð spá aðferð blanda af tveimur síðustu dögum og 3 sömu vikudögunum tekurinn gögn og hversu langt á að spá
def heimagerd_spa(data,lengdspa):
    spa=[]
    F1=0
    F2=0
    F3=0
    F4=0
    F5=0
    #ástæða fyrir if og else súpu  hér fyrir neðan er að þegar komið er út fyrir gögninn við spá þá þarf að 
    # nota spána til þess að spá áfram og spá listinn er 21 staki styttri en gögninn  af því að það þarf að hafa 
    #þrjár vikur til þess að að geta byrjað að spá með þessari aðferð
    for i in range(21,len(data)+lengdspa):
        if len(data)<(i-21):
            F1=spa[i-21-21]*0.05    #ástæðan fyrir auka  -21 er að spá listinn er 21 staki styttri en gögnin
        else:                   
            F1=data[i-21]*0.05
        if len(data)-1<(i-14):
            F2=spa[i-14-21]*0.25
        else:
            F2=data[i-14]*0.25
        if len(data)-1<(i-7):
            F3=spa[i-7-21]*0.4
        else:
            F3=data[i-7]*0.4
        if len(data)-1<(i-1):
            F4=spa[i-1-21]*0.3
        else:
            F4=data[i-1]*0.3
        if len(data)-1<(i-2):
            F2=spa[i-2-21]*0.2
        else:
            F2=data[i-2]*0.2
        spa.append(F1+F2+F3+F4+F5)
    

    return spa
#Fall sem hjálpar til við að besta stuðlana fyrir þrefalda veldisjöfnun
def opti(x):
    spa=triple_exponential_smoothing(M,7,x[0],x[1],x[2],14)

    return(MSE(M,spa))
#Fall sem býr finnur hvaða vikudaga er spáð fyrir fram í tíman
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
#fall sem Tekur inn gögnin og býr til vigt fyrir hverja vinnustund á hverjum vikudegi 
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
#fall sem notar spá, gögnin og dagana til þess að dreifa spá  spáðum degi yfir vinnudaginn
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

#fall sem reikna MSRE
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
Data=pd.read_excel('E:\likanX\DataA.xlsx', skiprows=3,parse_cols='B:P')  #skrá sett inn í pandas dataframe - athugið slóð að skrá er breytileg

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
spalengd=14
Z=[0.2,0.2,0.2]

res=sci.minimize(opti,Z, method='Nelder-Mead')
spa_TEXP=triple_exponential_smoothing(M,7,res.x[0],res.x[1],res.x[2],spalengd)


Tima_dreifing_ExpS=dreifing_klst(Data,spa_TEXP,vikudagur)



spa_heima=heimagerd_spa(M,spalengd)
spa_MA=Moving_Average(M,spalengd)
spa_WMA=weighted_Moving_Average(M,spalengd)
err_heim=MSE(M[21:],spa_heima)
err_MA=MSE(M[21:],spa_MA)
err_WMA=MSE(M[21:],spa_WMA)
err=(MSE(M,spa_TEXP))


heima=plt.plot(range(21,len(spa_heima)+21),spa_heima,linestyle='--', label='line 1')
Moving_A=plt.plot(range(21,len(spa_MA)+21),spa_MA,linestyle='--',label='line 2')
W_M_A=plt.plot(range(21,len(spa_WMA)+21),spa_WMA,linestyle='--',label='line 3')
TEXP=plt.plot(range(0,len(spa_TEXP)),spa_TEXP,linestyle='--',label='line 4')
D=plt.plot(range(0,len(Datafull)),Datafull)

plt.legend([heima,Moving_A,W_M_A,TEXP,D],['Heimagerð aðferd','Moving Average','Weighted MA','smoothing','Data'])


plt.show()
