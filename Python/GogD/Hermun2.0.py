import numpy as np
import pandas as pd
import matplotlib.pylab as plt 
import scipy.optimize as sci
import math

#======================================================================
GeneralInfo = {"OpenAt":  0, "CloseAt": 500, "NumberOfStaff": 1} #Note: seinna meir væri hægt að gera þetta að falli með user interface-i
EventList = [] #Gæti verið óþarfi að declarea hann hérna. Tékka á því.
clock = 0

def Start_Day():
	"""
	Fall sem "opnar" innhringiverið með þvi að senda inn tvö event um opnun og lokun 
	"""
	
	global clock
	clock = 0 #Núllstillir klukkuna í upphafi dags. Just in case.
	
	At_Event('opens', GeneralInfo['OpenAt'])
	At_Event('closes', GeneralInfo['CloseAt'])	

	return;


def Set_Staff():
	"""
	Fall sem upphafsstillir þá starfsmenn sem eru á vakt þennan daginn og setur það inn sem event.
	WorkingOn: Id á símtali ef er að þjónusta
			   idle ef laus   

	IsWorking: yes ef starfsmaðurinn er á vakt
			   No ef starfsmaðurinn er búinn að vakt eða ekki byrjaður.

	Note: Hérna væri hægt að bæta við kaffipásum starfsmannsins, þynnkustuðul o.s.fr.
	"""

	ListOfStaff = []
	for i in range(GeneralInfo["NumberOfStaff"]):
		#begin = int(input('Staff ' + str(i+1) + ' begins: '))
		#end = int(input('Staff ' + str(i+1) + ' ends: '))
		begin = 0 #harðkóða upphafs og endatíma fyrir starfsmanninn til að byrja með.
		end = 500
		staffId = {"Type": "Staff", "StaffId": i, "Begins": begin, "Ends": end, "WorkinOn": "idle", 'IsWorking': "no"}
		ListOfStaff.append(staffId)

	At_Event("Staff", ListOfStaff) 

	return;


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
	simtal = {"ID": ID, 'status': "A", 'Lengd_Simtals':lengdSimtal, 'Bidtimi': "NAN", 'Simtal_Inn': simtalInn, 'Simtal_Lokid': "NAN"}
	return (simtal);


def At_Event(EventType, time):
	'''
	Event listi.

	Innhringiver opnar: 		opens
	InnhringiVer Lokar:			closes
	StarfsmaðurHefurVinnu:		starts
	StarfsmaðurFerHeim:			ends
	SimtalKemurInn:				callInn
	SimtaliLykur:				callEnds

	'''

	'''
	if EventType == 'opens'

	elif EventType == 'closes'
			EventList.append({"Type": EventType, "Time": time})
	elif EventType == 'starts'

	elif EventType == 'ends'

	elif EventType == 'callInn'

	elif EventType == 'callEnds'

	else
	'''

	EventList.sort(key = {lambda x:x["Time"]}) #Major key. Fall sem raðar listanum yfir í evnets í rétta tíma röð þannig að Eventlist[0] er alltaf næst hluturinn í réttri tímaröð

	
#----------------------------------main----------------------------------------------


while clock <= GeneralInfo["CloseAt"]:
	e = EventList[0]
	del EventList[0]
	clock = e["Time"]

'''
	if e["Type"] == eitthvad
		
	elif e["Type"] == eitthvad

	elif e["Type"] == eitthvad

	elif e["Type"] == eitthvad

	else

'''