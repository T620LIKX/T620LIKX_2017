import numpy as np
import pandas as pd
import matplotlib.pylab as plt 


def Dagar(gogn):
	res=[]
	for i in range(0,19):
		res.append(gogn[gogn["Vikunumer"]==i].Simtol_inn.sum())


	
	return res







Data = pd.DataFrame()
Data=pd.read_excel('E:\likanX\DataA.xlsx', skiprows=3,parse_cols='B:P')  #skrá sett inn í pandas dataframe - athugið slóð að skrá er breytileg

#Breytum íslenskum stöfum í dálka nöfnum og línubil tekinn út 
cols = Data.columns
cols = cols.map(lambda x: x.replace(' ', '_').replace('á','a').replace('Á','A').replace('ð','d').replace('í','i').replace('ö','o').replace('ú','u'))
Data.columns = cols
#íslenskir stafir teknir úr daga dálki
dag = Data.Dagur
dag =dag.map(lambda x: x.replace('ö','o').replace('á','a').replace('ð','d').replace('þ','t'))
Data.Dagur=dag

man=Data[Data["Dagur"] =='man']
tri=Data[Data["Dagur"] =='tri']
mid=Data[Data["Dagur"] =='mid']
fim=Data[Data["Dagur"] =='fim']
fos=Data[Data["Dagur"] =='fos']
lau=Data[Data["Dagur"] =='lau']
sun=Data[Data["Dagur"] =='sun']


man.plot(x='Klukkustund', y='Simtol_inn', style='o',title='Mánudagar')
tri.plot(x='Klukkustund', y='Simtol_inn', style='o',title='þriðjudagar')
mid.plot(x='Klukkustund', y='Simtol_inn', style='o',title='miðvikudagar')
fim.plot(x='Klukkustund', y='Simtol_inn', style='o',title='Fimmtudagar')
fos.plot(x='Klukkustund', y='Simtol_inn', style='o',title='Föstudagars')
lau.plot(x='Klukkustund', y='Simtol_inn', style='o',title='Laugardagar')
sun.plot(x='Klukkustund', y='Simtol_inn', style='o',title='Sunnudagar')
plt.show()

man_av=[]
man_std=[]
tri_av=[]
tri_std=[]
mid_av=[]
mid_std=[]
fim_av=[]
fim_std=[]
fos_av=[]
fos_std=[]
lau_av=[]
lau_std=[]
sun_av=[]
sun_std=[]

for i in range(8,22):
	man_av.append(man[man["Klukkustund"]==i].Simtol_inn.mean())
	man_std.append(man[man["Klukkustund"]==i].Simtol_inn.std())
	tri_av.append(tri[tri["Klukkustund"]==i].Simtol_inn.mean())
	tri_std.append(tri[tri["Klukkustund"]==i].Simtol_inn.std())
	mid_av.append(mid[mid["Klukkustund"]==i].Simtol_inn.mean())
	mid_std.append(mid[mid["Klukkustund"]==i].Simtol_inn.std())
	fim_av.append(fim[fim["Klukkustund"]==i].Simtol_inn.mean())
	fim_std.append(fim[fim["Klukkustund"]==i].Simtol_inn.std())
	fos_av.append(fos[fos["Klukkustund"]==i].Simtol_inn.mean())
	fos_std.append(fos[fos["Klukkustund"]==i].Simtol_inn.std())
	lau_av.append(lau[lau["Klukkustund"]==i].Simtol_inn.mean())
	lau_std.append(lau[lau["Klukkustund"]==i].Simtol_inn.std())
	sun_av.append(sun[sun["Klukkustund"]==i].Simtol_inn.mean())
	sun_std.append(sun[sun["Klukkustund"]==i].Simtol_inn.std())

S=range(8,22)
plt.figure()
plt.errorbar(S,man_av,man_std)
plt.title("Mánudagur | fjöldi innhringinga á hverjum klukkutíma. Meðaltal og skekkja yfir vinnudaginn")

plt.figure()
plt.errorbar(S,tri_av,tri_std)
plt.title("Þriðjudagur| fjöldi innhringinga á hverjum klukkutíma.Meðaltal og skekkja yfir vinnudaginn")

plt.figure()
plt.errorbar(S,mid_av,mid_std)
plt.title("Miðvikudagur| fjöldi innhringinga á hverjum klukkutíma. Meðaltal og skekkja yfir vinnudaginn")
plt.figure()
plt.errorbar(S,fim_av,fim_std)
plt.title("Fimmtudagur | fjöldi innhringinga á hverjum klukkutíma. Meðaltal og skekkja yfir vinnudaginn")
plt.figure()
plt.errorbar(S,fos_av,fos_std)
plt.title("Föstudagur | fjöldi innhringinga á hverjum klukkutíma. Meðaltal og skekkja yfir vinnudaginn")
plt.figure()
plt.errorbar(S,lau_av,lau_std)
plt.title("Laugardagur | Meðaltal og skekkja yfir vinnudaginn")
plt.figure()
plt.errorbar(S,lau_av,lau_std)
plt.title("Sunnudagur | Meðaltal og skekkja yfir vinnudaginn")
plt.show()


manudagar=Dagar(man)
tridudagar=Dagar(tri)
fostudagar=Dagar(fos)
midvikudagar=Dagar(mid)
fimmtudagar=Dagar(fim)
laugardagar=Dagar(lau)
sunnudagar=Dagar(sun)
V=range(0,19)

plt.figure()
plt.plot(V,fostudagar)
plt.title("fjöldi innhringinga á föstudögum eftir vikum")
plt.figure()
plt.plot(V,manudagar)
plt.title("fjöldi innhringinga á mánudögum eftir vikum")
plt.figure()
plt.plot(V,midvikudagar)
plt.title("fjöldi innhringinga á þriðjudögum eftir vikum")
plt.figure()
plt.plot(V,fimmtudagar)
plt.title("fjöldi innhringina á miðvikudögum eftir vikum")
plt.figure()
plt.plot(V,laugardagar)
plt.title("fjöldi innhringina á laugardögum eftir vikum")
plt.figure()
plt.plot(V,sunnudagar)
plt.title("fjöldi innhringina á sunnudögum eftir vikum")

plt.show()