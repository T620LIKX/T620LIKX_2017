# Þetta skjal býr til SQL skipanir sem að reiknar meðalmillikomutíðni (lamdba) á hverjum degi á tilteknum tímabilum
# Þetta er hugsað til að reikna lambda fyrir Poisson dreifingu (spálíkan fyrir fjölda símtala á tímabili)
# Keyrið þennan kóða í terminal til að búa til textaskránan SQL_average.txt sem inniheldur SQL skipanirnar
# Keyrið svo í terminal kóðann sem er kommentaður út neðst til að fá niðurstöður úr SQL fyrirspurnunum.

# Við brutum þetta niður á hvern dag og hugsuðum þetta sem tímabilin 9-12, 13-17 og 18-21. Það er ekki mikið mál að breyta tímanum, t.d. ef að við viljum fá niður á klukkustund.

import numpy as np

tofile = open("SQL_average.txt", "w")

days = ['man','tri','mid','fim','fos','lau','sun']
hours = np.zeros((3,5)).astype(int)

# Hef 0 í lok línunnar þar sem að það hefur engin áhrif á SQL niðurstöðurnar og ég þarf að hafa arrayið í NxM stærð. (Þ.e. lenti í vandræðum með indexa ef að línurnar voru ekki jafn stórar)
hours[0,:] = ['9','10','11','12','0']
hours[1,:] = ['13','14','15','16','17']
hours[2,:] = ['18','19','20','21','0']

for day in days:
	counter = 0
	for hour in hours:
		#print('select avg(d.simtol_inn) as "QUERY (%s, %s)" from data d where' %(day,hours[counter,:]))
		tofile.write('select avg(d.simtol_inn) as "QUERY (%s, %s)" from data d where\n' %(day,hours[counter,:]))

		for i in range(4):
			#print('d.klukkustund = %s or ' %hour[i], end="")
			tofile.write('d.klukkustund = %s or ' %hour[i])

		#print('d.klukkustund = %s' %hour[4]) 
		tofile.write('d.klukkustund = %s\n' %hour[4])

		#print('group by d.dagur\nhaving d.dagur = \'%s\'; \n' %day)
		tofile.write('group by d.dagur\nhaving d.dagur = \'%s\'; \n\n' %day)
		counter += 1
tofile.close()

# Til að fá SQL niðurstöður (geymdar í SQL_average.txt) í textaskrá sem heitir result_average_millikomutimi.txt keyri ég þessa línu í terminal:
# Ath: databaseið mitt heitir likanx svo að þessvegna stendur -dlikanx (með d fyrir framan)
# psql -U gunnargylfason -f SQL_average.txt -dlikanx -q > result_average_millikomutimi.txt;