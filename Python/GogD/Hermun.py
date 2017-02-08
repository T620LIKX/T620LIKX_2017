import numpy as np
import pandas as pd
import matplotlib.pylab as plt 
import scipy.optimize as sci
import math

#======================================================================
GeneralInfo = {"OpenAt":  0, "CloseAt": 500, "NumberOfStaff": 1} #Note: seinna meir væri hægt að gera þetta að falli með user interface-i

clock = 0

def UpdateClock(n):
	global clock
	clock = clock + n

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

		staffId = "StaffID" + str(i+1)
		staffId = {"StaffId": staffId,"Begins": begin, "Ends": end, "WorkinOn": "idle", 'IsWorking': "no"}
		ListOfStaff.append(staffId)
	return ListOfStaff;

def nytt_simtal(id,simtalInn):
	"""
	Býr til nýtt símtal og upphafstillir breytur.
	Breytan status heldur utan um í hvaða fasa símtalið er.
	A: Er ekki búinn að hringja.
	B: Er í röð.
	C: Er í þjónustu.
	D: Er búinn að fá þjónustu.
	"""

	lengdSimtal= int(np.random.exponential(scale=100, size=None)) # beta =100 parameter fyrir exponential 1/landa
	ID = "CallID" + str(id+1)
	simtal = {"ID": ID, 'status': "A", 'Lengd_Simtals':lengdSimtal, 'Bidtimi': "NAN", 'Simtal_Inn': simtalInn, 'Simtal_Lokid': "NAN"}
	return (simtal);

def GeneratePhoneCalls():
	'''
	Þetta fall býr til lista af dictonarys af símtölum yfir daginn með því að nota fallið nytt_simtal.
	Note: Hérna væri hægt að útfæra frekari líkindadreifinu á símtölinn þegar það er fyrir hendi
	'''

	millitimi = np.random.poisson(lam=5.0, size=100) #Fjldi simtala a dag er harðkóðað sem 100

	ID = 0
	simtalinn_sek = 0
	simtol=[]
	for i in millitimi:
		simtalinn_sek = simtalinn_sek + millitimi[i] 
		simtal = nytt_simtal(ID, simtalinn_sek) 
		ID += 1 
		simtol.append(simtal) 
	return simtol;


def UpdateStatusOfPhoneCall():
	'''
	Þetta fall athugar hvort einhver sé búinn að slá á þráðinn á innhringiverið og uppfærir þá stöðuna á því símtali.
	'''

	for i in ListOfPhoneCalls:
		if i['Simtal_Inn'] <= clock:
			i["status"] = "B"


def UpdateStatusOffStaff():
	'''
	Þetta fall athugar hvort starfsmaður á að vera mættur í vinnuna og ef svo er þá uppfærir það stöðuna á honum.
	Sömuleiðis athuga það ef starfsmaður er búinn á vaktinni sinni.

	Ef starfsmaðurinn er að vinna þá athugar fallið hvort starfsmaðurinn sé að vinna í símtali. Ef það er komin tími á að símtalinu ljúki þá
	uppfærir falli það með því að setja starfsmanninn í status og biður þá annað fall að uppfæra stöðuna á símtalinu.
	
	Note: Ef starfsmaður er í símtali þegar vaktin er búinn þá þarf að útfæra eitthva hérna svo hann ljúki við það áður en hann pakkar saman.
	'''

	for i in ListOfStaff:
		if(i["IsWorking"] == "no" and i["Begins"] >= clock):
			i["IsWorking"] == "yes"
		if(i["IsWorking"] == "yes" and i["Ends"] <= clock):
			i["IsWorking"] == "no"

		#if i["IsWorking"] == "yes" and i["WorkingOn"] != "idle": #Þetta is segð gæti mögulega átt heima undir fyrstu if statementinun í þessu falli.


