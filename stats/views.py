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

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Partido, SofascoreStatsJugador, FbrefStatsJugador
from .serializers import SofascoreStatsJugadorSerializer, FbrefStatsJugadorSerializer

class EventoDetailView(APIView):
    def get(self, request, evento_id):
        partido = Partido.objects.get(id_sofascore_evento=evento_id)
        fbref_stats = FbrefStatsJugador.objects.filter(partido=partido)
        
        sofascore_stats_local = SofascoreStatsJugador.objects.filter(partido=partido, equipo=partido.equipo_local)
        sofascore_stats_visitante = SofascoreStatsJugador.objects.filter(partido=partido, equipo=partido.equipo_visitante)

        fbref_stats_local = fbref_stats.filter(partido=partido,equipo=partido.equipo_local)
        fbref_stats_visitante = fbref_stats.filter(partido=partido,equipo=partido.equipo_visitante)

        combined_stats_local = self.combine_stats(sofascore_stats_local, fbref_stats_local)
        combined_stats_visitante = self.combine_stats(sofascore_stats_visitante, fbref_stats_visitante)

        response_data = {
            "equipo_local": partido.equipo_local.nombre,
            "equipo_visitante": partido.equipo_visitante.nombre,
            "puntuacion_local": partido.puntuacion_local,
            "puntuacion_visitante": partido.puntuacion_visitante,
            "combinated_stats_local": combined_stats_local,
            "combinated_stats_visitante": combined_stats_visitante,
        }
        
        return Response(response_data)

    def combine_stats(self, sofascore_stats, fbref_stats):
        combined_stats = []
        fbref_dict = {stat.player.id: stat for stat in fbref_stats}

        for sofascore_stat in sofascore_stats:
            player_id = sofascore_stat.player.id
            fbref_stat = fbref_dict.get(player_id)

            combined_stats.append({
                "player": sofascore_stat.player.nombre,
                "numero_camiseta": sofascore_stat.numero_camiseta,
                "suplente": sofascore_stat.suplente,
                "total_pases": sofascore_stat.total_pases,
                "pases_precisos": sofascore_stat.pases_precisos,
                "total_balones_en_largo": sofascore_stat.total_balones_en_largo,
                "balones_en_largo_completados": sofascore_stat.balones_en_largo_completados,
                "total_centros": sofascore_stat.total_centros,
                "centros_completados": sofascore_stat.centros_completados,
                "duelos_aereos_perdidos": sofascore_stat.duelos_aereos_perdidos,
                "duelos_aereos_ganados": sofascore_stat.duelos_aereos_ganados,
                "minutos_jugados": sofascore_stat.minutos_jugados,
                "duelos_perdidos": sofascore_stat.duelos_perdidos,
                "duelos_ganados": sofascore_stat.duelos_ganados,
                "tiros_fuera": sofascore_stat.tiros_fuera,
                "tiros_dentro": sofascore_stat.tiros_dentro,
                "goles": sofascore_stat.goles,
                "sofascore_rating": sofascore_stat.sofascore_rating,
                "perdida_de_posesion": sofascore_stat.perdida_de_posesion,
                "fouls": sofascore_stat.fouls,
                "total_tackle": sofascore_stat.total_tackle,
                "dispossessed": sofascore_stat.dispossessed,
                "total_offside": sofascore_stat.total_offside,
                "touches": sofascore_stat.touches,
                "key_pass": sofascore_stat.key_pass,
                "was_fouled": sofascore_stat.was_fouled,
                "total_contest": sofascore_stat.total_contest,
                "won_contest": sofascore_stat.won_contest,
                "total_clearance": sofascore_stat.total_clearance,
                "interception_won": sofascore_stat.interception_won,
                "big_chance_missed": sofascore_stat.big_chance_missed,
                "blocked_scoring_attempt": sofascore_stat.blocked_scoring_attempt,
                "big_chance_created": sofascore_stat.big_chance_created,
                "outfielder_block": sofascore_stat.outfielder_block,
                "challenge_lost": sofascore_stat.challenge_lost,
                "goal_assist": sofascore_stat.goal_assist,
                "captain": sofascore_stat.captain,
                "hit_woodwork": sofascore_stat.hit_woodwork,
                "penalty_won": sofascore_stat.penalty_won,
                "expected_goals": sofascore_stat.expected_goals,
                "expected_assists": sofascore_stat.expected_assists,
                "own_goals": sofascore_stat.own_goals,
                "error_lead_to_a_shot": sofascore_stat.error_lead_to_a_shot,
                "error_lead_to_a_goal": sofascore_stat.error_lead_to_a_goal,
                "total_keeper_sweeper": sofascore_stat.total_keeper_sweeper,
                "accurate_keeper_sweeper": sofascore_stat.accurate_keeper_sweeper,
                "saved_shots_from_inside_the_box": sofascore_stat.saved_shots_from_inside_the_box,
                "saves": sofascore_stat.saves,
                "punches": sofascore_stat.punches,
                "good_high_claim": sofascore_stat.good_high_claim,
                "goals_prevented": sofascore_stat.goals_prevented,
                # Fbref Stats
                "Min": fbref_stat.Min if fbref_stat else None,
                "Gls": fbref_stat.Gls if fbref_stat else None,
                "Ast": fbref_stat.Ast if fbref_stat else None,
                "Sh": fbref_stat.Sh if fbref_stat else None,
                "SoT": fbref_stat.SoT if fbref_stat else None,
                "CrdY": fbref_stat.CrdY if fbref_stat else None,
                "CrdR": fbref_stat.CrdR if fbref_stat else None,
                "Fls": fbref_stat.Fls if fbref_stat else None,
                "Fld": fbref_stat.Fld if fbref_stat else None,
                "Off": fbref_stat.Off if fbref_stat else None,
                "Crs": fbref_stat.Crs if fbref_stat else None,
                "TklW": fbref_stat.TklW if fbref_stat else None,
                "Int": fbref_stat.Int if fbref_stat else None,
                "OG": fbref_stat.OG if fbref_stat else None,
                "PKatt": fbref_stat.PKatt if fbref_stat else None,
                "PKwon": fbref_stat.PKwon if fbref_stat else None,
                "PK": fbref_stat.PK if fbref_stat else None,
                "PKcon": fbref_stat.PKcon if fbref_stat else None,
                "Pos": fbref_stat.Pos if fbref_stat else None,
                "edad_dia_partido": fbref_stat.edad_dia_partido if fbref_stat else None,
                "nation": fbref_stat.nation if fbref_stat else None,
                "fbref_player_id": fbref_stat.fbref_player_id if fbref_stat else None,
            })

        return combined_stats

