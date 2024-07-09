from rest_framework import serializers
from .models import Torneo, Partido, SofascoreStatsJugador, FbrefStatsJugador

class TorneoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torneo
        fields = '__all__'

class PartidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partido
        fields = '__all__'

class SofascoreStatsJugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SofascoreStatsJugador
        fields = '__all__'

class FbrefStatsJugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FbrefStatsJugador
        fields = '__all__'
