from tkinter import *
import threading
import time
import random
from multiprocessing import pool

class Coche(threading.Thread):
    def __init__(self, id_coche, gasolinera):
        super().__init__()
        self.id_coche = id_coche
        self.gasolinera = gasolinera
        self.en_surtidor = False

    def run(self):
        # El coche llega a la gasolinera
        self.gasolinera.actualizar_estado(self.id_coche, False)

        # El coche solicita un surtidor
        surtidor_id = self.gasolinera.solicitar_surtidor()
        self.en_surtidor = True
        self.gasolinera.actualizar_estado(self.id_coche, True)

        # El coche está siendo atendido en el surtidor
        time.sleep(random.randint(1, 5)) # Simula el tiempo de repostaje

        # El coche deja el surtidor y se va de la gasolinera
        self.gasolinera.liberar_surtidor(surtidor_id)
        self.en_surtidor = False
        self.gasolinera.actualizar_estado(self.id_coche, False)

class Gasolinera:
    def __init__(self, num_surtidores):
        self.num_surtidores = num_surtidores
        self.surtidores = [False] * num_surtidores
        self.tiempo_inicio = None
        self.tiempo_final = None

    def solicitar_surtidor(self):
        surtidor_id = None
        while surtidor_id is None:
            for i in range(self.num_surtidores):
                if not self.surtidores[i]:
                    self.surtidores[i] = True
                    surtidor_id = i + 1
                    break
            time.sleep(0.1) # Evita el uso excesivo de CPU en el bucle de espera
        return surtidor_id

    def liberar_surtidor(self, surtidor_id):
        self.surtidores[surtidor_id - 1] = False

    def actualizar_estado(self, id_coche, en_surtidor):
        # Verifica que el id_coche esté en el rango válido de surtidores
        if id_coche > 0 and id_coche <= self.num_surtidores:
            surtidor = self.surtidores[id_coche - 1]
            if en_surtidor:
                surtidor.config(text="Surtidor {} - Ocupado".format(id_coche))
            else:
                surtidor.config(text="Surtidor {} - Libre".format(id_coche))

        # Verifica si todos los coches han finalizado
        if all(coche.en_surtidor == False for coche in self.coches):
            self.tiempo_final = time.time() # Guarda el tiempo de finalización de la simulación
            tiempo_total = self.tiempo_final - self.tiempo_inicio # Calcula el tiempo total de la simulación en segundos
            tiempo_promedio = tiempo_total / len(self.coches) # Calcula el tiempo promedio por coche
            tiempo_promedio_centisegundos = tiempo_promedio * 100 # Convierte el tiempo
