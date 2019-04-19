# Toy U2F
This is a toy U2F example. It is composed of three main parts
* The Authenticator (i.e. U2F device)
* The FIDO Client (i.e. the browser) 
* The Relying Party (i.e. the web service)

The three parts should be run in three different windows. I built a simple TUI (ui.py) to simulate interactions between the user and the browser.
```
python3 authenticator.py
```
```
python3 relyingParty.py
```
```
python3 ui.py
```
