import os
import threading
# dbPath = './DbFuncs/sql.db'

# itemLength = 220


# convert image to blob data
def convert_to_blod_data(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

# write 
def write_to_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

DBLOCK_ADS = 0
DBLOCK_MACHINE = 1
DBLOCK_PRODUCT = 2
dbLockList = []
def initDBLock():
    global dbLockList
    dbLockList.append(threading.Lock())
    dbLockList.append(threading.Lock())
    dbLockList.append(threading.Lock())

def getDBLock(db):
    return dbLockList[db]

THREAD_INIT = 0
THREAD_RUNNING = 1
THREAD_STOPPING = 2
THREAD_FINISHED = 3

threadStatus = []
def initThreadLock():
    global threadStatus
    threadStatus.append(THREAD_INIT)

def setThreadStatus(status):
    global threadStatus
    threadStatus[0] = status

def getThreadStatus():
    global threadStatus
    return threadStatus[0]

