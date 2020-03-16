import os
from passlib.hash import pbkdf2_sha256

def hashPassword(password):
    hash=pbkdf2_sha256.hash(password)
    return hash

def verifyPassword(password):
    hash=readHash()
    check=pbkdf2_sha256.verify(password,hash)
    return check

def storeHash(hash):
    with open("hash.txt", "w") as file:
        file.write(hash)

def readHash():
    with open("hash.txt","r") as file:
        return file.read()
