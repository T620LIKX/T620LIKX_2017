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

def StartDay(GeneralInfo):
	"""
	Fall sem "opnar" innhringiverið og biður notendan að stilla upp vaktaplaninu og skilar
	út lista af starfsmönnunum.
	"""
	
	global clock
	clock = 0 #Núllstillir klukkuna.

	ListOfStaff = []
	for i in range(GeneralInfo["NumberOfStaff"]):
		#begin = int(input('Staff ' + str(i+1) + ' begins: '))
		#end = int(input('Staff ' + str(i+1) + ' ends: '))

		begin = 0
		end = 1000
		staffId = "StaffId" + str(i+1)
		staffId = {"StaffId": staffId,"Begins": begin, "Ends": end, "WorkinOn": "NAN", "Idel": "No"}
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

	simtal = {"ID": ID, 'lengd_simtals':lengd_simtal,'status': "A", 'simtal_inn': simtal_inn, 'simtal_lokid': (simtal_inn+lengd_simtal)}
	return (simtal);

def GeneratePhoneCalls():

	millitimi = np.random.poisson(lam=5.0, size=100) #Fj0ldi simtala a dag er harðkóðað sem 100

	ID=0
	simtalinn_sek=0
	simtol=[]
	for i in millitimi:
		simtalinn_sek = simtalinn_sek + millitimi[i] #halda utan um hvern símtal kom inn.
		simtal = nytt_simtal(ID, simtalinn_sek) #býr til dict fyrir símtal
		ID += 1 
		simtol.append(simtal) #búa til lista með öllum símtölunum
	return simtol;

def UpdateStatus(ListOfPhoneCalls):
	for i in ListOfPhoneCalls:
		if i["simtal_inn"] <= clock:
			i["status"] = "B"

#------------------------------------------------------------------------------------------------------------------------------------

ListOfStaff = StartDay(GeneralInfo)

ListOfPhoneCalls = GeneratePhoneCalls()

#print(ListOfStaff)
#print(ListOfPhoneCalls)
#for i in ListOfPhoneCalls:
#	print(i)

UpdateStatus(ListOfPhoneCalls)
#print('l=========================')
#for i in ListOfPhoneCalls:
#	print(i)

