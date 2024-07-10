from rest_framework import serializers
from .models import Torneo, Partido, SofascoreStatsJugador, FbrefStatsJugador, Equipo, Player

class TorneoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torneo
        fields = '__all__'

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = ['nombre']

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['nombre']

class PartidoSerializer(serializers.ModelSerializer):
    equipo_local = EquipoSerializer()
    equipo_visitante = EquipoSerializer()
    
    class Meta:
        model = Partido
        fields = '__all__'

class SofascoreStatsJugadorSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()

    class Meta:
        model = SofascoreStatsJugador
        fields = '__all__'

class FbrefStatsJugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FbrefStatsJugador
        fields = '__all__'
