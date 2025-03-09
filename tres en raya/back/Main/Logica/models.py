from django.shortcuts import render
import numpy as np
from tqdm import tqdm
import os
import json
from django.conf import settings
from django.db import models

file_path = os.path.join(settings.BASE_DIR, 'Logica/JSON_IA/')

class Tablero(models.Model):
  estado = models.JSONField(default=np.zeros((3,3)).tolist())
  nombre = models.CharField(max_length=100, null=True, blank=True)

  def movimientos(self):
    return [(fila, columna) for fila in range(3) for columna in range(3) if self.estado[fila][columna] == 0]

  def jugada(self, jugador, fila, columna):
    if self.estado[fila][columna] == 0:
      self.estado[fila][columna] = jugador
      self.save()
    else:
      raise ValueError("Movimiento erroneo. Error")

  def fin_juego(self):
    estadio = np.array(self.estado)
    if (estadio.sum(axis=0) == 3).any() or (estadio.sum(axis=1) == 3).any() or (np.trace(estadio) == 3).any() or (np.trace(np.fliplr(estadio)) == 3).any():
      return 1

    if (estadio.sum(axis=0) == -3).any() or (estadio.sum(axis=1) == -3).any() or (np.trace(estadio) == -3).any() or (np.trace(np.fliplr(estadio)) == -3).any():
      return -1

    if len(self.movimientos()) == 0:
      return 0

    return None

  def reset(self):
    self.estado = np.zeros((3,3)).tolist()
    self.save()

class Agente(models.Model):
  maquina = models.BooleanField(default=True)
  simbolo = models.IntegerField(default=1)
  variacion = models.FloatField()
  prob_exploracion = models.FloatField()
  exploracion = models.BooleanField()
  nombre = models.CharField(max_length=100, unique=True)
  movimientos = models.JSONField(default=list, null=True, blank=True)

  def Simbolo_Mod(self, simbolo):
    self.simbolo = simbolo
    self.save()

  def Modificacion(self, var = None, prob_exp = None, exp = None):
    if var is not None:
      self.variacion = var
    if prob_exp is not None:
      self.prob_exploracion = prob_exp
    if exp is not None:
      self.exploracion = exp
    self.save()

  def Accion(self, tablero):
    movimientos = tablero.movimientos()
    data = self.read_json()
    if self.exploracion and np.random.uniform(0, 1) < self.prob_exploracion:
      i = np.random.choice(len(movimientos))
      return movimientos[i]
    decision = -1000
    for fila, columna in movimientos:
      estadio = np.array(tablero.estado)
      tabla = estadio.copy()
      tabla[fila][columna] = self.simbolo
      estado = str(tabla.reshape(3*3))
      valor = 0 if data.get(estado) is None else data[estado]
      if valor > decision:
        decision = valor
        fila_enviar, columna_enviar = fila, columna
    return fila_enviar, columna_enviar

  def Reset(self):
    self.movimientos = []
    self.save()

  def Update(self, tablero):

    estadio = np.array(tablero.estado)
    if str(estadio.reshape(3*3)) not in self.movimientos:
      self.movimientos.append(str(estadio.reshape(3*3)))
      self.save()

  def Recompensa(self, recompensa):
    data = self.read_json()
    for movimiento in reversed(self.movimientos):
      if data.get(movimiento) is None:
        data[movimiento] = 0
      data[movimiento] += self.variacion * (recompensa - data[movimiento])
      recompensa = data[movimiento]
    self.save_json(data)


  def crear_json(self):
    file_name = f'{self.nombre}_{self.simbolo}'
    file_path_1 = os.path.join(file_path, file_name)
    if not os.path.exists(file_path_1):
      self.save_json({})

  def read_json(self):
    try:
      file_name = f'{self.nombre}_{self.simbolo}'
      with open(os.path.join(file_path, file_name), 'r') as file:
        return json.load(file)
    except:
      try:
        self.crear_json()
        file_name = f'{self.nombre}_{self.simbolo}'
        with open(os.path.join(file_path, file_name), 'r') as file:
          return json.load(file)
      except:
        print("Error al leer el archivo")
        return None
    
  def save_json(self, data):
    try:
      file_name = f'{self.nombre}_{self.simbolo}'
      with open(os.path.join(file_path, file_name), 'w') as file:
        json.dump(data, file)
    except:
      try:
        self.crear_json()
        file_name = f'{self.nombre}_{self.simbolo}'
        with open(os.path.join(file_path, file_name), 'w') as file:
          json.dump(data, file)
      except:
        print("Error al guardar el archivo")
        return None


def Tablero_Unico():
  tablero, created = Tablero.objects.get_or_create(nombre = 'Tablero_Unico')
  return tablero


