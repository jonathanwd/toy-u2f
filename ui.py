from browser import Browser

b = Browser()
dns = {
    # 'authenticator': ('127.0.1.1', 23456),
    "example.com": ('127.0.1.1', 23457),
    "attacker.com": ('127.0.1.1', 23457),
    "test.com": ('127.0.1.1', 23458)
}

def get_info():
    website = input("\tWhat website? ")
    if website not in dns:
        print("Website not found")
        return None, None, None
    username = input("\tEnter your username: ")
    password = input("\tEnter your password: ")
    return website, username, password

while True:
    command = input("S-Sign up\nR-Register\nA-Authenticate\nX-Exit\n\tSelection: ")
    if str.lower(command) == 's':
        website, username, password = get_info()
        if website:
            print(b.sign_up(website, username, password, dns[website]))
    elif str.lower(command) == 'r':
        website, username, password = get_info()
        if website:
            print(b.register_u2f(website, username, password, dns[website]))
    elif str.lower(command) == 'a':
        website, username, password = get_info()
        if website:
            print(b.authenticate_u2f(website, username, password, dns[website]))
    elif str.lower(command) == 'x':
        break
    

# b.register_u2f("steve", "not_secure", "example.com")
# b.authenticate_u2f("steve", "not_secure", "example.com")