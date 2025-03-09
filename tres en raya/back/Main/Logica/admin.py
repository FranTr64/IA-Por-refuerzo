from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Tablero)
admin.site.register(Agente)
admin.site.register(Juego_Humano)
admin.site.register(Juego_Entrenamiento)