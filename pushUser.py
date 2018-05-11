import sys

sys.path.append("zklib")

import psycopg2, time

from zklib import zklib, zkconst,zkdevice
from zk import ZK

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
zkt = ZK('192.168.1.201', port=4370, timeout=5)
zkt.connect()
conZkt = zkt.is_connect

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
                zkt.set_user(uid=int(i[0]),name=i[2],privilege=1,password=str(1),group_id=str(1),user_id=str(i[1]))
            print("Pushing user is done")
        elif data.__len__() == 0:
            print("No user to pushing")
    else:
        print("Can not pushing user")
        print("Can not connect device")
    time.sleep(60)