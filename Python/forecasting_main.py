import numpy as np
import pandas as pd
import matplotlib.pylab as plt 
import scipy.optimize as sci
import math
#velur aðferð til að spá ef bestu aðferð, besta aðferð er skilgreind sem sú spá sem hefur lægsta MSRE á milli gagnasets og spágilda.
def select_forecast(M, spalengd):

    print('sláðu inn 1 til að finna bestu spáaðferð')
    print('sláðu inn 2 til að spá með Heimagerðri spáaðferð')
    print('sláðu inn 3 til að spá með hreifið meðaltal')
    print('sláðu inn 4 til að spá með veigið hreifið meðaltal')
    print('sláðu inn 5 til að spá með þreföld veldisjöfnun')
    Mo=int(input())
    if Mo==1:
        return(best_forecast(M,spalengd))
    if Mo==2:
        spa_heima=heimagerd_spa(M,spalengd)
        plt.plot(range(21,len(spa_heima)+21),spa_heima,linestyle='--')
        plt.title('Heimagerð spáaðferð gaf besta niðustöðu')
        return(spa_heima)
    if Mo==3:
        spa_MA=Moving_Average(M,spalengd)
        plt.plot(range(21,len(spa_MA)+21),spa_MA,linestyle='--')
        plt.title('Hreifið meðaltal gaf besta niðustöðu')
        return(spa_MA)
    if Mo==4:
        spa_WMA=weighted_Moving_Average(M,spalengd)
        plt.plot(range(21,len(spa_WMA)+21),spa_WMA,linestyle='--')
        return(spa_WMA)
    if Mo==5:
        Z=[0.2,0.2,0.2]
        res=sci.minimize(opti,Z, method='Nelder-Mead')
        spa_TEXP=triple_exponential_smoothing(M,7,res.x[0],res.x[1],res.x[2],spalengd)
        plt.plot(range(0,len(spa_TEXP)),spa_TEXP,linestyle='--')
        return(spa_TEXP)
#fall sem finnur þá spá aðferð sem gefur lægsta MRSE skekkju.
def best_forecast(data,spalengd):
    M=data
    Z=[0.2,0.2,0.2]
    res=sci.minimize(opti,Z, method='Nelder-Mead')
    spa_TEXP=triple_exponential_smoothing(M,7,res.x[0],res.x[1],res.x[2],spalengd)
    spa_heima=heimagerd_spa(M,spalengd)
    spa_MA=Moving_Average(M,spalengd)
    spa_WMA=weighted_Moving_Average(M,spalengd)
    
    err_heim=MSE(M[21:],spa_heima)
    err_MA=MSE(M[21:],spa_MA)
    err_WMA=MSE(M[21:],spa_WMA)
    err_TEXP=(MSE(M,spa_TEXP))

    lamark=min(err_heim,err_MA,err_WMA,err_TEXP)
    if lamark==err_heim:
        plt.plot(range(21,len(spa_heima)+21),spa_heima,linestyle='--')
        plt.title('Heimagerð spáaðferð gaf besta niðustöðu, spáin er brotalínan')
        return (spa_heima)
    if lamark==err_MA:
        plt.plot(range(21,len(spa_MA)+21),spa_MA,linestyle='--')
        plt.title('Hreifið meðaltal gaf besta niðustöðu,spáin er brotalínan')
        return (spa_MA)
    if lamark==err_WMA:
        plt.plot(range(21,len(spa_WMA)+21),spa_WMA,linestyle='--')
        plt.title('Veigið hreifið Meðaltal gaf bestu niðurstöðu,spáin er brotalínan')
        return (spa_MA)
    if lamark==err_TEXP:
        plt.plot(range(0,len(spa_TEXP)),spa_TEXP,linestyle='--')
        plt.title('Þreföld veldisjöfnun gaf bestu niðurstöðu,spáin er brotalínan')
        return (spa_TEXP)

def set_dates(data):
    print('sláðu inn mörk tímabilsins sem athugið að það þarf að vera á milli 20160101 og 20160630 og að minstakosti 21 dagur:')
    start_date=input("sláðu inn upphaf tímabils:")
    stop_date=input("sláðu inn lok tímabilsins:")
    data=data[data["dagsetning"]>int(start_date)]
    data=data[data["dagsetning"]<int(stop_date)]
    calls_inn,Date,weekday=Config_data(data)
    if len(calls_inn)<21:
        print("Villa:tímabil var styttra en 21 dagur ")
        quit()
    return (calls_inn,Date,weekday)

