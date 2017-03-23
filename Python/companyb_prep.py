from sqlalchemy import Table, MetaData, create_engine
import datetime
import calendar
import numpy as np
import pandas as pd
engine = create_engine("postgresql://postgres:st36543654@localhost/likanx") # breyta hjá hverjum
    
Table=pd.read_sql_table('callcenter_b',engine)

timestamp=Table.ix[:,0]
## búum til nýtt data frame sem er innihaldið af deginum þurfum að púsla því saman við hitt
gogn=pd.DataFrame({"ar": timestamp.dt.year,
              "manudur": timestamp.dt.month,
            #  "dagsetning": timestamp.dt.day,
              "klukkustund": timestamp.dt.hour,
            #  "dayofyear": timestamp.dt.dayofyear,
              "week": timestamp.dt.week,
              "vikunumer": timestamp.dt.weekofyear,
              "dayofweek": timestamp.dt.dayofweek,
              "weekday": timestamp.dt.weekday,
            #  "quarter": timestamp.dt.quarter,
             })
# print(gogn)
# print(Table)
# print(type(gogn))
# print(type(Table))

# það þarf að skoða þetta, misssum ehv tölur 
bigdata=Table.append(gogn)
a=Table[Table['call_center_name'].str.contains('1|2')]
b=Table[Table['call_center_name'].str.contains('Net|TV')]
total=Table['calls_queued'].sum()
nettotal=a['calls_queued'].sum()
tvtotal=b['calls_queued'].sum()
netpri=a[a['call_center_name'].str.contains('Forgangur')]
tvpri=b[b['call_center_name'].str.contains('Forgangur')]
netpri=netpri['calls_queued'].sum()
tvpri=tvpri['calls_queued'].sum()
print(nettotal)
print(tvtotal)

print(netpri)
print(tvpri)

print('hlutfall forgangs símtala hjá verum 1 & 2')
print(netpri/nettotal)
print('hlutfall forgagns símtala hjá verum 3 & 4')
print(tvpri/tvtotal)