from django.urls import path
from .views import TorneosListView, PartidosListView, EventoDetailView

urlpatterns = [
    path('torneos/', TorneosListView.as_view(), name='torneos-list'),
    path('torneo/<int:torneo_id>/partidos/', PartidosListView.as_view(), name='torneo-partidos-list'),
    path('evento/<int:evento_id>/', EventoDetailView.as_view(), name='evento-detail'),
]