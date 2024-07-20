from django.contrib import admin
from .models import Equipo, Torneo, Partido, Player, SofascoreStatsJugador, FbrefStatsJugador, HeatMapPlayerMatch, ManagerTeamPartido

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sofascore_id')
    search_fields = ('nombre', 'sofascore_id')

@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sofascore_id', 'nombre_temporada', 'año_temporada')
    search_fields = ('nombre', 'sofascore_id', 'nombre_temporada', 'año_temporada')

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('id_sofascore_evento', 'torneo', 'equipo_local', 'equipo_visitante', 'puntuacion_local', 'puntuacion_visitante', 'inicio_partido')
    search_fields = ('id_sofascore_evento', 'torneo__nombre', 'equipo_local__nombre', 'equipo_visitante__nombre')
    list_filter = ('torneo', 'estado', 'inicio_partido')
    list_select_related = ('torneo', 'equipo_local', 'equipo_visitante')
    list_per_page = 20

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sofascore_id', 'nacionalidad', 'posicion', 'fecha_nacimiento')
    search_fields = ('nombre', 'sofascore_id', 'nacionalidad', 'posicion')
    list_per_page = 20

@admin.register(SofascoreStatsJugador)
class SofascoreStatsJugadorAdmin(admin.ModelAdmin):
    list_display = ('player', 'partido', 'numero_camiseta', 'total_pases', 'pases_precisos', 'total_centros', 'minutos_jugados', 'goles', 'sofascore_rating')
    search_fields = ('player__nombre', 'partido__id_sofascore_evento')
    list_filter = ('partido', 'player')
    list_select_related = ('player', 'partido')
    list_per_page = 20

@admin.register(FbrefStatsJugador)
class FbrefStatsJugadorAdmin(admin.ModelAdmin):
    list_display = ('player', 'partido', 'numero_camiseta', 'Min', 'Gls', 'Ast', 'Sh', 'SoT')
    search_fields = ('player__nombre', 'partido__id_sofascore_evento')
    list_filter = ('partido', 'player')
    list_select_related = ('player', 'partido')
    list_per_page = 20

@admin.register(HeatMapPlayerMatch)
class HeatMapPlayerMatchAdmin(admin.ModelAdmin):
    list_display = ('player', 'partido')
    search_fields = ('player__nombre', 'partido__id_sofascore_evento')
    list_filter = ('partido', 'player')
    list_select_related = ('player', 'partido')
    list_per_page = 200

@admin.register(ManagerTeamPartido)
class ManagerTeamPartidoAdmin(admin.ModelAdmin):
    list_display = ('partido', 'equipo', 'manager_name')
    search_fields = ('partido__id_sofascore_evento', 'equipo__nombre', 'manager_name')
    list_filter = ('partido', 'equipo')
    list_select_related = ('partido', 'equipo')
    list_per_page = 20
