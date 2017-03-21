from sqlalchemy import Table, MetaData, create_engine
import datetime
import calendar
import numpy as np
import pandas as pd
engine = create_engine("postgresql://postgres:lukas@localhost/likanx") # breyta hjá hverjum
    
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
print(bigdata)

