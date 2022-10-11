
import sqlite3

class Database:
    filename = "database.db"
    def __init__(self):
        self.comn = sqlite3.connect(Database.filename)
        self.cur = self.comn.cursor()

    def __del__(self):
        self.comn.close()

    def listar_pacientes(self):
        return self.cur.execute("""SELECT * FROM pacientes""").fetchall()

    def paciente_id(self, id_pac):
        return self.cur.execute("""SELECT nombre, peso, altura FROM pacientes WHERE id = ?""",
                                                                (id_pac)).fetchone()

    def nombres_pacientes(self, order='asc'):
        if order == 'asc':
            self.cur.execute("""SELECT nombre FROM pacientes ORDER BY nombre""")
        elif order == 'desc':
            self.cur.execute("""SELECT nombre FROM pacientes ORDER BY nombre DESC""")
        else:
            raise ValueError("""El attr 'order' puede ser 'asc p 'desc'""")
        
        return [item[0] for item in self.cur]

    def data_imc(self, nombre):
        return self.cur.execute("""SELECT peso, altura FROM pacientes WHERE nombre = ?""",(nombre,)).fetchone()
    
    def data_pacientes(self):
        return self.cur.execute("""SELECT nombre, peso, altura FROM pacientes ORDER BY nombre""").fetchall()