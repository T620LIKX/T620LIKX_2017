import numpy as np
import pandas as pd
import matplotlib.pylab as plt 
import math

def UpdateClock(n):
   global clock
   clock = 0 # núllstilla klukku

def StartDay():
   """
   Fall sem "opnar" innhringiverið og biður notendan að stilla upp vaktaplaninu á starfsmönnunum og skilar
   út lista af dictonarys af starfsmönnunum.
   WorkingOn: Id á símtali ef er að þjónusta
            idle ef laus   

   IsWorking: yes ef starfsmaðurinn er á vakt
            No ef starfsmaðurinn er búinn að vakt eða ekki byrjaður.
   """
   global clock
   clock = 0 #Núllstillir klukkuna í upphafi dags.
   ListOfStaff = []
   for i in range(GeneralInfo["NumberOfStaff"]):
      #begin = int(input('Staff ' + str(i+1) + ' begins: '))
      #end = int(input('Staff ' + str(i+1) + ' ends: '))
      begin = 0 #harðkóða upphafs og endatíma fyrir starfsmanninn til að byrja með.
      end = 1000
      staffId = {"StaffId": i+1,"Begins": begin, "Ends": end, "WorkinOn": "idle", 'IsWorking': "no"}
      ListOfStaff.append(staffId)
   return ListOfStaff;

def UpdateStatusOffStaff():
   '''
   Þetta fall athugar hvort starfsmaður á að vera mættur í vinnuna og ef svo er þá uppfærir það stöðuna á honum.
   Sömuleiðis athuga það ef starfsmaður er búinn á vaktinni sinni.

   Ef starfsmaðurinn er að vinna þá athugar fallið hvort starfsmaðurinn sé að vinna í símtali. Ef það er komin tími á að símtalinu ljúki þá
   uppfærir falli það með því að setja starfsmanninn í status og biður þá annað fall að uppfæra stöðuna á símtalinu.
   
   Note: Ef starfsmaður er í símtali þegar vaktin er búinn þá þarf að útfæra eitthva hérna svo hann ljúki við það áður en hann pakkar saman.
   '''

   for i in ListOfStaff:
      if(i["IsWorking"] == "no" and i["Begins"] == clock):
         i["IsWorking"] = "yes"
      if(i["IsWorking"] == "yes" and i["Ends"] >= clock and i["WorkingOn"] == "idle":
         i["IsWorking"] = "no"

#Býr til nýtt símtal, hversu langt það er og upphafstillir breytur.
def nytt_simtal(ID,simtal_inn):
      """
   Býr til nýtt símtal og upphafstillir breytur.
   Breytan status heldur utan um í hvaða fasa símtalið er.
   A: Er ekki búinn að hringja.
   B: Er í röð.
   C: Er í þjónustu.
   D: Er búinn að fá þjónustu.
   """
   lengd_simtal= int(np.random.exponential(scale=100, size=None)) # beta =100 parameter fyrir exponential 1/landa
   simtal=dict([('ID',ID),('lengd_simtals',lengd_simtal),('stada','A'),('simtal_inn',simtal_inn)])
   return (simtal)

def GeneratePhoneCalls():
   '''
   Þetta fall býr til lista af dictonarys af símtölum yfir daginn með því að nota fallið nytt_simtal.
   Note: Hérna væri hægt að útfæra frekari líkindadreifinu á símtölinn þegar það er fyrir hendi
   '''

   millitimi = np.random.poisson(lam=5.0, size=15) #Fjldi simtala a dag er harðkóðað sem 15

   ID = 0
   simtalinn_sek = 0
   simtol=[]
   for i in millitimi:
      ID += 1 
      simtalinn_sek = simtalinn_sek + millitimi[i] 
      simtal = nytt_simtal(ID, simtalinn_sek) 
      simtol.append(simtal) 
   return simtol;

def UpdateStatusOfPhoneCall():
   '''
   Þetta fall athugar hvort einhver sé búinn að slá á þráðinn á innhringiverið og uppfærir þá stöðuna á því símtali.
   '''
   for i in ListOfPhoneCalls:
      if i['Simtal_Inn'] == clock and i["status"] = "A" :
         i["status"] = "B"

def service(ID,service_start,callduration,status):
  
   customer_service = {'CALLID':ID,'service start':service_start,'status':'C','service end':service_start+callduration}
   return (customer_service)

def find_staff():
#þessi forlykkja fer í gegnum listan staff finnur dict fyrir einn starfsmann og skilar id fyrir starfsmann ef hann er laus
   for  i,x in enumerate(ListOfStaff): #kalla í listan af starfsfólki
      if x.get('Idel') =='yes':
         return(x.get('StaffId')) #skila staffid
      else:
         return()#allir starfsmennuppteknir hvað þá ?

def find_next_phonecall(): 
#þessi forlykkja fer í gegnum listan simtol finnur dict fyrir eitt simtal og skilar id fyrir símtali ef simtal er í bið
   for i,x in enumerate(simtol):#kalla í listan af símtölunum
      if x.get('stada') =='waiting':
         return(x.get('ID'))# skilar simtal id
      else:
         return('NAN') # ekkert símtal í bið hvað þá ?

def set_employer_call():
   next_phonecall=find_next_phonecall() # ID fyrir phonecall
   free_staff=find_staff() # ID fyrir starfsmann
   Eventlist=[]
   event = {"Call_ID": next_phonecall,"Staff_ID": free_staff, "service_start": start , "service_end": start+duration }
   Eventlist.append(event)
   return(Eventlist)

GeneralInfo = {"OpenAt":  0, "CloseAt": 500, "NumberOfStaff": 1} #Note: seinna meir væri hægt að gera þetta að falli með user interface-i

ListOfStaff = StartDay()
ListOfPhoneCalls = GeneratePhoneCalls()
print(ListOfStaff)
for i in millitimi:
   ID +=1  
   simtalinn_sek= simtalinn_sek+millitimi[i] # halda utan um hvern símtal kom inn.
   simtal=nytt_simtal(ID,simtalinn_sek)#býr til dict fyrir símtal
   simtol.append(simtal)#búa til lista með öllum símtölunum

for i in simtol:
   print (i)

event=set_employer_call()

for i in event:
   print(i) 