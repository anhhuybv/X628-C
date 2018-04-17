import sys

sys.path.append("zklib")

import psycopg2, time

from zklib import zklib, zkconst,zkdevice
from zk import ZK, const

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

conn = None
zkt = ZK('192.168.1.201', port=4370, timeout=5)
conn = zkt.connect().is_connect
print(conn)
# Pull data from device X628
if True:
    # if(statusConnect):
    #     cur.execute("SELECT uid,iduser,name FROM usertable")
    #     data = cur.fetchall()
    #     for i in data:
    #         zk.setUser(uid=int(i[0]), userid=str(i[1]), name=str(i[2]), password='1', role=zkconst.LEVEL_USER)
    #     print("Pushing user is done")
    # else:
    #     print("Can not pushing user")
    #     print("Can not connect device")
    # zkt.delete_user(uid = int(12))
    #
    # users = zk.getUser()
    #
    # for uid in users:
    #     print ('  UID        : {}'.format(uid))
    #     print ('  User  ID   : {}'.format(users[uid][0]))
    #     print ('  Name       : {}'.format(users[uid][1]))
    #     print ('  Privilege  : {}'.format(users[uid][2]))
    #     print ('  Password   : {}'.format(users[uid][3]))
    arrayData = []
    cur.execute("SELECT * FROM timetable")
    data = cur.fetchall()
    for i in data:
        arrayData.append(i)
        print(i)

    #     dataUsers = ({"uid": format(uid), "iduser": format(users[uid][0]), "name": format(users[uid][1]), "privilege": format(1), "password": format(1)})
    #     cur.execute("INSERT INTO usertable (uid,iduser,name,privilege,password) VALUES (%(uid)s, %(iduser)s, %(name)s, %(privilege)s, %(password)s)", dataUsers)
    # connectDB.commit()
    # time.sleep(60)