class JugadoresStatsView(APIView):
    def get(self, request):
        partidos = Partido.objects.all()
        combined_stats = []

        for partido in partidos:
            fbref_stats = FbrefStatsJugador.objects.filter(partido=partido)
            sofascore_stats_local = SofascoreStatsJugador.objects.filter(partido=partido, equipo=partido.equipo_local)
            sofascore_stats_visitante = SofascoreStatsJugador.objects.filter(partido=partido, equipo=partido.equipo_visitante)

            fbref_stats_local = fbref_stats.filter(equipo=partido.equipo_local)
            fbref_stats_visitante = fbref_stats.filter(equipo=partido.equipo_visitante)

            combined_stats_local = self.combine_stats(sofascore_stats_local, fbref_stats_local)
            combined_stats_visitante = self.combine_stats(sofascore_stats_visitante, fbref_stats_visitante)

            combined_stats.extend(combined_stats_local)
            combined_stats.extend(combined_stats_visitante)

        return Response(combined_stats)

    def combine_stats(self, sofascore_stats, fbref_stats):
        combined_stats = []
        fbref_dict = {stat.player.id: stat for stat in fbref_stats}

        for sofascore_stat in sofascore_stats:
            player_id = sofascore_stat.player.id
            fbref_stat = fbref_dict.get(player_id)

            combined_stats.append({
                "player": sofascore_stat.player.nombre,
                "numero_camiseta": sofascore_stat.numero_camiseta,
                "suplente": sofascore_stat.suplente,
                "total_pases": sofascore_stat.total_pases,
                "pases_precisos": sofascore_stat.pases_precisos,
                "total_balones_en_largo": sofascore_stat.total_balones_en_largo,
                "balones_en_largo_completados": sofascore_stat.balones_en_largo_completados,
                "total_centros": sofascore_stat.total_centros,
                "centros_completados": sofascore_stat.centros_completados,
                "duelos_aereos_perdidos": sofascore_stat.duelos_aereos_perdidos,
                "duelos_aereos_ganados": sofascore_stat.duelos_aereos_ganados,
                "minutos_jugados": sofascore_stat.minutos_jugados,
                "duelos_perdidos": sofascore_stat.duelos_perdidos,
                "duelos_ganados": sofascore_stat.duelos_ganados,
                "tiros_fuera": sofascore_stat.tiros_fuera,
                "tiros_dentro": sofascore_stat.tiros_dentro,
                "goles": sofascore_stat.goles,
                "sofascore_rating": sofascore_stat.sofascore_rating,
                "perdida_de_posesion": sofascore_stat.perdida_de_posesion,
                "fouls": sofascore_stat.fouls,
                "total_tackle": sofascore_stat.total_tackle,
                "dispossessed": sofascore_stat.dispossessed,
                "total_offside": sofascore_stat.total_offside,
                "touches": sofascore_stat.touches,
                "key_pass": sofascore_stat.key_pass,
                "was_fouled": sofascore_stat.was_fouled,
                "total_contest": sofascore_stat.total_contest,
                "won_contest": sofascore_stat.won_contest,
                "total_clearance": sofascore_stat.total_clearance,
                "interception_won": sofascore_stat.interception_won,
                "big_chance_missed": sofascore_stat.big_chance_missed,
                "blocked_scoring_attempt": sofascore_stat.blocked_scoring_attempt,
                "big_chance_created": sofascore_stat.big_chance_created,
                "outfielder_block": sofascore_stat.outfielder_block,
                "challenge_lost": sofascore_stat.challenge_lost,
                "goal_assist": sofascore_stat.goal_assist,
                "captain": sofascore_stat.captain,
                "hit_woodwork": sofascore_stat.hit_woodwork,
                "penalty_won": sofascore_stat.penalty_won,
                "expected_goals": sofascore_stat.expected_goals,
                "expected_assists": sofascore_stat.expected_assists,
                "own_goals": sofascore_stat.own_goals,
                "error_lead_to_a_shot": sofascore_stat.error_lead_to_a_shot,
                "error_lead_to_a_goal": sofascore_stat.error_lead_to_a_goal,
                "total_keeper_sweeper": sofascore_stat.total_keeper_sweeper,
                "accurate_keeper_sweeper": sofascore_stat.accurate_keeper_sweeper,
                "saved_shots_from_inside_the_box": sofascore_stat.saved_shots_from_inside_the_box,
                "saves": sofascore_stat.saves,
                "punches": sofascore_stat.punches,
                "good_high_claim": sofascore_stat.good_high_claim,
                "goals_prevented": sofascore_stat.goals_prevented,
                # Fbref Stats
                "Min": fbref_stat.Min if fbref_stat else None,
                "Gls": fbref_stat.Gls if fbref_stat else None,
                "Ast": fbref_stat.Ast if fbref_stat else None,
                "Sh": fbref_stat.Sh if fbref_stat else None,
                "SoT": fbref_stat.SoT if fbref_stat else None,
                "CrdY": fbref_stat.CrdY if fbref_stat else None,
                "CrdR": fbref_stat.CrdR if fbref_stat else None,
                "Fls": fbref_stat.Fls if fbref_stat else None,
                "Fld": fbref_stat.Fld if fbref_stat else None,
                "Off": fbref_stat.Off if fbref_stat else None,
                "Crs": fbref_stat.Crs if fbref_stat else None,
                "TklW": fbref_stat.TklW if fbref_stat else None,
                "Int": fbref_stat.Int if fbref_stat else None,
                "OG": fbref_stat.OG if fbref_stat else None,
                "PKatt": fbref_stat.PKatt if fbref_stat else None,
                "PKwon": fbref_stat.PKwon if fbref_stat else None,
                "PK": fbref_stat.PK if fbref_stat else None,
                "PKcon": fbref_stat.PKcon if fbref_stat else None,
                "Pos": fbref_stat.Pos if fbref_stat else None,
                "edad_dia_partido": fbref_stat.edad_dia_partido if fbref_stat else None,
                "nation": fbref_stat.nation if fbref_stat else None,
                "fbref_player_id": fbref_stat.fbref_player_id if fbref_stat else None,
            })

        return combined_stats