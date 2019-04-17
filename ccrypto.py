import hmac
import hashlib
import Crypto
import random
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from collections import OrderedDict 

device_secret_key = b"\xc8\xbb\x34\x48\x9c\xcf\x6c\x38\xfd\x3e\x55\xb4\xa9\xdf\x75\x7e\x78\xfa\x6c\xa6\xd3\x6e\x5b\x36\xf1\x7c\x28\x60\x52\x65\xc3\x92"

def new_credential(appID):
    nonce = random.randint(1,1000)
    msg = appID + str(nonce)
    hmac_object = hmac.new(device_secret_key, msg.encode(), hashlib.sha256)
    digest = hmac_object.digest()
    key = ECC.construct(curve='P-256', d=int.from_bytes(digest, byteorder='big'))
    return key, nonce

def credential_from_nonce(appID, nonce):
    msg = appID + str(nonce)
    hmac_object = hmac.new(device_secret_key, msg.encode(), hashlib.sha256)
    digest = hmac_object.digest()
    key = ECC.construct(curve='P-256', d=int.from_bytes(digest, byteorder='big'))
    return key

def generate_mac(appID, key):
    msg = appID + key.export_key(format='PEM')
    hmac_object = hmac.new(device_secret_key, msg.encode(), hashlib.sha256)
    digest = hmac_object.digest()
    return digest

def sign(key, toSign):
    signer = DSS.new(key, 'fips-186-3')
    h = SHA256.new(str(toSign).encode())
    print(str(toSign))
    print(h.hexdigest())
    signature = signer.sign(h)
    return signature
    
def verify(publicKey, signature, toSign):
    key = ECC.import_key(publicKey)
    h = SHA256.new(str(toSign).encode())
    print(str(toSign))
    print(h.hexdigest())
    verifier = DSS.new(key, 'fips-186-3')
    try:
        verifier.verify(h, signature)
        print("The message is authentic.")
        return True
    except ValueError:
        print("The message is not authentic.")
        return False
