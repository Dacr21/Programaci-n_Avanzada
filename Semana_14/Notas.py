#%%
# COM1
import serial.tools.list_ports

ports =  serial.tools.list_ports.comports()

for port in ports:
    print(port)
#%%
import serial.tools.list_ports
ports =  serial.tools.list_ports.comports()
lis = []
for port in ports:
    idx = str(port).find(' ')
    puerto = str(port)[0:idx]
    lis.append(puerto)

lis
    

#%%
import serial

PORT = 'COM1'

try:
    #Establecer conexion con el purto serial
    print(f"Estableciendo comunicacion por {PORT}")
    ser = serial.Serial(port = PORT,
                        baudrate = 9600,
                        bytesize = 8,
                        timeout = 2,
                        stopbits=serial.STOPBITS_ONE)
    print("Conexion establecida")

    while True:
        try:
            #Si hay datos en el buffer de entradas
            if ser.in_waiting > 0:
                # Se leen los datos y esperar al caracter EOL
                data = ser.readline()
                #La data recibida son bytes y hay que convertirlos
                string = data.decode('utf-8')
                print(f"Rx: {string}")
        #Se cancela la ejecucion del programa con Ctrl + C
        except KeyboardInterrupt:
            print("Conexion cerrada")
            ser.close()
            break
except:
    print(f"Puerto [{PORT}] no esta disponible")

#%%
import serial

PORT = 'COM1'

try:
    #Establecer conexion con el purto serial
    print(f"Estableciendo comunicacion por {PORT}")
    ser = serial.Serial(port = PORT,
                        baudrate = 9600,
                        bytesize = 8,
                        timeout = 2,
                        stopbits=serial.STOPBITS_ONE)
    print("Conexion establecida")

    while True:
        #Si hay datos en el buffer de entradas
        string = input("Tx:")
        if string == "QUIT":
            break
        else:
            data = string.encode("utf-8")
            ser.write(data)

    print("Conexion cerrada")
    ser.close()
except:
    print(f"Puerto [{PORT}] no esta disponible")