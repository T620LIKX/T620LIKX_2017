import numpy as np
import pandas as pd
import matplotlib.pylab as plt 
import scipy.optimize as sci
import math

#======================================================================
GeneralInfo = {"OpenAt":  0, "CloseAt": 500, "NumberOfStaff": 1} #Note: seinna meir væri hægt að gera þetta að falli með user interface-i
EventList = [] #Gæti verið óþarfi að declarea hann hérna. Tékka á því.
ListOfStaff = [] #Gæti verið óþarfi að declarea hann hérna, geri það nú þegar í fallinu setstaff

clock = 0

def Start_Day():
	"""
	Fall sem "opnar" innhringiverið með þvi að senda inn tvö event um opnun og lokun 
	"""
	
	global clock
	clock = 0 #Núllstillir klukkuna í upphafi dags. Just in case.
	

	At_Event('opens', GeneralInfo['OpenAt'], 0, 0)
	At_Event('closes', GeneralInfo['CloseAt'], 0, 0)

	return;

def At_Event(EventType, time, id, other):
	'''
	Event listi. Hér  bætum við eventum inn á listann

	Innhringiver opnar: 		opens
	InnhringiVer Lokar:			closes
	StarfsmaðurHefurVinnu:		starts
	StarfsmaðurFerHeim:			ends
	SimtalKemurInn:				callInn 		<--- nytt_simtal
	SimtaliLykur:				callEnds 
	Tékka á stöðunni:			checkStatus     <--- Þetta fall er keyrt eftir hvert skipti sem starfsmaður klárar símtal "í while lykkjunni" og þá tékkar það aftur í event list hvort það sé símtal í röðinni og ef svo er þá skráir það símtalið á starfsmanninn.

	'''

	if EventType == 'opens' or EventType == 'closes':
		EventList.append({"Type": EventType, "Time": time})
	
	elif EventType == "starts" or EventType == 'ends':
		EventList.append({'Type': EventType, 'Time': time, 'Id': id})

	elif EventType == "callInn":
		EventList.append({"Type": EventType, "Time": time, 'Id': id, "CallLength": other})
	
	elif EventType == "callEnds":
		Eventlist.append({"Type": EventType, "Time": time, 'Id': id})

	'''
	elif EventType == 'callEnds'
	'''
	
	EventList.sort(key=lambda x: x["Time"]) #Major key. Fall sem raðar listanum yfir í evnets í rétta tíma röð þannig að Eventlist[0] er alltaf næst hluturinn í réttri tímaröð
	return;

def Set_Staff():
	"""
	Fall sem upphafsstillir þá starfsmenn sem eru á vakt þennan daginn og setur það inn sem event.
	WorkingOn: Id á símtali ef er að þjónusta
			   idle ef laus   

	Note: Hérna væri hægt að bæta við kaffipásum starfsmannsins, þynnkustuðul o.s.fr.
	"""

	for i in range(GeneralInfo["NumberOfStaff"]):
		#begin = int(input('Staff ' + str(i+1) + ' begins: '))
		#end = int(input('Staff ' + str(i+1) + ' ends: '))
		begin = 0 #harðkóða upphafs og endatíma fyrir starfsmanninn til að byrja með.
		end = 450
		staffId = {"Type": "Staff", "StaffId": i}
		#staffId = {"Type": "Staff", "StaffId": i, "Began": 0, "Ended": 0, "WorkinOn": "idle"}
		ListOfStaff.append(staffId)
		At_Event("starts", begin, i, 0)
		At_Event("ends", end, i, 0)

	return;

def find_staff(id):
	for i in ListOfStaff:
		if i["StaffId"] == id:
			return i;


def GeneratePhoneCalls():
	'''
	Þetta fall býr til lista af dictonarys af símtölum yfir daginn með því að nota fallið nytt_simtal.
	Note: Hérna væri hægt að útfæra frekari líkindadreifinu á símtölinn þegar það er fyrir hendi
	'''

	millitimi = np.random.poisson(lam=5.0, size=100) #Fjldi simtala a dag er harðkóðað sem 100

	ID = 0
	simtalinn_sek = 0
	for i in millitimi:
		simtalinn_sek = simtalinn_sek + millitimi[i]
		lengdSimtal= int(np.random.exponential(scale=100, size=None))
		At_Event("callInn", simtalinn_sek, ID, lengdSimtal)
		ID += 1 
	return;


#----------------------------------main----------------------------------------------

Start_Day()
Set_Staff()
GeneratePhoneCalls() #Væri mjög töff ef þetta fall yrði meira discrete

while clock < GeneralInfo["CloseAt"]:
	e = EventList[0]
	del EventList[0]

	clock = e["Time"]


	if e["Type"] == "opnes":
		clock = e['Time']

	elif e["Type"] == "closes":
		clock == e['Time']
	elif e["Type"] == 'starts':
		'''
		Byrjar að uppfæra breytuna um starfsmanninn, þ.e.a.s 
		x1. finna starfsmann í listofstaff
		x2. Setja inn key i dictid sem er "began": e['Time']
		x3. Setja inn key sem er "WorkingOn": "idle"
		4. Tekka hvort starfsmadur getur svarad simtali
		'''	
		find_staff(e["Id"]).update({"Began": e["Time"], "WorkingOn": "idle"})
		clock == e['Time']


	elif e["Type"] == 'ends':
		find_staff(e["Id"]).update({"Ended": e["Time"]})
		clock == e['Time']

	elif e["Type"] == 'callInn':
		e["Status"] = 'innLine'
		clock == e['Time']

	elif e["Type"] == "callEnds":
		e["Status"] = "callHasEnded"
		clock == e['Time']
				
	print(clock)

'''
	if e["Type"] == eitthvad

		gera eitthvað. Gætum verið með skjal/lista um allar niðurstöður og þetta fall gæti uppfært það.
		a

	elif e["Type"] == eitthvad

	elif e["Type"] == eitthvad

	elif e["Type"] == eitthvad

	else

'''	