from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Torneo, Partido, SofascoreStatsJugador, FbrefStatsJugador

def get_all_torneos(request):
    torneos = Torneo.objects.all().values('nombre', 'sofascore_id')
    return JsonResponse(list(torneos), safe=False)

def get_torneo_partidos(request, torneo_id):
    torneo = get_object_or_404(Torneo, sofascore_id=torneo_id)
    partidos = Partido.objects.filter(torneo=torneo).values(
        'id_sofascore_evento', 'equipo_local__nombre', 'equipo_visitante__nombre'
    )
    return JsonResponse(list(partidos), safe=False)

def get_evento_data(request, evento_id):
    partido = get_object_or_404(Partido, id_sofascore_evento=evento_id)
    sofascore_stats = SofascoreStatsJugador.objects.filter(partido=partido).select_related('player')
    fbref_stats = FbrefStatsJugador.objects.filter(partido=partido).select_related('player')

    data = {
        'torneo': {
            'nombre': partido.torneo.nombre,
            'nombre_temporada': partido.torneo.nombre_temporada,
            'año_temporada': partido.torneo.año_temporada
        },
        'partido': {
            'id': partido.id,
            'equipo_local': {
                'nombre': partido.equipo_local.nombre,
                'id': partido.equipo_local.id
            },
            'equipo_visitante': {
                'nombre': partido.equipo_visitante.nombre,
                'id': partido.equipo_visitante.id
            },
            'puntuacion_local': partido.puntuacion_local,
            'puntuacion_visitante': partido.puntuacion_visitante,
            'inicio_partido': partido.inicio_partido
        },
        'sofascore_stats': [
            {
                'id': stat.id,
                'player': {
                    'nombre': stat.player.nombre,
                    'id': stat.player.id
                },
                'numero_camiseta': stat.numero_camiseta,
                'minutos_jugados': stat.minutos_jugados,
                # Add other stats here
            } for stat in sofascore_stats
        ],
        'fbref_stats': [
            {
                'id': stat.id,
                'player': {
                    'nombre': stat.player.nombre,
                    'id': stat.player.id
                },
                'numero_camiseta': stat.numero_camiseta,
                'Min': stat.Min,
                # Add other stats here
            } for stat in fbref_stats
        ]
    }

    return JsonResponse(data)
