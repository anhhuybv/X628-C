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

if True:
    temp = zkt.get_users()
    for i in temp:
        print(i.uid , i.user_id , i.name)