class Juego_Humano(models.Model):
  jugador_1 = models.ForeignKey(Agente, on_delete=models.CASCADE, related_name='jugador_1')
  jugador_2 = models.ForeignKey(Agente, on_delete=models.CASCADE, related_name='jugador_2')
  jugador_primero = models.BooleanField(default=True)
  tablero = models.ForeignKey(Tablero, on_delete=models.CASCADE, default=Tablero_Unico)
  vision = models.BooleanField(default=False)
  rondas_jugadas = models.IntegerField(default=0)
  rondas_max = models.IntegerField(default=2)
  puntuacion = models.JSONField(default=[0,0,0], null=True, blank=True)
  game_over = models.BooleanField(default=False)
  ganador = models.IntegerField(default=0)

  def Inicio_Partida(self):
    jugadores = [self.jugador_1, self.jugador_2]
    self.tablero.reset()
    self.rondas_jugadas += 1
    self.game_over = False
    for jugador in jugadores:
      if jugador.maquina:
        jugador.Reset()
    self.save()

  def Partida(self, data = None):
    if self.jugador_1.simbolo != 1:
      self.jugador_1.Simbolo_Mod(1)
    if self.jugador_2.simbolo != -1:
      self.jugador_2.Simbolo_Mod(-1)
    jugadores = [self.jugador_1, self.jugador_2]
    maquina = True
    while maquina and not self.game_over:
      if self.jugador_primero:
        if jugadores[0].maquina:
          movimiento = jugadores[0].Accion(self.tablero)
          self.tablero.jugada(jugadores[0].simbolo, movimiento[0], movimiento[1])
          self.jugador_primero = False
        else:
          if data is not None:
            self.tablero.jugada(jugadores[0].simbolo, data['mov_1'], data['mov_2'])
            self.jugador_primero = False
            data = None
          else:
            maquina = False
      else: 
        if jugadores[1].maquina:
          movimiento = jugadores[1].Accion(self.tablero)
          self.tablero.jugada(jugadores[1].simbolo, movimiento[0], movimiento[1])
          self.jugador_primero = True
        else:
          if data is not None:
            self.tablero.jugada(jugadores[1].simbolo, data['mov_1'], data['mov_2'])
            self.jugador_primero = True
            data = None
          else:
            maquina = False
      self.Analisis()
    self.save()
    print(self.game_over)
    return {"tablero":self.tablero.estado, "puntuacion": self.puntuacion, "rondas maximas":self.rondas_max, "game over":self.game_over, "rondas jugadas":self.rondas_jugadas, "Jugador_1":jugadores[0].nombre, "Jugador_2":jugadores[1].nombre, "Ganador":self.ganador}


  def Analisis(self):
    jugadores = [self.jugador_1, self.jugador_2]
    for jugador in jugadores:
      if jugador.maquina:
        jugador.Update(self.tablero)
    if self.tablero.fin_juego() is not None:
      self.ganador = self.tablero.fin_juego()
      self.game_over = True
      self.Recompensa()
      for i, jugador in enumerate(jugadores):
        if self.tablero.fin_juego() == jugador.simbolo:
          self.puntuacion[i] += 1
      if self.tablero.fin_juego() == 0:
        self.puntuacion[2] += 1
    self.save()


  def Recompensa(self):
    jugadores = [self.jugador_1, self.jugador_2]
    if self.tablero.fin_juego() == 0:
      for jugador in jugadores:
        if jugador.maquina:
          jugador.Recompensa(0.5)
    else:
      for jugador in jugadores:
        if jugador.maquina:
          if self.tablero.fin_juego() == jugador.simbolo:
            jugador.Recompensa(1)
          else:
            jugador.Recompensa(0)


# Principalmente usado para hacer partidas en bucle IA vs IA
class Juego_Entrenamiento(models.Model):
  jugador_1_ia = models.ForeignKey(Agente, on_delete=models.CASCADE, related_name='jugador_1_ia')
  jugador_2_ia = models.ForeignKey(Agente, on_delete=models.CASCADE, related_name='jugador_2_ia')
  tablero_ia = models.ForeignKey(Tablero, on_delete=models.CASCADE, default=Tablero_Unico)
  vision = models.BooleanField(default=False)
  victorias = models.JSONField(default=list, null=True, blank=True)
  rondas = models.IntegerField(default=50)

  def Partida(self):
    if self.jugador_1_ia.simbolo != 1:
      self.jugador_1_ia.Simbolo_Mod(1)
    if self.jugador_2_ia.simbolo != -1:
      self.jugador_2_ia.Simbolo_Mod(-1)
    jugadores = [self.jugador_1_ia, self.jugador_2_ia]
    self.victorias = [0,0,0]
    for ronda in tqdm(range(self.rondas)):
      self.tablero_ia.reset()
      for jugador in jugadores:
        if jugador.maquina:
          jugador.Reset()
      game_over = False
      while not game_over:
        for jugador in jugadores:
          movimiento_jugador = jugador.Accion(self.tablero_ia)
          jugada = self.tablero_ia.jugada(jugador.simbolo, movimiento_jugador[0], movimiento_jugador[1])
          for jugador in jugadores:
            if jugador.maquina:
              jugador.Update(self.tablero_ia)
          if self.tablero_ia.fin_juego() is not None:
            game_over = True
            break
      self.Recompensa()
      for i, jugador in enumerate(jugadores):
        if self.tablero_ia.fin_juego() == jugador.simbolo:
          self.victorias[i] += 1
      if self.tablero_ia.fin_juego() == 0:
        self.victorias[2] += 1

    return {'Victorias':self.victorias}

  def Recompensa(self):
    jugadores = [self.jugador_1_ia, self.jugador_2_ia]
    if self.tablero_ia.fin_juego() == 0:
      for jugador in jugadores:
        if jugador.maquina:
          jugador.Recompensa(0.5)
    else:
      for jugador in jugadores:
        if jugador.maquina:
          if self.tablero_ia.fin_juego() == jugador.simbolo:
            jugador.Recompensa(1)
          else:
            jugador.Recompensa(0)