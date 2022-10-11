#import socket

#HOST = "192.168.0.100"
#PORT = 65123

#with socket.socket(socket.AF_INET, 
#                    socket.SOCK_STREAM) as s:

#    s.bind((HOST, PORT))
 #   s.listen()

#   conn, addr = s.accept()  #Esperando......

#    with conn:
 #       print("Conectando a ", addr)

#        while True:
#           data = conn.recv(1024)

#            if not data:
#                break
            
#            conn.sendall(data)

#%%
#import socket

#HOST = "192.168.0.100"
#PORT = 65123

#with socket.socket(socket.AF_INET, 
 #                   socket.SOCK_STREAM) as s:

 #   s.bind((HOST, PORT))
  #  s.listen()

  #  conn, addr = s.accept()

   # try:
   #     with conn:
   #         print("Conectado a", addr)
   #         while True:
   #             data = conn.recv(1)
#
   #            if not data:
   #                 break
   #             else:
   #                 strData = data.decode('utf-8')
   #                 print(strData)
    #except KeyboardInterrupt:
  #      pass
#
#print("Cerrando conexion")

#%%
#import socket

#HOST = "192.168.0.100"
#PORT = 65123
#HEADER  = 10

#with socket.socket(socket.AF_INET, 
#                    socket.SOCK_STREAM) as s:

#    s.bind((HOST, PORT))
#    s.listen()

#    conn, addr = s.accept()

#    try:
#        with conn:
#            print("Conectado a", addr)
#            while True:
#                data_len = conn.recv(HEADER)
#
#                if not data_len:
#                    break
#                else:
#                    data = conn.recv(int(data_len))
#                    strData = data.decode('utf-8')
#                    print(strData)
#    except KeyboardInterrupt:
#        pass

#print("Cerrando conexion")
#%%
import socket
import pickle

HOST = "192.168.0.100"
PORT = 65123
HEADER  = 10

with socket.socket(socket.AF_INET, 
                    socket.SOCK_STREAM) as s:

    s.bind((HOST, PORT))
    s.listen()

    conn, addr = s.accept()

    try:
        with conn:
            print("Conectado a", addr)
            while True:
                data_len = conn.recv(HEADER)

                if not data_len:
                    break
                else:
                    data = b""
                    data += conn.recv(int(data_len))
                    data_deserial = pickle.loads(data)
                    print(data_deserial)
    except KeyboardInterrupt:
        pass

print("Cerrando conexion")
