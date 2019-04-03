from platform import Platform

p = Platform()
p.connect()
p.ask_authenticator_make_credential()
p.disconnect()