def find_next_phonecall(): 
	'''
	Þetta fall finnur næsta lausa símtal og skila id-inu á því til baka.
	Ef ekkert símtal er í bið þá skilar það villu meldingunni NAN

	Note: Hér væri hægt að útfæra frekari kóða ef við viljum taka tillits til callback
	'''

	for i in ListOfPhoneCalls:
		if i['status'] == 'B': #Hugsanlegt error, ef listinn er ekki alltaf raðaður eftir ID
			return(i["ID"]);
	return('NAN');

def find_next_Idle_staff(IdOfPhoneCall):
	"""
	Þetta fall fer í gegnum lista af starfsmönnum og athugar fyrst hvort starfsmaðurinn er á vakt og síðan
	það finnur ef starfsmaðurinn er laus. Ef það er laus starfsmaður þá skráir fallið símtalið á starfsmanninn.
	Það kallar´ síðan á set_end_time_of_phonecall sem uppfærir símtalið.

	ATH!! Ef það er enginn starfsmaður laus. Hvað þá? Verðum að passa að símtalið sem fór inn glatist ekki? Kannski returna id-inu af

	Note: Ef allir starfsmenn eru lausir þá fær fyrsti starfsmaðurinn alltaf verkefnið. Passa það þegar við skoðum tölfræðina
   	"""
	for i in ListOfStaff: 
		if i["IsWorking"] == "yes":
			if i["WorkinOn"] == 'idel':
				i["WorkinOn"] = IdOfPhoneCall
				return;
			else:
				return;
				#print("Feit villumelding i find_next_Idle_staff. Enginn starfsmadur laus")
		else:
			return;
			#print("Feit villumelding i find_next_Idle_staff. Enginn starfsmadur a vakt")


#--------------------------------------------------------------------------------------

#Föll sem eru ekki komin með hlutverk

def set_wait_time_of_phonecall(IdOfPhoneCall, lengBid):
	"""
	Fall sem uppfærir stöðuna á því hvenær símtalinu á að vera lokið. 

	Mætti kannski útfæra það þannig að það uppfærir statusinn á símtalinu líka. Þ.e.a.s færi símtalið úr fasa B yfir í C
	"""
	for i in ListOfPhoneCalls:
		if i["ID"] == IdOfPhoneCall:
			i["Bidtimi"] = lengBid
			return;
	print("Villumelding i set_wait_time_of_phonecall") #Ætti aldrei að geta komist hingað.


def set_end_time_of_phonecall(IdOfPhoneCall):
	"""
	Fall sem uppfærir stöðuna á því hvenær símtalinu á að vera lokið. 
	"""
	for i in ListOfPhoneCalls:
		if i["ID"] == IdOfPhoneCall:
				i["Simtal_Lokid"] = i["Simtal_Inn"] + i["Bidtimi"] + i["Lengd_Simtals"]
				return;
	print("Villumelding i set_end_time_of_phonecall") #Ætti aldrei að geta komist hingað.

'''
Föll sem eru ekki útfærð

Fall eða if setning einhversstaðar sem uppfærir símtalið þannig það sé komið úr fasa B yfir C og uppfærir biðtímann. Getur notað set_wait_time_of_phonecall

Fall sem athuga hvort starfsmaður sé búinn með símtalið og setur starfsmanninn þá sem idel. Það mætti kannski bara fara inn í fallið UpdateStatusOfStaff



'''


#------------------------------------------------------------------------------------------------------------------------------------

ListOfStaff = StartDay()
ListOfPhoneCalls = GeneratePhoneCalls()

for i in ListOfPhoneCalls:
	print(i)


while clock <= GeneralInfo["CloseAt"]:
	print(clock)
	UpdateStatusOffStaff()
	UpdateStatusOfPhoneCall()

	if find_next_phonecall() != 'NAN':
		find_next_Idle_staff(find_next_phonecall())

	UpdateClock(1)


for i in ListOfPhoneCalls:
	print(i)

