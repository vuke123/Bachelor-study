import sys
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Hash import HMAC, SHA256
from base64 import b64decode
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes


def check_master_password(entered_master):

    with open("parameters.txt", "r") as f:
        master_salt64 = f.readline().rstrip()
        master_cipher_iv64 = f.readline().rstrip()
        f.close()
    with open("passwords.txt", "r") as f:
        hash64 = f.readline().rstrip()
        hashedHash64 = f.readline().rstrip()
        f.close()

    if not check_integrity(b64decode(hash64), b64decode(hashedHash64)):
        print("The integrity of master password is broken")
        return None

    key = PBKDF2(entered_master, b64decode(master_salt64), count=100000, hmac_hash_module=SHA256)
    cipher = AES.new(key, AES.MODE_CBC, b64decode(master_cipher_iv64))
    provjera = ""
    try:
        provjera = cipher.decrypt(b64decode(hash64))
        confirmation_word = unpad(provjera, AES.block_size, style='pkcs7')
    except:
        print("The master password is incorrect")
        return False

    if confirmation_word == b'ConfirmMasterPassword':
        print("The master password is correct")
        return True
    else:
        print("The master password is incorrect")
        return False


def check_integrity(encryped_word, hmac):

    keyHMAC = b'Swordfish'
    h = HMAC.new(keyHMAC, digestmod=SHA256)
    h.update(encryped_word)
    try:
        h.hexverify(hmac)
        return True
    except ValueError:
        return False


def encrypt(master, word):
    salt = get_random_bytes(16)
    key = PBKDF2(master, salt, count=100000, hmac_hash_module=SHA256)
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_word = cipher.encrypt(pad(word, AES.block_size, style='pkcs7'))

    return encrypted_word, salt, cipher.iv


def decrypt(master, salt, cipheriv, encrypted_word, hmac):
    key = PBKDF2(master, salt, count=100000, hmac_hash_module=SHA256)
    cipher = AES.new(key, AES.MODE_CBC, cipheriv)
    integrity = check_integrity(encrypted_word, hmac)
    return unpad(cipher.decrypt(encrypted_word), AES.block_size, style='pkcs7'), integrity


def find_address(passwords_lines, parameters_lines, address, master, return_password=None):
    dict1 = {}
    i = 0
    while i < len(passwords_lines)-1:
        encrypted_word = b64decode(passwords_lines[i].strip())
        hmac = b64decode(passwords_lines[i+1].strip())
        salt = b64decode(parameters_lines[i].strip())
        cipheriv = b64decode(parameters_lines[i+1].strip())
        dict1[encrypted_word] = (hmac, salt, cipheriv, i)
        i += 2
    for encrypted_word, (hmac, salt, cipheriv, i) in dict1.items():
        integrity = True
        addr_psww, integrity = decrypt(
            master, salt, cipheriv, encrypted_word, hmac)
        addr_psww = addr_psww.decode('utf-8')
        if integrity == False:
            print("The integrity is broken for address: " %
                  addr_psww.split(" "[0]))
        if addr_psww.split(" ")[0] == address and integrity == True:
            if return_password == None:
                return i
            else:
                return i, addr_psww.split(" ")[1]
    if return_password == None:
        return -1
    else:
        return -1, None


def generate_hmac(encrypted_word):
    keyHMAC = b'Swordfish' ##nesigurno 
    h = HMAC.new(keyHMAC, digestmod=SHA256)
    h.update(encrypted_word)
    return b64encode(h.hexdigest().encode()).decode('utf-8')


def is_valid_password(password):
    if len(password) < 8:
        return False
    has_uppercase = False
    has_lowercase = False
    has_digit = False
    for char in password:
        if char.isupper():
            has_uppercase = True
        elif char.islower():
            has_lowercase = True
        elif char.isdigit():
            has_digit = True
        if has_uppercase and has_lowercase and has_digit:
            return True
    return False


def main():
    method = sys.argv[1]

    if method == 'init':
        master_password = sys.argv[2]

        if not is_valid_password(master_password):
            print("Master password must be at least 8 characters long, have at lest one uppercase letter, lowercase letter and one digit.")
            return
        encrypted_word, salt, iv = encrypt(
            master_password, b'ConfirmMasterPassword')

        with open("passwords.txt", "w") as f:
            f.write(b64encode(encrypted_word).decode('utf-8') + '\n')
            f.write(generate_hmac(encrypted_word) + '\n')
            f.close()
        with open("parameters.txt", "w") as f:
            f.write(b64encode(salt).decode('utf-8') + "\n")
            f.write(b64encode(iv).decode('utf-8') + "\n")
            f.close()
            print("Password manager initialized")

    elif method == 'put':
        entered_master = sys.argv[2]
        address = sys.argv[3]
        password = sys.argv[4]

        if check_master_password(entered_master) == True:
            with open("passwords.txt", "r") as f:
                passwords_lines = f.readlines()[2:]
            with open("parameters.txt", "r") as f:
                parameters_lines = f.readlines()[2:]

            line_for_update = find_address(
                passwords_lines, parameters_lines, address, entered_master, return_password=None)
            encrypted_word, salt, iv = encrypt(
                entered_master, (address + " " + password).encode('utf-8'))
            if line_for_update == -1:
                with open("passwords.txt", "a") as f:
                    f.write(b64encode(encrypted_word).decode('utf-8') + '\n')
                    f.write(generate_hmac(encrypted_word) + '\n')
                    f   .close()
                with open("parameters.txt", "a") as f:
                    f.write(b64encode(salt).decode('utf-8') + '\n')
                    f.write(b64encode(iv).decode('utf-8') + '\n')
                    f.close()
            else:
                with open("passwords.txt", "r") as f:
                    lines = f.readlines()
                    f.close()
                lines[2 + line_for_update] = b64encode(
                    encrypted_word).decode('utf-8') + "\n"
                lines[2 + line_for_update +
                      1] = generate_hmac(encrypted_word) + "\n"
                with open("passwords.txt", "w") as f:
                    f.writelines(lines)
                    f.close()
                with open("parameters.txt", "r") as f:
                    lines = f.readlines()
                    f.close()
                lines[2 +
                      line_for_update] = b64encode(salt).decode('utf-8') + "\n"
                lines[2 + line_for_update +
                      1] = b64encode(iv).decode('utf-8') + "\n"
                with open("parameters.txt", "w") as f:
                    f.writelines(lines)
                    f.close()
            print("Stored password for {} ".format(address))

    elif method == "get":
        entered_master = sys.argv[2]
        address = sys.argv[3]

        if check_master_password(entered_master) == True:
            with open("passwords.txt", "r") as f:
                passwords_lines = f.readlines()[2:]
            with open("parameters.txt", "r") as f:
                parameters_lines = f.readlines()[2:]
            index, password = find_address(
                passwords_lines, parameters_lines, address, entered_master, return_password=True)
            if index == -1:
                print("The requested address does not exist")
            else:
                print("Password for {} is {}".format(address, password))


if __name__ == "__main__":
    main()
