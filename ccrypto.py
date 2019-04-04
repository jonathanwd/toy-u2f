import hmac
import hashlib
import Crypto
from Crypto.PublicKey import RSA
from Crypto.PublicKey import ECC
from collections import OrderedDict 

device_secret_key = b"\xc8\xbb\x34\x48\x9c\xcf\x6c\x38\xfd\x3e\x55\xb4\xa9\xdf\x75\x7e\x78\xfa\x6c\xa6\xd3\x6e\x5b\x36\xf1\x7c\x28\x60\x52\x65\xc3\x92"

def generate_credential(algo, rpEntity, userEntity):
    credential = {}
    key = None
    if algo == -7:
        appID = str(rpEntity)
        # nonce = Crypto.Random.random.getrandbits(64)
        nonce = "\xc8\xbb\x34\x48\x9c\xcf\x6c\x38\xfd\x3e\x55\xb4\xa9\xdf\x75\x7e\x78\xfa\x6c\xa6\xd3\x6e\x5b\x36\xf1\x7c\x28\x60\x52\x65\xc3\x92"
        msg = appID + str(nonce)
        hmac_object = hmac.new(device_secret_key, msg.encode(), hashlib.sha256)
        digest = hmac_object.digest()
        key = ECC.construct(curve='P-256', d=int.from_bytes(digest, byteorder='big'))
        print(key)
        # key = RSA.generate(2048)
        credential["type"] = "public-key"
        # credential["privateKey"] = key.exportKey(format='PEM')
        credential['rpId'] = rpEntity["id"]
        credential['userHandel'] = userEntity["id"]
        credential['otherUI'] = None
        credential['credentialId'] = 1
    return credential

# print(key.export_key(format='PEM'))
print(generate_credential(
    -7, 
    OrderedDict([
                ("id", "example.com"),
                ("name", "Acme")]), 
    OrderedDict([
                ("id", b"\x30\x82\x01\x93\x30\x82\x01\x38\xa0\x03\x02\x01\x02\x30\x82\x01\x93\x30\x82\x01\x38\xa0\x03\x02\x01\x02\x30\x82\x01\x93\x30\x82"),
                ("icon", "https://pics.example.com/00/p/aBjjjpqPb.png"),
                ("name",  "johnpsmith@example.com"),
                ("displayName", "John P. Smith")])))