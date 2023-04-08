from db_connector import *

mydb = con()

mycursor = mydb.cursor()

def loginf(email,password):
    sql = "SELECT * from userdetails WHERE email=%s"
    val = (email,)
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    print(data)
    if data[0][2] == password:
        return True, data[0][0], data[0][3]
    else:
        return False, None, None