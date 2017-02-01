import numpy as np
import pandas as pd
import matplotlib.pylab as plt 
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
#Línur sem eru kommentaðar út innihalda kóða þar sem hver notandi þarf að gera breytingar
#Function that connects to database
def db_connect(host, username, pw, dbname):
	#Check if program will connect to host or database 
	
	if dbname == 'NULL':
		conn_string = "host='{}' user='{}' password='{}'".format(host, username, pw) 
	else:
		conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, username, pw)

	conn = psycopg2.connect(conn_string)
	conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cursor = conn.cursor()
	print("Connected!\n")

	return (cursor, conn)
#Function that closes connection
def connection_close(cursor, conn):
	conn.commit() #Commit pending transactions in DB
	cursor.close() #Close current cursor
	conn.close() #Close connection

#Make connection string to connect to database
host = 'localhost'
username = 'postgres'
pw = 'lukas'
#Connect to postgres 
cursor, conn = db_connect(host, username, pw, dbname = 'NULL')
connection_close(cursor, conn)
#Connect to database 
cursor, conn = db_connect(host, username, pw, dbname = 'likanx')
SQLCommand = ("SELECT manudur,vikunumer,dagur,dagsetning,klukkustund,simtol_inn"
               " FROM data") 
gogn=[]
cursor.execute(SQLCommand)
# Using a while loop, taka allt í einu
row = cursor.fetchone()
while row is not None:
	gogn.append(row)
	row = cursor.fetchone()
	print(gogn)


# # taka eitt í einu
# cursor.execute("SELECT manudur" " FROM data") 
# manudur = cursor.fetchall()

# cursor.execute("SELECT vikunumer" " FROM data") 
# vika = cursor.fetchall()

# cursor.execute("SELECT dagur" " FROM data") 
# dagur = cursor.fetchall()

# cursor.execute("SELECT dagsetning" " FROM data") 
# dagsetning = cursor.fetchall()

# cursor.execute("SELECT klukkustund" " FROM data") 
# klukkustund = cursor.fetchall()

# cursor.execute("SELECT simtol_inn" " FROM data") 
# stimtol = cursor.fetchall()

connection_close(cursor, conn)