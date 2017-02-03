data = [line.strip() for line in open("result_average_millikomutimi.txt", 'r')]
data = filter(lambda x:x != "(1 row)", data)
data = filter(lambda x:x != "", data)
data = list(filter(lambda x:x != "-------------------------------", data))

L = range(len(data))
L = L[0::2]
for i in L:
	data[i] = data[i][7:10]+data[i][13:15]
	data[i] = data[i].replace(" ","0")

with open("data.txt","wt") as myfile:
	for i in L:
		myfile.write(data[i])
		myfile.write('|')
		myfile.write(data[i+1])
		myfile.write('\n')

myfile.close