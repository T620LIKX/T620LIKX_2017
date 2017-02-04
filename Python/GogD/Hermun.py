clock = 0

def UpdateClock(n):
	global clock
	clock = clock + n

def MakeSimtal(id):
	key = "PhoneCallNr" + id
	key = {"LengdThjonustu": 5, "BidTimi": 0, "HvarErEg": "A"}
	return;

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
		staffId = {"StaffId": staffId,"Begins": begin, "Ends": end, "WorkinOn": "NAN", "Idel": "No"}
		ListOfStaff.append(staffId)
	return ListOfStaff;

ListOfStaff = StartDay()

print(ListOfStaff)
