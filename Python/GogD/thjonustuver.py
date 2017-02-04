import numpy as np
import pandas as pd
import matplotlib.pylab as plt 
import scipy.optimize as sci
import math

def nytt_simtal(ID,simtal_inn,simtal_lokid):
   lengd_simtal= np.random.exponential(scale=100, size=None)
   status = "röð"
   simtal=dict([('ID',ID),('lengd_simtals',lengd_simtal),('stada',status),('simtal_inn',simtal_inn),('simtal_lokið',simtal_lokid)])
   return (simtal)

def millikomutimi(fjoldi_vidskiptavina):
   millitimi = np.random.poisson(lam=5.0, size=fjoldi_vidskiptavina)
   return (millitimi)

ID=0
simtalinn_sek=0
simtal=[]
millitimi = millikomutimi(15)
for i in millitimi:
   simtalinn_sek= simtalinn_sek+millitimi[i]
   simtal=nytt_simtal(ID,simtalinn_sek,20)
   ID +=1
   print(simtal)

print (simtal)



