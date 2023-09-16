import os
# dbPath = './DbFuncs/sql.db'

# screenX = 600
# screenY = 900

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

lockList = []
def initLock(lock):
    global lockList
    lockList.append(lock)
def initThreadLock(lock):
    global lockList
    lockList.append(lock)

