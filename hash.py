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
    os.environ['PM_PASSWORD']=hash

def readHash():
    return os.environ['PM_PASSWORD']
