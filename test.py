from platform import Platform

p = Platform()
p.connect()
p.send('hi')
p.disconnect()