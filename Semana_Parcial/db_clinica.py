
import sqlite3

class Database:
    datafile = "clinica.db"
    def __init__(self):
        # Se habilita la conexion con la dB
        self.conn = sqlite3.connect(Database.datafile)
        self.cur = self.conn.cursor()
        
        
    def __del__(self):
        # Se cierra la conexion con la dB
        self.conn.close()
        
        
    def listar_medicos(self):
        # Retorna una lista de tuplas con la informacion de los medicos
        # con el formato [(med_id, nombre, apellido), ...]
        #
        # Se utiliza para llenar la informacion de la tabla tabMedicos
        return self.cur.execute("""SELECT med_id, nombre, apellido FROM medicos
                                   ORDER by med_id ASC""").fetchall()   
    
    
    def listar_pacientes_medico(self, med_id):
        return self.cur.execute("""SELECT pacientes.pac_id, pacientes.apellido, pacientes.nombre, pacientes.altura, pacientes.edad, pacientes.sexo
                                   FROM pacientes
                                   JOIN medico_paciente
                                   JOIN medicos
                                   ON medicos.med_id = medico_paciente.med_id
                                   AND medico_paciente.pac_id = pacientes.pac_id
                                   WHERE medicos.med_id = ?
                                   ORDER BY pacientes.apellido ASC""",(med_id,)).fetchall()
        
    
    def nombre_paciente(self, id_pac):
        return self.cur.execute("""SELECT apellido, nombre
                                    FROM pacientes
                                    WHERE pac_id = ?""", (id_pac,)).fetchone()
    
    
    def data_peso(self, pac_id):
        # Retorna una lista con los pesos registrados de un paciente en el 
        # historial de pesos: [peso1, peso2, ...]
        #
        # Se utiliza para el reporte gráfico
        return self.cur.execute("""SELECT historial_pesos.peso
                                    from historial_pesos
                                    JOIN pacientes
                                    on pacientes.pac_id = historial_pesos.pac_id
                                    WHERE pacientes.pac_id = ?""", (pac_id,)).fetchall()