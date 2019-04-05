from platform1 import Platform

p = Platform()
p.connect('127.0.1.1', 23456)
p.ask_authenticator_make_credential()
p.receive_attestation()
p.disconnect()