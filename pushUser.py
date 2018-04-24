import sys

sys.path.append("zklib")

import psycopg2, time

from zklib import zklib, zkconst,zkdevice

# Connect to database
connectDB = None
cur = None
try:
    connectDB = psycopg2.connect(database="postgres", user="postgres", password="123", host="127.0.0.1", port="5432")
    print ("Connected database successfully")
    cur = connectDB.cursor()
except:
    print ("Unable to connect to the database")

# Connect to device X628
zk = zklib.ZKLib("192.168.1.201", 4370)
statusConnect = zk.connect()
if statusConnect:
    print ("Connected to device")
else:
    print ("No connected to devive")

# Pull data from device X628
while True:
    if(statusConnect):
        cur.execute("SELECT uid,iduser,name FROM usertable")
        data = cur.fetchall()
        if data.__len__() != 0:
            for i in data:
                zk.setUser(uid=int(i[0]), userid=str(i[1]), name=str(i[2]), password='1', role=zkconst.LEVEL_USER)
            print("Pushing user is done")
        elif data.__len__() == 0:
            print("No user to pushing")
    else:
        print("Can not pushing user")
        print("Can not connect device")

    # users = zk.getUser()
    # for uid in users:
    #     print ('  UID        : {}'.format(uid))
    #     print ('  User  ID   : {}'.format(users[uid][0]))
    #     print ('  Name       : {}'.format(users[uid][1]))
    #     print ('  Privilege  : {}'.format(users[uid][2]))
    #     print ('  Password   : {}'.format(users[uid][3]))
    #     dataUsers = ({"uid": format(uid), "iduser": format(users[uid][0]), "name": format(users[uid][1]), "privilege": format(1), "password": format(1)})
    #     cur.execute("INSERT INTO usertable (uid,iduser,name,privilege,password) VALUES (%(uid)s, %(iduser)s, %(name)s, %(privilege)s, %(password)s)", dataUsers)
    # connectDB.commit()
    time.sleep(60)