# Þetta skjal býr til SQL skipanir sem að reiknar meðalmillikomutíðni (lamdba) á hverjum degi á tilteknum tímabilum
# Þetta er hugsað til að reikna lambda fyrir Poisson dreifingu (spálíkan fyrir fjölda símtala á tímabili)
# Keyrið þennan kóða í terminal til að búa til textaskránan SQL_average.txt sem inniheldur SQL skipanirnar
# Keyrið svo í terminal kóðann sem er kommentaður út neðst til að fá niðurstöður úr SQL fyrirspurnunum.

# Við brutum þetta niður á hvern dag og hugsuðum þetta sem tímabilin 9-12, 13-17 og 18-21. Það er ekki mikið mál að breyta tímanum, t.d. ef að við viljum fá niður á klukkustund.

import numpy as np
filename = 'SQL_average_phour.txt'

tofile = open(filename, 'w')

days = ['man','tri','mid','fim','fos','lau','sun']

hours = range(9,21)
print(hours)
for hour in hours :
	print(hour)

for day in days:
	counter = 0
	for hour in hours:
		print('select avg(d.simtol_inn) as "QUERY (%s, %s)" from data d where' %(day,hour))
		tofile.write('select avg(d.simtol_inn) as "QUERY (%s, %s)" from data d where\n' %(day,hour))
		print('d.klukkustund = %s ' %hour, end="")
		tofile.write('d.klukkustund = %s ' %hour)
		print('group by d.dagur\nhaving d.dagur = \'%s\'; \n' %day)
		tofile.write('group by d.dagur\nhaving d.dagur = \'%s\'; \n\n' %day)
		counter += 1
tofile.close()

# Til að fá SQL niðurstöður (geymdar í SQL_average_phour.txt) í textaskrá sem heitir result_average_millikomutimi.txt keyri ég þessa línu í terminal:
# Ath: databaseið mitt heitir likanx svo að þessvegna stendur -dlikanx (með d fyrir framan)
# psql -U gunnargylfason -f SQL_average_phour.txt -dlikanx -q > result_average_millikomutimi_phour.txt;
