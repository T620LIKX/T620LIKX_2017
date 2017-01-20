import numpy as np
import pandas as pd
import matplotlib.pylab as plt 
from sqlalchemy import create_engine
#Línur sem eru kommentaðar út innihalda kóða þar sem hver notandi þarf að gera breytingar
Data = pd.DataFrame()
#Data=pd.read_excel('C:\data\DataA.xlsx', skiprows=3,parse_cols='B:P')  #skrá sett inn í pandas dataframe - athugið slóð að skrá er breytileg

#Breytum íslenskum stöfum í dálka nöfnum og línubil tekinn út 
cols = Data.columns
cols = cols.map(lambda x: x.replace(' ', '_').replace('á','a').replace('Á','A').replace('ð','d').replace('í','i').replace('ö','o').replace('ú','u'))
Data.columns = cols
#íslenskir stafir teknir úr daga dálki
dag = Data.Dagur
dag =dag.map(lambda x: x.replace('ö','o').replace('á','a').replace('ð','d'))
Data.Dagur=dag
print(Data)
#engine = create_engine('postgresql://USERNAME:PASSWORD@localhost:5432/DATABASE') # býr til töflu með öllum gögnunum í postres þarf að setja inn notendanafn, password og nafn á gagnagrunni
#Data.to_sql('data', engine)