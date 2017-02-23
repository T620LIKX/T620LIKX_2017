import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from sqlalchemy import create_engine
#Línur sem eru kommentaðar út innihalda kóða þar sem hver notandi þarf að gera breytingar
Data = pd.DataFrame()
Data=pd.read_excel('Háskólaverkefni - upplýsignar fyrir call center.xlsx', skiprows=3,parse_cols='B:P')  #skrá sett inn í pandas dataframe - athugið slóð að skrá er breytileg

#Breytum íslenskum stöfum í dálka nöfnum og línubil tekinn út
cols = Data.columns
cols = cols.map(lambda x: x.replace(' ', '_').replace('á','a').replace('Á','a').replace('ð','d').replace('í','i').replace('ö','o').replace('ú','u').lower())
Data.columns = cols
#íslenskir stafir teknir úr daga dálki
dag = Data.dagur
dag = dag.map(lambda x: x.replace('ö','o').replace('á','a').replace('ð','d').replace('þ','t'))
Data.dagur = dag
#print(Data)
engine = create_engine('postgresql://postgres:postgres@localhost:5432/likanx') # býr til töflu með öllum gögnunum í postres þarf að setja inn notendanafn, password og nafn á gagnagrunni
Data.to_sql('callcenter_a', engine)