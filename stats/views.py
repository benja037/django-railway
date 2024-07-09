from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Torneo, Partido, SofascoreStatsJugador, FbrefStatsJugador
from .serializers import TorneoSerializer, PartidoSerializer, SofascoreStatsJugadorSerializer, FbrefStatsJugadorSerializer

class TorneosListView(APIView):
    def get(self, request):
        torneos = Torneo.objects.all()
        serializer = TorneoSerializer(torneos, many=True)
        return Response(serializer.data)

class PartidosListView(APIView):
    def get(self, request, torneo_id):
        partidos = Partido.objects.filter(torneo__sofascore_id=torneo_id)
        serializer = PartidoSerializer(partidos, many=True)
        return Response(serializer.data)

class EventoDetailView(APIView):
    def get(self, request, evento_id):
        partido = Partido.objects.get(id_sofascore_evento=evento_id)
        sofascore_stats = SofascoreStatsJugador.objects.filter(partido=partido)
        fbref_stats = FbrefStatsJugador.objects.filter(partido=partido)
        
        response_data = {
            "equipo_local": partido.equipo_local.nombre,
            "equipo_visitante": partido.equipo_visitante.nombre,
            "sofascore_stats": SofascoreStatsJugadorSerializer(sofascore_stats, many=True).data,
            "fbref_stats": FbrefStatsJugadorSerializer(fbref_stats, many=True).data,
        }
        
        return Response(response_data)
    