
#%%
os.chdir(r"C:\\Users\\DiegoCR\\Desktop\\2021-02\\Programacion_avanzada_de_computadoras\\Semana_5\\test")
from genericpath import exists
import os
for i in range(12):
    if not os.path.exists(f".\\test\\test{i+1}"):
        os.makedirs(f".\\test\\test{i+1}")
#%%
os.chdir(".\\test")
print(os.getcwd())

#%%
print(os.listdir())

#%%
# Archivos de texto

PATH = "C:\\Users\\DiegoCR\\Desktop\\2021-02\\Programacion_avanzada_de_computadoras\\Semana_5\\test"

with open(os.path.join(PATH, "readme.txt"), mode = 'w', encoding='utf-8') as file:
    file.write("INSTRUCCIONES\n")
    file.write("=============\n\n")
    file.write("En los directorios se tienen diferentes test a ser distribuidos\n")
    file.write("entre los diferentes alumnos")
#%%
os.chdir(r"C:\\Users\\DiegoCR\\Desktop\\2021-02\\Programacion_avanzada_de_computadoras\\Semana_5\\test")
for item in os.listdir("."):
    if os.path.isdir(item):
        print(item,"    <DIR>")
    elif os.path.isfile(item):
        print(item, "   ", os.path.getsize(item),"  bytes")

#%%
with open("readme.txt", mode = "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())

#%%
#Generador de archivos de preguntas

import random

PATH = "C:\\Users\\DiegoCR\\Desktop\\2021-02\\Programacion_avanzada_de_computadoras\\Semana_5\\test"

os.chdir(PATH)

capitales = {"Amazonas": "Chachapoyas", 
             "Áncash": "Huaraz",
             "Apurímac": "Abancay",
             "Arequipa": "Arequipa",
             "Ayacucho": "Ayacucho",
             "Cajamarca": "Cajamarca",
             "Cusco": "Cusco",
             "Huancavelica": "Huancavelica",
             "Huánuco": "Huánuco",
             "Ica": "Ica",
             "Junín": "Huancayo",
             "La Libertad": "Trujillo",
             "Lambayeque": "Chiclayo",
             "Lima": "Lima",
             "Loreto": "Iquitos",
             "Madre de Dios": "Puerto Maldonado",
             "Moquegua": "Moquegua",
             "Pasco": "Cerro de Pasco",
             "Piura": "Piura",
             "Puno": "Puno",
             "San Martín": "Moyobamba",
             "Tacna": "Tacna",
             "Tumbes": "Tumbes",
             "Ucayali": "Pucallpa"}

for quizNum in range(1,13):
    #Se crean las rutas y nombres de archivos de salida
    quizFileName = os.path.join(PATH, f"test{quizNum}", f"test{quizNum}.txt")
    answerKeyFileName = os.path.join(PATH,f"test{quizNum}",f"test{quizNum}_answer.txt")

    with open(quizFileName, mode='w', encoding='utf8') as quizFile:
        with open(answerKeyFileName, mode='w', encoding='utf8') as answerKeyFileName:

#Se crea un encabezado para el archivo de test
            quizFile.write("Nombre:\n\nFecha:\n\nPeriodo:\n\n")
            quizFile.write('    ' * 20 + f"Capitales por departamento - Test {quizNum}\n\n")

            departamentos = list(capitales.keys())
            random.shuffle(departamentos)

            for idx, departamento in enumerate(departamentos, start=1):
                correctAnswers = capitales.get(departamento)

                wrongAnswers = list(capitales.values())
                del wrongAnswers[wrongAnswers.index(correctAnswers)]
                wrongAnswers = random.sample(wrongAnswers, 3)

                answerOptions = wrongAnswers + [correctAnswers]

                random.shuffle(answerOptions)

                quizFile.write(f"{idx}. Cual es la capital de {departamento}?:\n")

                for letter, answer in zip('ABCD', answerOptions):
                    quizFile.write(f"\t{letter}. {answer}\n")
                else:
                    quizFile.write("\n")

                answerKeyFileName.write(f"{idx}. {'ABCD'[answerOptions.index(correctAnswers)]}\n")

#%%
import shelve
datos = ["A", "B", "C", "D"]
os.chdir("C:\\Users\\DiegoCR\\Desktop\\2021-02\\Programacion_avanzada_de_computadoras\\Semana_5")
with shelve.open("mis_datos") as shelve_file:
    shelve_file["datos"] = datos

#%%
with shelve.open("mis_datos") as shelve_file:
    datos = shelve_file["datos"]

#%%
