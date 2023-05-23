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
import time


def Hash_password(password, salt=None):
    if salt == None:
        salt = b64encode(os.urandom(16)).decode('utf-8')

    salted_password = salt + password
    hash_object = SHA256.new(data=salted_password.encode('utf-8'))
    hashed_password = hash_object.hexdigest()
    return hashed_password, salt


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


def Check_integrity(username_index, hashed_password):
    with open("secure_storage.txt", "r") as f:
        lines = f.readlines()
        hmac = lines[int(username_index / 3 * 2)].strip()
        key = lines[int(username_index / 3 * 2) + 1].strip()
        key = b64decode(key.encode('utf-8'))
        h = HMAC.new(key,digestmod=SHA256)
        h.update(bytes.fromhex(hashed_password))
        f.close()
    try:
        h.hexverify(hmac)
        return True
    except ValueError:
        return False


def Generate_hmac(hashed_password):
    key = os.urandom(16)
    h = HMAC.new(key, digestmod=SHA256)
    h.update(bytes.fromhex(hashed_password))
    return h.hexdigest(), key


def Change_password(username_index):
    lines = []
    changed = False
    with open("passwords.txt", "r") as f:
        lines = f.readlines()
        f.close()

    while changed == False:
        password = getpass.getpass("New password: ")
        repeated_password = getpass.getpass("Repeat new password: ")
        if password != repeated_password:
            print("Password change failed. Password mismatch.")
        else:
            changed = True

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
    lines_ss[(username_index / 3 * 2)] = hmac_password + "\n"
    lines_ss[(username_index / 3 * 2) + 1] = key + "\n"
    with open("secure_storage.txt", "r") as f:
        f.writelines(lines_ss)
        f.close()

    print("Password change successful.")


def main():
    must_change_psswd = False
    username = sys.argv[1]
    boolean, lines, username_index = Check_user_exist(username)
    hashed_password = "b94d27"  # random wrong password
    saved_hashed_password = None
    if boolean:
        saved_hashed_password = lines[username_index + 1].strip()
        if saved_hashed_password[-1] == "!":
            must_change_psswd = True
            saved_hashed_password = saved_hashed_password[:-1]
        if Check_integrity(username_index, saved_hashed_password) == False:
            print("The integrity is broken!")

    confirmed_password = False
    i = 0
    while confirmed_password or i < 5:
        password = getpass.getpass("Password: ")
        if boolean:
            hashed_password, _ = Hash_password(password, lines[username_index + 2])
        print(hashed_password)
        print(saved_hashed_password)
        if hashed_password == saved_hashed_password:
            if must_change_psswd == True:
                Change_password(username_index)
        else:
            print("Username or password incorrect.")
            time.sleep(pow(3, i))
            i += 1


if __name__ == "__main__":
    main()