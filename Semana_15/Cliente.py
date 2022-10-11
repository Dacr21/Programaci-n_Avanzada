#import socket

#HOST = "192.168.0.100" #IP Server
#PORT = 65123

#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

#    s.connect((HOST, PORT))
   
#    s.sendall(b"Hola mundo")
#    data = s.recv(1024)

#print("Recibido: ", repr(data))

#%%

#import socket
#import time

#HOST = "192.168.0.100"
#PORT = 65123

#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#    s.connect((HOST,PORT))
#
#    for n in range(1,11):
#        strData = str(n)
#        data = strData.encode("utf-8")
#        s.send(data)
#
#        time.sleep(1)
#%%
#import socket
#import time

#HOST = "192.168.0.100"
#PORT = 65123
#HEADER  = 10

#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#    s.connect((HOST,PORT))

#    names = ['Maria', 'Rodrigo', 'Heteraclico', 'Sandro', 'Jeffri']

#    for name in names:
#        data_len = len(name)
#        data = f"{data_len:<{HEADER}}{name}".encode('utf-8')
#        s.send(data)

#        time.sleep(1)
#%%
#%%
import socket
import pickle

HOST = "192.168.0.100"
PORT = 65123
HEADER  = 10

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))

    names = ['Maria', 'Rodrigo', 'Heteraclico', 'Sandro', 'Jeffri']
    data_serial = pickle.dumps(names) #bytes

    data_len = len(data_serial)
    data = f"{data_len:<{HEADER}}".encode('utf-8') + data_serial
    print(data)
    s.send(data)