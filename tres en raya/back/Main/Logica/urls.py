from django.urls import path
from . import views

urlpatterns = [
    path('prueba/',views.prueba, name='prueba'),
    path('cookies/',views.cookies, name='cookies'),
    path('iniciar_partida/',views.iniciar_partida, name='inicio_partida'),
    path('realizar_jugada/',views.realizar_jugada, name='realizar_jugada'),
    path('reset_partida/',views.reset_partida, name='reset_partida'),
    path('crear_agente/',views.crear_agente, name='crear_agente'),
    path('partida_entrenamiento/',views.partida_entrenamiento, name='partida_entrenamiento'),
    path('fin_partida/',views.fin_partida, name='fin_partida')
]