#!/usr/bin/env python3
import simulator
import csv


def CollectList(filename, day):
	lambdas = []

	file = open(filename,"r")
	reader = csv.reader(file)
	data = []
	for row in reader:
		data.append(row)
	thelam = ''


	for i in range (0,len(data)):
		dagur = data[i][0]
		if dagur == day:
			thelam = float(data[i][1].split('|')[1].strip())
			thelam = thelam/3600
			timi = float(data[i][1].split('|')[0].strip().replace(')',''))
			timi = timi*3600
			lambdas.append( {'time': timi, 'lam': thelam} )

	file.close()
	return lambdas




