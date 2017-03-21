from sqlalchemy import Table, MetaData, create_engine
import pandas
engine = create_engine("postgresql://postgres:st36543654@localhost/likanx") # breyta hjá hverjum
    
Table=pandas.read_sql_table('callcenter_b',engine)

print(Table['calls_queued'].sum())