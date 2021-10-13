#!/bin/python

import os
import json
import base64 
import win32crypt
from Crypto.Cipher import AES
import sqlite3
import argparse

def getDecryptionKey(localStateFilePath):
    expanded = os.path.expandvars(localStateFilePath)
    with open(expanded, 'r') as file:
        encrypted_key = json.loads(file.read())['os_crypt']['encrypted_key']
    encrypted_key = base64.b64decode(encrypted_key)                                 
    # Remove "DPAPI" string 
    encrypted_key = encrypted_key[5:]                                               
    
    decryptedKey = None
    # Decrypt key with using DPAPI  
    try:
        decryptedKey = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except:
        print("- ERROR: Unable to decrypt key from \"Local State\" with using DPAPI.")
        print("- Maybe script is not executed on the same OS, which created the file?")
        exit()
    
    return decryptedKey
    

def decryptString(decryptionKey, data):
    nonce = data[3:3+12]
    ciphertext = data[3+12:-16]
    tag = data[-16:]
    cipher = AES.new(decryptionKey, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag) # the decrypted cookie


def decryptCookies(cookieFilePath, localStateFilePath, outputFilePath):
    counter = 0
    decryptionKey = getDecryptionKey(localStateFilePath)

    print("- decrytion starts")

    # iterate over data
    con = sqlite3.connect(cookieFilePath)

    if outputFilePath != None:
        outputFileHandler = open(outputFilePath, "w")
        outputFileHandler.seek(0)
        outputFileHandler.write("creation_utc;top_frame_site_key;host_key;name;value;decrypted_value;path;expires_utc;is_secure;is_httponly;last_access_utc;has_expires;is_persistent;priority;samesite;source_scheme;source_port;is_same_party;\n")

    for row in con.execute('SELECT creation_utc,top_frame_site_key,host_key,name,value,hex(encrypted_value),path,expires_utc,is_secure,is_httponly,last_access_utc,has_expires,is_persistent,priority,samesite,source_scheme,source_port,is_same_party FROM cookies'):
        counter += 1
        # get decrypted cookie value
        decryptedCookie = decryptString(decryptionKey,bytes.fromhex(row[5]))

        if outputFilePath != None:
            # render CSV lines
            lineStr = str(row[0])
            for i in range(1,17):
                lineStr +=";"
                if (i == 5):
                    lineStr += decryptedCookie.decode("utf-8")
                else:
                    lineStr += str(row[i])
            outputFileHandler.write(lineStr+"\n")
        else:
            print("- cookie "+row[3]+" (for site "+row[2]+"):")
            print(decryptedCookie.decode("utf-8")+"\n")


    print("- decrytion is complete, total number of decrypted cookies: " + str(counter))
    if outputFilePath != None:
        outputFileHandler.truncate()
        outputFileHandler.close()
        print("- output successfully saved to: "+ outputFilePath)



def initParser():
    parser = argparse.ArgumentParser(description='This script decrypts encryted cookie file, with using "Local State" file and DPAPI. Works for Chrome-like browsers (Chrome, Chromium, Edge, ...).')
    parser.add_argument('-c', '--cookie-file', type=str, nargs=1 ,help='Path to cookie db file to decrypt, for example:\n"C:\\Users\\{USERNAME}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cookies"', required=True)
    parser.add_argument('-l', '--local-state-file', type=str, nargs=1 ,help='Path to "Local State", for example:\n"C:\\Users\\{USERNAME}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Local State"', required=True)
    parser.add_argument('-o','--output-csv', type=str, nargs=1 ,help='Output CSV file with all cookie attributes. If outputfile is not defined, decrypted cookies will be printed on standart output.')
    args = parser.parse_args()
    return args


def main():
    args = initParser()

    # pass arguments to variables
    cookieFilePath = getattr(args, "cookie_file")[0]
    localStateFilePath = getattr(args, "local_state_file")[0]
    outputFilePath = None
    if (getattr(args, "output_csv") != None):
        outputFilePath = getattr(args, "output_csv")[0]

    # call decrypt function
    decryptCookies(cookieFilePath, localStateFilePath, outputFilePath)


if __name__ == "__main__":
    main()
