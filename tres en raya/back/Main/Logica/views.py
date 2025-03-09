from django.db import models
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
# Create your models here.

def Crear_Obtener_Agente(booly):
  if not booly:
    jugador_1, created = Agente.objects.get_or_create(nombre = 'Agente_A', defaults = {'variacion' : 0.5, 'prob_exploracion' : 0.5, 'exploracion' : True})
    jugador_2, created = Agente.objects.get_or_create(nombre = 'Humano', defaults = {'maquina' : False, 'variacion' : 0.5, 'prob_exploracion' : 0.5, 'exploracion' : True})
  else:
    jugador_1, created = Agente.objects.get_or_create(nombre = 'Humano', defaults = {'maquina' : False, 'variacion' : 0.5, 'prob_exploracion' : 0.5, 'exploracion' : True})
    jugador_2, created = Agente.objects.get_or_create(nombre = 'Agente_B', defaults = {'variacion' : 0.5, 'prob_exploracion' : 0.5, 'exploracion' : True})
  return jugador_1, jugador_2

def prueba(request):
  print("llega hasta aquí")
  print("Headers recibidos en Django:", request.headers)
  if request.method == "POST":
      return JsonResponse({"status": "ok"})
  return JsonResponse({"error": "Solo se aceptan POST"}, status=400)

def cookies(request):
  csrf_token = get_token(request)  # Obtén el token CSRF
  response = JsonResponse({'status': 'Respuestas'})
  response.set_cookie('csrftoken', csrf_token)  # Establece la cookie CSRF
  return response

def iniciar_partida(request):
  partidas = Juego_Humano.objects.all()
  partidas.delete()
  data = json.loads(request.body)
  jugador_1, jugador_2 = Crear_Obtener_Agente(data['primero'])
  daty = {
    'jugador_1': jugador_1,
    'jugador_2': jugador_2,
    'rondas_max': data['rondas_max'],
  }
  partida = Juego_Humano.objects.create(**daty)
  partida.Inicio_Partida()
  datos = partida.Partida()
  datos['Id'] = partida.id
  return JsonResponse(datos)

def realizar_jugada(request):
  try:
    data = json.loads(request.body)
    print(data)
    partida = Juego_Humano.objects.get(id=data['id'])
    datos = partida.Partida(data)
    datos['Id'] = partida.id
    return JsonResponse(datos)
  except Exception as e:
    return JsonResponse({'status':'error', 'mensaje':str(e)})

def reset_partida(request):
  data = json.loads(request.body)
  partida = Juego_Humano.objects.get(id=data['id'])
  partida.Inicio_Partida()
  datos = partida.Partida()
  datos['Id']=partida.id
  return JsonResponse(datos)

def crear_agente(request):
  data = json.loads(request.body)
  agente = Agente.objects.create(**data)
  return JsonResponse({'id':agente.id})

def partida_entrenamiento(request):
  data = json.loads(request.body)
  _, Agente_B = Crear_Obtener_Agente(True)
  Agente_A, _ = Crear_Obtener_Agente(False)
  data['jugador_1_ia'] = Agente_A
  data['jugador_2_ia'] = Agente_B
  entrenamiento = Juego_Entrenamiento.objects.create(**data)
  datos = entrenamiento.Partida()
  return JsonResponse(datos)

def fin_partida(request):
  data = json.loads(request.body)
  partida = Juego_Humano.objects.get(id=data['id'])
  partida.delete()
  return JsonResponse({'status':'ok'})
