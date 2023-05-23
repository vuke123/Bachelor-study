import sys
import getpass
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Hash import HMAC, SHA256
from base64 import b64decode
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
import os


def Hash_password(password, salt=None):
    if salt == None:
        salt = b64encode(os.urandom(16)).decode('utf-8')
    salted_password = salt + password
    hash_object = SHA256.new(data=salted_password.encode('utf-8'))
    hashed_password = hash_object.hexdigest()
    return hashed_password, b64decode(salt.encode('utf-8'))


def Generate_hmac(hashed_password):
    key = os.urandom(16)  # bytes
    h = HMAC.new(key, digestmod=SHA256)
    h.update(bytes.fromhex(hashed_password))
    return h.hexdigest(), key


def Add_user(username):
    with open("passwords.txt", "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i % 3 == 0 and line.strip() == username:
                print("Username already exists")
                f.close()
                return
        f.close()
    condition = False 
    password = getpass.getpass("Password: ")
    repeated_password = getpass.getpass("Repeat password: ")

    if password != repeated_password:
        print("User add failed. Password mismatch.")
    else:
        hashed_password, salt = Hash_password(password)
        hmac_password, key = Generate_hmac(hashed_password)
        with open("passwords.txt", "a") as f:
            f.write(username + '\n')  # string
            f.write(hashed_password + '\n')  # hexa
            f.write(b64encode(salt).decode('utf-8') + "\n")  # to base64 byte string
            f.close()
        with open("secure_storage.txt", "a") as f:
            f.write(hmac_password + "\n")  # hexa
            f.write(b64encode(key).decode('utf-8') + "\n")  # byte string
        print("User {} successfuly added.".format(username))
    return


def Check_user_exist(username):
    username_index = None
    with open("passwords.txt", "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i % 3 == 0 and line.strip() == username:
                username_index = i
        f.close()
    if username_index == None:
        return False, None, None
    else:
        return True, lines, username_index


def Change_passwd(username):
    lines = []
    username_index = None
    boolean, lines, username_index = Check_user_exist(username)
    if boolean == False:
        print("User does not exist.")
        return
    else:
        password = getpass.getpass("Password: ")
        repeated_password = getpass.getpass("Repeat password: ")
        if password != repeated_password:
            print("Password change failed. Password mismatch.")
            return
        hashed_password, salt = Hash_password(password, salt=None)
        lines[username_index + 1] = hashed_password + "\n"
        lines[username_index + 2] = b64encode(salt).decode('utf-8') + "\n"
        hmac_password, key = Generate_hmac(hashed_password)
        with open("passwords.txt", "w") as f:
            f.writelines(lines)
            f.close()
        with open("secure_storage.txt", "r") as f:
            lines_ss = f.readlines()
            f.close()
        lines_ss[int(username_index / 3 * 2)] = hmac_password + "\n"
        lines_ss[int(username_index / 3 * 2) + 1] = b64encode(key).decode('utf-8') + "\n"
        with open("secure_storage.txt", "w") as f:
            f.writelines(lines_ss)
            f.close()

        print("Password change successful.")
        return

def Forcepass(username):
    username_index = None
    boolean, lines, username_index = Check_user_exist(username)
    if boolean == False:
        print("User does not exist.")
        return
    else:
        lines[username_index + 1] = lines[username_index + 1].strip() + "!" + "\n"
        with open("passwords.txt", "w") as f:
            f.writelines(lines)
            f.close()
        print("User will be requested to change password on next login.")


def Delete_user(username):
    username_index = None
    boolean, lines, username_index = Check_user_exist(username)
    if boolean == False:
        print("User does not exist.")
        return
    else:
        lines.pop(username_index + 2)
        lines.pop(username_index + 1)
        lines.pop(username_index)
        with open("passwords.txt", "w") as f:
            f.writelines(lines)
            f.close()
        with open("secure_storage.txt", "r") as f:
            lines_ss = f.readlines()
            f.close()
        lines_ss.pop(username_index + 1)
        lines_ss.pop(username_index)
        with open("secure_storage.txt", "w") as f:
            f.writelines(lines_ss)
            f.close()
        print("User successfuly removed.")


def main():
    method = sys.argv[1]
    username = sys.argv[2]
    if method == "add":
        Add_user(username)
    elif method == "passwd":
        Change_passwd(username)
    elif method == "forcepass":
        Forcepass(username)
    elif method == "del":
        Delete_user(username)


if __name__ == "__main__":
    main()