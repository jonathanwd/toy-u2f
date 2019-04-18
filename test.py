from browser import Browser
from authenticator import Authenticator
from relyingParty import RelyingParty

b = Browser()
b.register_u2f("steve", "not_secure", "example.com")
b.authenticate_u2f("steve", "not_secure", "example.com")
