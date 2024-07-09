from django.urls import path
from .views import get_all_torneos, get_torneo_partidos, get_evento_data

urlpatterns = [
    path('torneos/', get_all_torneos, name='get_all_torneos'),
    path('torneo/<int:torneo_id>/partidos/', get_torneo_partidos, name='get_torneo_partidos'),
    path('evento/<int:evento_id>/', get_evento_data, name='get_evento_data'),
]