def Config_data(Data):
    M=[]
    V=0
    Date=[]
    vikudagur=[]
    for i in range(Data.index[0],len(Data.index)+Data.index[0]):
        V=V+Data.loc[i,"simtol_inn"]
        if Data.loc[i,"klukkustund"]==21:
            M.append(V)
            V=0
            Date.append(Data.loc[i,"dagsetning"])
            vikudagur.append(Data.loc[i,"dagur"])
    return(M,Date,vikudagur)


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
def weighted_Moving_Average(data,lengdspa): #Hreifð veigið meðaltal inntak er spágögn og fjöldi daga sem á að spá áfram um
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
#Fall sem hjálpar til við að besta stuðlana fyrir þrefalda veldisjöfnun vigurinn X er upphafs gildinn sem byrjað er með við að reyna að lámarka
def opti(x):
    spa=triple_exponential_smoothing(M,7,x[0],x[1],x[2],14)

    return(MSE(M,spa))
#Fall sem býr finnur hvaða vikudaga er spáð fyrir fram í tíman intaks breytur síðasti vikudagur í raungögnum 
def viku_dagar(sidastid,lengdspa):
    dagur=[]
    dagur.append(sidastid)
    for i in range(1,lengdspa+1): 
        if  dagur[i-1]=='man':
            dagur.append('tri')
        if dagur[i-1]=='tri':
            dagur.append('mid')
        if dagur[i-1]=='mid':
            dagur.append('fim')
        if dagur[i-1]=='fim':
            dagur.append('fos')
        if dagur[i-1]=='fos':
            dagur.append('lau')
        if dagur[i-1]=='lau':
            dagur.append('sun')
        if dagur[i-1]=='sun':
            dagur.append('man')
    return (dagur[1:])
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
#inngangs breytur eru spáin, hvaða vikudaga það var spáð fram um og viktir fyrir álag yfir vinnudaginn á missmunandi vikudögum
def dreifing_klst(spa,dagar,man,tri,mid,fim,fos,lau,sun):

    timar=[]
    for i in range(0,len(dagar)):
        if dagar[i]=='man':
            timar.append([x*spa[i] for x in man])
        if dagar[i]=='tri':
            timar.append([x*spa[i] for x in tri])
        if dagar[i]=='mid':
            timar.append([x*spa[i] for x in mid])
        if dagar[i]=='fim':
            timar.append([x*spa[i] for x in fim])
        if dagar[i]=='fos':
            timar.append([x*spa[i] for x in fos])
        if dagar[i]=='lau':
            timar.append([x*spa[i] for x in lau])
        if dagar[i]=='sun':
            timar.append([x*spa[i] for x in sun])
    titlestring='spáð álag fyrir dag nr:'

    for i in range(0,len(timar)):
        plt.figure()
        plt.plot(range(9,len(timar[i])+9),timar[i])
        r=titlestring+ repr(i+1)+' '+repr(dagar[i])
        plt.title(r)
        plt.axis([9,21,0, 250])


#fall sem reiknar MSRE
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
#spalengd=int(input('Hvað á að spá fyrir marga daga fram í tíman:'))
(man,tri,mid,fim,fos,lau,sun)=Timavigt(DataV)
(M,date,vikudagur)=set_dates(Data)
spalengd=14

spa_dagar=viku_dagar(vikudagur[-1],spalengd)



#vigur með upphaflegum gildum Fyrir fasta í tripple exponential smoothing , 
Z=[0.2,0.2,0.2]

res=sci.minimize(opti,Z, method='Nelder-Mead')
spa_TEXP=triple_exponential_smoothing(M,7,res.x[0],res.x[1],res.x[2],spalengd)
spa_heima=heimagerd_spa(M,spalengd)
spa_MA=Moving_Average(M,spalengd)
spa_WMA=weighted_Moving_Average(M,spalengd)

#Tima_dreifing_ExpS=dreifing_klst(Data,spa_TEXP,vikudagur)

MM=select_forecast(M,spalengd)

plt.plot(range(0,len(M)),M)
plt.show()
dreifing_klst(MM[-14:],spa_dagar,man,tri,mid,fim,fos,lau,sun)


plt.show()
