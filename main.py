
# * Imports
from cryptography.fernet import Fernet
import json
import os

# ! Note: When making a fork of this project you should first make a new key using the function below

# def makeNewKey():
#     key = Fernet.generate_key()

#     with open('securityKey.key', 'wb') as mykey:
#         mykey.write(key)


# * Load Security Key
with open('securityKey.key', 'rb') as mykey:
    key = mykey.read()


# * Functions
def login(username, password, level):
    usersData = {}
    with open("users.json") as f:
        data = json.loads(f.read())
        usersData = data

    try:
        if (usersData[username]):
            user = usersData[username]
            if user["password"] == password:
                if user["level"] == level:
                    return True
                else:
                    return('ERR: Security level incorrect \n')
            else:
                return('ERR: Password incorrect \n')
    except:
        return('ERR: Username not found \n')


def encryptFile(localKey, fileName):
    f = Fernet(localKey)

    with open(f'Documents/{fileName}.json', 'rb') as original_file:
        original = original_file.read()

    encrypted = f.encrypt(original)

    with open(f'Documents/enc_{fileName}.json', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    os.remove(f'Documents/{fileName}.json')


def decryptFile(localKey, fileName):
    f = Fernet(localKey)

    with open(f'Documents/enc_{fileName}.json', 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = f.decrypt(encrypted)

    with open(f'Documents/dec_{fileName}.json', 'wb') as decrypted_file:
        decrypted_file.write(decrypted)


def openDocument(localKey, fileName, accesslevel):
    try:
        if int(accesslevel) and int(accesslevel) <= 5:
            result = True
            if int(accesslevel) != 1:
                # Login stuff
                userName = input('Type your username \n \n')
                password = input('Type your password \n \n')
                result = (login(userName, password, accesslevel))

            if result == True:
                decryptFile(localKey, fileName)
                fileData = {}
                with open(f"Documents/dec_{fileName}.json") as f:
                    data = json.loads(f.read())
                    fileData = data
                if fileData[accesslevel] != "":
                    input(fileData[accesslevel])
                    os.remove(f'Documents/dec_{fileName}.json')
                    return ""
                else:
                    return "ACCESS DENIED"
            else:
                return result
        else:
            return('ERR: Invalid input (type "help" for more info) \n')
    except:
        return('ERR: Invalid input (type "help" for more info) \n')


# * Main app
infoData = {}
with open("databaseInfo.json") as f:
    data = json.loads(f.read())
    infoData = data
print("Welcome to", infoData["databaseName"])
print("Date of database:", infoData["databaseDate"])
print("Description of database:", infoData["databseDescription"])

while True:
    query = input('Type a query (type "help" for guide) \n \n')
    if query == "help" or query == "Help":
        print("help: Guide of queries")
        print("access FileName UserSecurityLevel: Access a file")
        print("change FileName UserSecurityLevel: Change a file")
        print("write FileName UserSecurityLevel: Write a new file")
        print("delete FileName UserSecurityLevel: Delete a file")
        print("logout: Logout of the database \n")

    # Close program command
    elif query == "logout" or query == "Logout":
        print("Logging out...")
        quit()

    else:

        # * List queries
        query = query.split(" ")
        # print("LIST:", query)
        # Access file command
        if query[0] == "access":
            # print(query)
            if len(query) == 3:
                print(openDocument(key, query[1], query[2]))
            else:
                print('ERR: Invalid input (type "help" for more info) \n')

        else:
            print('ERR: Invalid query (type "help" for more info) \n')
