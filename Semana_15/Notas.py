# APP: CHAT CLIENTE - SERVIDOR TCP/IP
import socket
import threading
import sys

HOST = "192.168.0.100"
PORT = 54321
HEADER_SIZE = 10

class Server:
    def __init__(self):
        self.connections = [] #lista de sockets
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST,PORT))
        self.sock.listen()

    def run(self):
        print("Servidor iniciado. Esperando conexiones ... ")
        while True:
            conn, addr = self.sock.accept()

            #Se establece un thread por cada conexion entrante para

            th=threading.Thread(target=self.handle, args=(conn, addr), daemon = True)
            th.start()

            print(str(addr[0]) + ":" + str(addr[1]), "conectado a Server")

            self.connections.append(conn)

    def handle(self, conn, addr):
        while True:
            try:
                data_header = conn.recv(HEADER_SIZE)
                data = conn.recv(int(data_header))
                #Hacemos un broadcast (replicar el mensaje del cliente en los demas clientes)
                for connection in self.connections:
                    connection.send(data_header + data)
            except:
                #El cliente se ha desconectado
                print(str(addr[0]) + ":" + str(addr[1]), "desconectado")
                self.connections.remove(conn)
                conn.close()
                break
class Client:
    def __init__(self, address, username='chat_user'):
        self.username = username
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address, PORT))

        #Thread para el envio de mensajes
        th=threading.Thread(target=self.sendMsg, daemon=True)
        th.start()

        while True:
            data_header = self.sock.recv(HEADER_SIZE)
            if not data_header:
                break
            data = self.sock.recv(int(data_header))
            print("\n" + data.decode('utf-8'))

    def sendMsg(self):
        while True:
            strData = input(f"{self.username}>")
            data_len = len(strData + self.username + ">")
            self.sock.send(f"{data_len:<{HEADER_SIZE}}{self.username}>{strData}".encode('utf-8'))





#python chat.py (Server)
#python chat.py IP_SERVER (Cliente) Con nombre generico
#python chat.py IP_SERVER NICKNAME (Cliente) Con nombre especifico

def main():
    if len(sys.argv) > 1:
        if len(sys.argv) == 3:
            client = Client(sys.argv[1], sys.argv[2])
        else:
            client = Client(sys.argv[1])
    else:
        server = Server()
        server.run()

if __name__ == "__main__":
    main()