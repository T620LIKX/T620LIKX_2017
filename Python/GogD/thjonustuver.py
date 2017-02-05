import numpy as np
import pandas as pd
import matplotlib.pylab as plt 
import scipy.optimize as sci
import math

clock = 0
def UpdateClock(n):
   global clock
   clock = clock + n

def StartDay():
   """
   Fall sem "opnar" innhringiverið og biður notendan að stilla upp vaktaplaninu og skilar
   út lista af starfsmönnunum.
   Note, seinna meir væri hægt að setja þetta upp með user interface-i
   """
   ListOfStaff = []
   #staff = int(input("Enter number of employees: "))
   global clock
   clock =0
   staff = 1
   for i in range(staff):
      #begin = int(input('Staff ' + str(i+1) + ' begins: '))
      #end = int(input('Staff ' + str(i+1) + ' ends: '))
      begin = 0
      end = 1000
      staffId = "StaffId" + str(i+1)
      staffId = {"StaffId": staffId,"Begins": begin, "Ends": end, "WorkinOn": "NAN", "Idel": "yes"}
      ListOfStaff.append(staffId)
   return ListOfStaff;
#Býr til nýtt símtal, hversu langt það er og upphafstillir breytur.
def nytt_simtal(ID,simtal_inn):
   lengd_simtal= int(np.random.exponential(scale=100, size=None)) # beta =100 parameter fyrir exponential 1/landa
   status = "waiting" # upphafstillum að símtal byrji í röð
   simtal=dict([('ID',ID),('lengd_simtals',lengd_simtal),('stada',status),('simtal_inn',simtal_inn)])
   return (simtal)

def millikomutimi(fjoldi_vidskiptavina):
   millitimi = np.random.poisson(lam=5.0, size=fjoldi_vidskiptavina) #býr til x  millikomutíma landa = 5 
   return (millitimi)

def service(ID,service_start,callduration,status):
   
   status = 'in service'
   customer_service = {'ID':ID,'service start':service_start,'status':status,'service end':service_start+callduration}
   return (customer_service)

def find_staff(listinn): #tekur inn ListOfStaff listann
#þessi forlykkja fer í gegnum listan staff finnur dict fyrir einn starfsmann og skilar id fyrir starfsmann ef hann er laus
   for i, x in enumerate(listinn):
      check=x.get('Idel')
      if check =='yes':
         staff_id=x.get('StaffId')
         return((staff_id))
      else:
         return()#allir starfsmennuppteknir hvað þá ?

def find_next_phonecall(listinn): #tekur inn simtol listann
#þessi forlykkja fer í gegnum listan simtol finnur dict fyrir eitt simtal og skilar id fyrir símtali ef simtal er í bið
   for i, x in enumerate(listinn):
      check=x.get('stada')
      if check =='waiting':
         simtal_id=x.get('ID')
         return((simtal_id))
      else:
         return() # ekkert símtal í bið hvað þá ?

#def set_employer_call():


ID=0
simtalinn_sek=0
simtol=[]
millitimi = millikomutimi(15)
ListOfStaff = StartDay()
print(ListOfStaff)

for i in millitimi:
   ID +=1  
   simtalinn_sek= simtalinn_sek+millitimi[i] # halda utan um hvern símtal kom inn.
   simtal=nytt_simtal(ID,simtalinn_sek)#býr til dict fyrir símtal
   simtol.append(simtal)#búa til lista með öllum símtölunum

for i in simtol:
   print (i)




