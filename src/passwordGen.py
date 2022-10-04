import secrets
import string
import base64

# secure random string
secure_str = ''.join((secrets.choice(string.ascii_letters) for i in range(8)))
print(secure_str)
# Output QQkABLyK

# secure password
password = ''.join((secrets.choice(string.ascii_letters +
                                   string.digits + string.punctuation) for i in range(8)))
print(password)


message = password
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

print("base64 encode: %s" % base64_message)

base64_bytes = base64_message.encode('ascii')
message_bytes = base64.b64decode(base64_bytes)
message = message_bytes.decode('ascii')

print(message)


def getRandomPasswd(pwdlength=8):
    password = ''.join((secrets.choice(string.ascii_lowercase + string.ascii_uppercase +
                                       string.digits + string.punctuation) for i in range(pwdlength)))
    passwordBytes = password.encode('ascii')
    base64_bytes = base64.b64encode(passwordBytes)
    passwordMsg = base64_bytes.decode('ascii')
    return (password, passwordMsg)


def RanPasswdGenerate(pwdlength=8, upCase=True, loCase=True, digit=True, spChar=True):
    import string
    import random
    import secrets
    charList = []
    # Add the required charactor
    if upCase:
        charList.append(random.choice(string.ascii_uppercase))
    if loCase:
        charList.append(random.choice(string.ascii_lowercase))
    if digit:
        charList.append(random.choice(string.digits))
    if spChar:
        charList.append(random.choice(string.punctuation))
    # Add a secret random string
    charList.append(''.join((secrets.choice(string.ascii_lowercase + string.ascii_uppercase +
                                            string.digits + string.punctuation) for _ in range(pwdlength-len(charList)))))
    # random change the sequence
    password = ''.join(random.sample(charList, len(charList)))
    return password


def passwdConvert(messageStr, b64Encode=True):
    if b64Encode:
        message_bytes = messageStr.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message
    else:
        base64_bytes = messageStr.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        return message


# test case:
print('Start to test')
password = ''.join((secrets.choice(string.ascii_lowercase + string.ascii_uppercase +
                                   string.digits + string.punctuation) for i in range(6)))

print(password)
cvtStr = passwdConvert(password, b64Encode=True)
print(cvtStr)
testPwd = passwdConvert(cvtStr, b64Encode=False)
print(testPwd)

result = 'pass' if password == testPwd else 'failed'
print(result)


print(RanPasswdGenerate(pwdlength=10))
