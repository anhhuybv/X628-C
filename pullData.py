from time import sleep
from datetime import datetime, date, time
import psycopg2
from zk import ZK, const

# Connect to database
cur = None
try:
    connectDB = psycopg2.connect(database="postgres", user = "postgres", password = "123", host = "localhost", port = "5432")
    print "Connected database successfully"
    cur = connectDB.cursor()
except:
    print "Unable to connect to the database"

# Connect to device X628
zk = ZK('192.168.1.200', port=4370, timeout=5)
conncetX628 = zk.connect()
if zk.is_connect:
    print "Connected to device\nStart pulling data"
else:
    print "No connected to devive"

statusPull = True

# Pull data from device X628
while statusPull:
    users = conncetX628.get_users()
    # Delete data table
    cur.execute("DELETE FROM usertable")
    # Pull data to table
    for user in users:
        print '  UID        : {}'.format(user.uid)
        print '  User  ID   : {}'.format(user.user_id)
        print '  Name       : {}'.format(user.name)
        print '  Privilege  : {}'.format(user.privilege)
        print '  Password   : {}'.format(user.password)
        print '  Group ID   : {}'.format(user.group_id)
        namedict = ({"uid": format(user.uid), "id": format(user.user_id),"name": format(user.name),"privilege": format(user.privilege),
                     "password": format(user.password),"groupid": format(user.group_id)})
        cur.execute("INSERT INTO usertable (uid,id,name,privilege,password,groupid) VALUES (%(uid)s, %(id)s, %(name)s, %(privilege)s, %(password)s, %(groupid)s)", namedict)
        #cur.executemany("""INSERT INTO bar(first_name,last_name) VALUES (%(first_name)s, %(last_name)s)""", namedict)
        #connectDB.commit()
                #     timerequest = datetime.combine(date.min, lattendance[2].time())
                #     timein = datetime.combine(date.min, datetime.time(datetime.strptime('09:00:00', '%H:%M:%S')))
                #     timedefault1 = datetime.combine(date.min, datetime.time(datetime.strptime('09:00:00', '%H:%M:%S')))
                #     timedefault2 = datetime.combine(date.min, datetime.time(datetime.strptime('11:45:00', '%H:%M:%S')))
                #     timedefault3 = datetime.combine(date.min, datetime.time(datetime.strptime('14:00:00', '%H:%M:%S')))
                #     timedefault4 = datetime.combine(date.min, datetime.time(datetime.strptime('17:45:00', '%H:%M:%S')))
                #     timedefault5 = datetime.combine(date.min, datetime.time(datetime.strptime('03:00:00', '%H:%M:%S')))
                #     timedefault6 = datetime.combine(date.min, datetime.time(datetime.strptime('08:00:00', '%H:%M:%S')))
                #     timelate = datetime.time(datetime.strptime('00:00:00', '%H:%M:%S'))
                #     if (timedefault1 < timerequest < timedefault2):
                #         timelate = timerequest - timedefault1
                #     elif (timedefault3 < timerequest < timedefault4):
                #         timelate = timerequest - timedefault3

                    # cur.execute("SELECT id,timein,timeout from datatable WHERE (id,date) = " + "(" + `lattendance[0]` + "," + `str(lattendance[2].date())` + ")" )
                    # rowss = cur.fetchall()
                    # if (rowss != []):
                    #     halftime = time(3,00,00)
                    #     fulltime = time(8,00,00)
                    #     timesub = timerequest - datetime.combine(date.min, rowss[0][1])
                    #     f = (datetime.min + timesub).time()
                    #     point = 1
                    #     if f >= fulltime:
                    #         point = 1000000
                    #     elif fulltime > f >= halftime:
                    #         point = 1000
                    #     cur.execute("UPDATE datatable set (point,timeout) = (" +  `point` + "," + `str(timerequest)` + ") where (id,date) = " + "(" + `lattendance[0]` + "," + `str(lattendance[2].date())` + ")" )
                    #     connectDB.commit()
                    #     zk.clearAttendance()
                    # elif (rowss == []):
                    #     cur.execute("INSERT INTO datatable (id,name,DATE,point,timein,STATE,timelate) VALUES \
                    #     ("+  `lattendance[0]` + "," + `data_user[uid][1]` + "," + `str(lattendance[2].date())` + "," + `1` + ","+ \
                    #     `str(timerequest)` + "," + `str(lattendance[1])` + "," + `str(timelate)` +")")
                    #     connectDB.commit()
                    #     zk.clearAttendance()
    statusPull = False