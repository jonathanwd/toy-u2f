import hmac
import hashlib
import Crypto
import base64
import random
from Crypto.PublicKey import RSA
from Crypto.PublicKey import ECC
from Crypto.Cipher import AES
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from collections import OrderedDict 

device_secret_key = b"\xc8\xbb\x34\x48\x9c\xcf\x6c\x38\xfd\x3e\x55\xb4\xa9\xdf\x75\x7e\x78\xfa\x6c\xa6\xd3\x6e\x5b\x36\xf1\x7c\x28\x60\x52\x65\xc3\x92"

def generate_credential(appID):
    nonce = random.randint(1,1000)
    msg = appID + str(nonce)
    hmac_object = hmac.new(device_secret_key, msg.encode(), hashlib.sha256)
    digest = hmac_object.digest()
    key = ECC.construct(curve='P-256', d=int.from_bytes(digest, byteorder='big'))
    return key, nonce

def generate_mac(appID, key):
    msg = appID + key.export_key(format='PEM')
    hmac_object = hmac.new(device_secret_key, msg.encode(), hashlib.sha256)
    digest = hmac_object.digest()
    return digest

def sign(key, toSign):
    signer = DSS.new(key, 'fips-186-3')
    h = SHA256.new(str(toSign).encode())
    signature = signer.sign(h)
    return signature
    
    # credential = {}
    # key = None
    # nonce = Crypto.Random.random.getrandbits(64)
    # nonce = b"\xc8\xbb\x34\x48\x9c\xcf\x6c\x38\xfd\x3e\x55\xb4\xa9\xdf\x75\x7e\x78\xfa\x6c\xa6\xd3\x6e\x5b\x36\xf1\x7c\x28\x60\x52\x65\xc3\x92"
    # msg = appID + str(nonce)
    # hmac_object = hmac.new(device_secret_key, msg.encode(), hashlib.sha256)
    # digest = hmac_object.digest()
    # key = ECC.construct(curve='P-256', d=int.from_bytes(digest, byteorder='big'))
    # publicKey = key.publicKey()
    # credential["type"] = "public-key"
    # credential['user'] = user
    # cipher_aes = AES.new(digest, AES.MODE_EAX, nonce=nonce)
    # credentialSource = str(OrderedDict(sorted(credential.items())))
    # ciphertext = cipher_aes.encrypt(credentialSource.encode())
    # credential["privateKey"] = key.export_key(format='PEM')
    # credential['credentialId'] = ciphertext
    # attestation = {}
    # attestation['publicKey'] = publicKey.export_key(format='PEM')
    # attestation['nonce'] = str(base64.b64encode(nonce))[2:-1]
    # attestation['algo'] = algo
    # attestation['credentialId'] = str(base64.b64encode(credential['credentialId']))[2:-1]
    # h = SHA256.new(appID.encode())
    # signer = DSS.new(key, 'fips-186-3')
    # signature = signer.sign(h)
    # attestation['app_id_sig'] = str(base64.b64encode(signature))[2:-1]
    # print(attestation['app_id_sig'])
    # return str(attestation).replace("'",'"')

def verify(publicKey, signature, appID):
    signature = base64.b64decode(signature)
    key = ECC.import_key(publicKey)
    h = SHA256.new(appID.encode())
    verifier = DSS.new(key, 'fips-186-3')
    try:
        verifier.verify(h, signature)
        print("The message is authentic.")
    except ValueError:
        print("The message is not authentic.")

# test = (-1, {"id": "example.com", "name": "Jessica"}, {"id": "User ID", "name": "jessica@example.com", "displayName": "Jessica Smith"})
# print(generate_credential(-7, {"id": "example.com", "name": "Jessica"}, {"id": "User ID", "name": "jessica@example.com", "displayName": "Jessica Smith"}))

# print(generate_credential(
#     -7, 
#     OrderedDict([
#                 ("id", "example.com"),
#                 ("name", "Acme")]), 
#     OrderedDict([
#                 ("id", b"\x30\x82\x01\x93\x30\x82\x01\x38\xa0\x03\x02\x01\x02\x30\x82\x01\x93\x30\x82\x01\x38\xa0\x03\x02\x01\x02\x30\x82\x01\x93\x30\x82"),
#                 ("icon", "https://pics.example.com/00/p/aBjjjpqPb.png"),
#                 ("name",  "johnpsmith@example.com"),
#                 ("displayName", "John P. Smith")])))