import mysql.connector

def con():
      
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="P@ssword",
  database="webstylebid"
  )
  return mydb

