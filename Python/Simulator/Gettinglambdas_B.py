import csv 

#filename = ['nytt_compb.csv']

#days = ['Monday','Tuesday','Wednesday','Thursday','Fridays','Saturday','Sunday']

def CollectList(filename,day):
	lambdas = []

	file = open(i,'r')
	reader = csv.reader(file)

	data = []

	for row in reader:
	data.append(row)
	file.close()

	call_center_type = ''
	for i in range(1,len(data)):

		call_center_type = data[i][0]
		weekday = data[i][1]
		hour = data[i][2]
		thelam = data[i][3]
		
		lambdas.append({'call_type': call_center_type, 'day':weekday, 'time':hour, 'lam':thelam})
	
	return lambdas

#for i in sorted(lambdas, key=lambda i:['day']):
#	print(i)

#print(lambdas)
