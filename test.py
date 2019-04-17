from browser import Browser

b = Browser()
b.register_u2f("steve", "not_secure", "example.com")
b.authenticate_u2f("steve", "not_secure", "example.com")
