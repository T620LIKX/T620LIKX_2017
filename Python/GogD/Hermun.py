import numpy as np
import pandas as pd
import matplotlib.pylab as plt 
import scipy.optimize as sci
import math

#======================================================================
GeneralInfo = {"OpenAt":  0, "CloseAt": 1000, "NumberOfStaff": 1} #	Note, seinna meir væri hægt að gera þetta að falli með user interface-i

clock = 0

def UpdateClock(n):
	global clock
	clock = clock + n

def StartDay():
	"""
	Fall sem "opnar" innhringiverið og biður notendan að stilla upp vaktaplaninu á starfsmönnunum og skilar
	út lista af dictonarys af starfsmönnunum.
	WorkingOn: Id á símtali ef er að þjónusta
			   Idle ef laus   
	IsWorking: Yes ef starfsmaðurinn er á vakt
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

		staffId = "StaffId" + str(i+1)
		staffId = {"StaffId": staffId,"Begins": begin, "Ends": end, "WorkinOn": "idle", 'IsWorking': "No"}
		ListOfStaff.append(staffId)
	return ListOfStaff;

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

	simtal = {"ID": ID, 'status': "A", 'lengd_simtals':lengd_simtal, 'simtal_inn': simtal_inn, 'simtal_lokid': 0}
	return (simtal);

def GeneratePhoneCalls():

	millitimi = np.random.poisson(lam=5.0, size=100) #Fj0ldi simtala a dag er harðkóðað sem 100

	ID = 0
	simtalinn_sek = 0
	simtol=[]
	for i in millitimi:
		simtalinn_sek = simtalinn_sek + millitimi[i] #halda utan um hvern símtal kom inn.
		simtal = nytt_simtal(ID, simtalinn_sek) #býr til dict fyrir símtal
		ID += 1 
		simtol.append(simtal) #búa til lista með öllum símtölunum
	return simtol;

def UpdateStatusOfPhoneCall():
	for i in ListOfPhoneCalls:
		if i["simtal_inn"] <= clock:
			i["status"] = "B"

def UpdateStatusOfEmployee()
	for i in ListOfStaff:
		if i[""]
#============================================================================
'''
def find_staff():
	"""
	þessi forlykkja fer í gegnum listan staff finnur dict fyrir einn starfsmann og skilar id fyrir starfsmann ef hann er laus
   	"""
	for i in ListOfStaff: 
		if i['Idel'] == 'yes':
			return(i['StaffId']);
		else:
			return(); #allir starfsmennuppteknir hvað þá ?

def find_next_phonecall(): 
#þessi forlykkja fer í gegnum listan simtol finnur dict fyrir eitt simtal og skilar id fyrir símtali ef simtal er í bið
   for x in enumerate(simtol):#kalla í listan af símtölunum
      
      if x.get('stada') =='waiting':
         return(x.get('ID'))# skilar simtal id
      else:
         return() # ekkert símtal í bið hvað þá ?

def set_employer_call():
   next_phonecall=find_next_phonecall(simtol)
   free_staff=find_staff(ListOfStaff)
   []
'''
#------------------------------------------------------------------------------------------------------------------------------------

ListOfStaff = StartDay()
ListOfPhoneCalls = GeneratePhoneCalls()

while clock <= GeneralInfo["CloseAt"]:

	UpdateStatusOfPhoneCall()
	UpdateClock(1)

