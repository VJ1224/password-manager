import os
from passlib.hash import pbkdf2_sha256

def hashPassword(password):
    return pbkdf2_sha256.hash(password)

def verifyPassword(password):
    return pbkdf2_sha256.verify(password,readHash())

def storeHash(hash):
    os.environ['PM_PASSWORD'] = hash

def readHash():
    return os.environ['PM_PASSWORD']

storeHash(hashPassword("vj1224"))
