import numpy
import pandas as pd
import csv


class SettingsManager():
	
	def __init__(self):
		self.starttime = 0
		self.endtime = 43200
		self.number_of_workers = 1

		self.l = []
		self.lam = 0
		self.mu = 0.2
		self.rho = self.lam / self.mu

	def rand_phonecall_length(self):
		return numpy.random.exponential(1/self.mu)

	def MakeWeek(self):

		week = {}
		week['Day'] = {'Man':[], 'Tri':[],'Mid':[],'Fim':[],'Fos':[],'Lau':[], 'Sun':[] }

		for i in range (0,13):
			x = self.l[i]
			week['Day']['Man'].append(x)
		for i in range(13,26):
			x = self.l[i]
			week['Day']['Tri'].append(x)
		for i in range(26,39):
			x = self.l[i]
			week['Day']['Mid'].append(x)
		for i in range(39,52):
			x = self.l[i]
			week['Day']['Fim'].append(x)
		for i in range(52,65):
			x = self.l[i]
			week['Day']['Fos'].append(x)
		for i in range(65,78):
			x = self.l[i]
			week['Day']['Lau'].append(x)
		for i in range(78,91):
			x = self.l[i]
			week['Day']['Sun'].append(x)
		return week

	def rand_arrival_time(self, sec):

		l = self.CollectList('MedaltalPerHour.csv')
		week = self.MakeWeek()
		day = self.ReturnDays(sec)
		hour = self.ReturnHours(sec)


		for i in week:
			if (day < 1):
				self.lam = week['Day']['Man'][hour]
			elif (day >= 1 and day < 2):
				self.lam = week['Day']['Tri'][hour]
			elif (day >= 2 and day < 3):
				self.lam = week['Day']['Mid'][hour]
			elif (day >= 3 and day < 4):
				self.lam = week['Day']['Fim'][hour]
			elif (day >= 4 and day < 5):
				self.lam = week['Day']['Fos'][hour]
			elif (day >= 5 and day < 6):
				self.lam = week['Day']['Lau'][hour]
			elif (day >= 6 and day < 7):
				self.lam = week['Day']['Sun'][hour]

		self.lam = lam/3600
		return numpy.random.exponential(1/self.lam)

	def ReturnDays(self, sec):
		x = int(sec/(3600*12))
		if (x > 6):
			x = x%7
		return x


	def ReturnHours(self,sec):
		x = int(sec/3600)
		if (x > 12):
			x = x%12
		return x


	def CollectList(self, filename):
		file = open(filename,"r")
		reader = csv.reader(file)
		data = []
		for row in reader:
			data.append(row)
		thelam = ''
		for i in range (0,len(data)):
			thelam = float(data[i][1].split('|')[1].strip())
			self.l.append(thelam)
		file.close()
		return self.l


		

