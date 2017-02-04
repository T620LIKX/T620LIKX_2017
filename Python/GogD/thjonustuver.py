import numpy as np
import pandas as pd
import matplotlib.pylab as plt 
import scipy.optimize as sci
import math

#Býr til nýtt símtal, hversu langt það er og upphafstillir breytur.
def nytt_simtal(ID,simtal_inn):
   lengd_simtal= int(np.random.exponential(scale=100, size=None)) # beta =100 parameter fryirr exponential 1/landa
   status = "röð" # upphafstillum að símtal byrji í röð
   simtal=dict([('ID',ID),('lengd_simtals',lengd_simtal),('stada',status),('simtal_inn',simtal_inn),('simtal_lokið',simtal_inn+lengd_simtal)])
   return (simtal)

def millikomutimi(fjoldi_vidskiptavina):
   millitimi = np.random.poisson(lam=5.0, size=fjoldi_vidskiptavina) #býr til x  millikomutíma landa = 5 
   return (millitimi)

ID=0
simtalinn_sek=0
simtol=[]
millitimi = millikomutimi(15)
for i in millitimi:
   simtalinn_sek= simtalinn_sek+millitimi[i] # halda utan um hvern símtal kom inn.
   simtal=nytt_simtal(ID,simtalinn_sek)#býr til dict fyrir símtal
   ID +=1
   simtol.append(simtal)#búa til lista með öllum símtölunum

for i in simtol:
   print (i)










