data = [line.strip() for line in open("result_average_millikomutimi_phour.txt", 'r')]
data = list(filter(lambda x:x != "", data))

L = range(len(data))
L = L[0::4]
for i in L:
	if data[i][11:14] == " 9)":
		print(data[i][11:14])
		data[i][11:14] =data[i][11:14]+" 09"
		print(data[i][11:14])
	

with open("MedaltalPerHour.csv","wt") as myfile:
	for i in L:
		myfile.write(data[i][7:14])
		#myfile.write(data[i][12:14])
		myfile.write('|')
		myfile.write(data[i+2])
		myfile.write('\n')

myfile.close