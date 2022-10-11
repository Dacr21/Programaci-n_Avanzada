
import socket
import threading

HOST = "192.168.0.100"
PORT = 54321
HEADER_SIZE  = 5

class Server:
    def __init__(self):
        self.connections = [] #lista de sockets
        self.userlist = [] #lista de nombres de usuario
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST,PORT))
        self.sock.listen()

    def run(self):
        print("Servidor iniciado. Esperando conexiones ... ")
        while True:
            conn, addr = self.sock.accept()

            #Se establece un thread por cada conexion entrante para
            self.connections.append(conn)
            th=threading.Thread(target=self.handle, args=(conn, addr), daemon = True)
            th.start()
            print(str(addr[0]) + ":" + str(addr[1]), "conectado a Server")
            

    def handle(self, conn, addr):
        while True:
            try:
                comand_code = conn.recv(2)
                if comand_code == b'TX':
                    data_header = conn.recv(HEADER_SIZE)
                    data = conn.recv(int(data_header))
                    #Hacemos un broadcast (replicar el mensaje del cliente en los demas clientes)
                    for connection in self.connections:
                        connection.send(comand_code + data_header + data)

                elif comand_code == b'US':
                    data_header = conn.recv(HEADER_SIZE)
                    nombre = conn.recv(int(data_header))
                    if nombre.decode("utf-8") not in self.userlist:
                        self.userlist.append(nombre.decode("utf-8"))
                        #Envio de lista de usuarios a los usuarios
                        self.Envio_lista()
                    else:
                        comand_code_Envio = 'CC'.encode('utf-8')
                        nombre = ''.encode('utf-8')
                        conn.send(comand_code_Envio)
                        conn.close()

                elif comand_code == '':
                    print('F')
                    pass

                else:
                    print("ERROR")
                    conn.close()
                
            except:
                #El cliente se ha desconectado
                print(str(addr[0]) + ":" + str(addr[1]), "desconectado")
                self.connections.remove(conn)
                try:    
                    self.userlist.remove(nombre.decode("utf-8"))
                except:
                    pass
                conn.close()
                self.Envio_lista()                
                break

    def Envio_lista(self):
        command_envio_lista = 'US'#.encode('utf-8')
        comand_clean_list = 'CL'.encode('utf-8')
        for connection in self.connections:
            connection.send(comand_clean_list)
            for usuarios_conectados in self.userlist:
                len_lista = str(len(usuarios_conectados))#.encode('utf-8')
                connection.send(f"{command_envio_lista}{len_lista:<{HEADER_SIZE}}{usuarios_conectados}".encode('utf-8'))

def main():
    server = Server()
    server.run()

if __name__ == "__main__":
    main()