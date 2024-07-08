import pandas as pd
pd.set_option('display.max_columns', None)
import requests
import ScraperFC as sfc
import traceback
import html5lib
from bs4 import BeautifulSoup
import lxml
from datetime import datetime, timezone
import unicodedata
import pytz
import copy
from django.core.management.base import BaseCommand
from stats.models import Partido, Equipo, Torneo, SofascoreStatsJugador, FbrefStatsJugador, Player, HeatMapPlayerMatch, ManagerTeamPartido
import time

# Zona horaria de Chile
chile_tz = pytz.timezone('America/Santiago')

equipo_mapping = {
    'everton-de-vina-del-mar': 'everton',
    "o'higgins": 'ohiggins',
    'union-la-calera': 'la-calera',
}

# Funciones
def extract_event_info(event):
    extracted_info = {
        "id_evento": event['id'],
        "Torneo": event['tournament']['uniqueTournament']['name'],
        "Torneo Sofascore Id": event['season']['id'],  # Actualizado para tomar el id de la temporada
        "Temporada": event['season']['name'],
        "Año de Temporada": event['season']['year'],
        "Ronda": event['roundInfo']['round'],
        "Estado": event['status']['description'],
        "Equipo Local": event['homeTeam']['name'],
        "Equipo Local Id": event['homeTeam']['id'],
        "Equipo Visitante": event['awayTeam']['name'],
        "Equipo Visitante Id": event['awayTeam']['id'],
        "Puntuación Local": event['homeScore'].get('current', 0),
        "Puntuación Visitante": event['awayScore'].get('current', 0),
        "Goles en Tiempo Normal Local": event['homeScore'].get('normaltime', 0),
        "Goles en Tiempo Normal Visitante": event['awayScore'].get('normaltime', 0),
        "Comienzo del Periodo Actual": event['time'].get('currentPeriodStartTimestamp', 0),
        "Inicio del Partido": event.get('startTimestamp', 0)
    }
    print("Extracted Info:", extracted_info)  # Añadir una línea de depuración aquí
    return extracted_info

def timestamp_to_date(timestamp):
    dt = datetime.fromtimestamp(timestamp, tz=chile_tz)
    day = dt.strftime('%d').lstrip('0')
    return dt.strftime(f'%B-{day}-%Y')

def normalize_text(text):
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    return text.lower().replace(" ", "-")

def map_equipo(nombre):
    nombre_normalizado = normalize_text(nombre)
    if nombre_normalizado in equipo_mapping:
        return equipo_mapping[nombre_normalizado]
    return nombre_normalizado

def encontrar_enlaces(partidos, enlaces):
    enlaces_copia = copy.deepcopy(enlaces)
    enlaces_usados = set()
    for partido in partidos:
        equipo_local = map_equipo(partido['Equipo Local'])
        equipo_visitante = map_equipo(partido['Equipo Visitante'])
        fecha_partido = timestamp_to_date(partido['Comienzo del Periodo Actual'])
        enlace_encontrado = None
        
        partido['fecha_partido'] = fecha_partido

        for enlace in enlaces_copia:
            enlace_normalizado = enlace.lower()
            if equipo_local in enlace_normalizado and fecha_partido.lower() in enlace_normalizado:
                enlace_encontrado = enlace
                enlaces_usados.add(enlace)
                enlaces_copia.remove(enlace)
                break
        
        if not enlace_encontrado:
            for enlace in enlaces_copia:
                enlace_normalizado = enlace.lower()
                if equipo_visitante in enlace_normalizado and fecha_partido.lower() in enlace_normalizado:
                    enlace_encontrado = enlace
                    enlaces_usados.add(enlace)
                    enlaces_copia.remove(enlace)
                    break
        
        partido['enlace'] = enlace_encontrado

    enlaces_sin_partido = [enlace for enlace in enlaces_copia  if enlace not in enlaces_usados]
    return partidos, enlaces_sin_partido

def get_or_create_equipo(sofascore_id, nombre):
    equipo, created = Equipo.objects.get_or_create(sofascore_id=sofascore_id, defaults={'nombre': nombre})
    if created:
        print(f"Equipo creado: {nombre} (ID: {sofascore_id})")
    return equipo

def get_or_create_torneo(nombre, sofascore_id, nombre_temporada, año_temporada):
    torneo, created = Torneo.objects.get_or_create(
        sofascore_id=sofascore_id,
        defaults={
            'nombre': nombre,
            'nombre_temporada': nombre_temporada,
            'año_temporada': año_temporada
        }
    )
    if created:
        print(f"Torneo creado: {nombre} - {nombre_temporada} ({año_temporada})")
    return torneo

def eventInfoToDatabase(evento):
    # Convertir timestamps a objetos datetime
    comienzo_periodo_actual = datetime.fromtimestamp(evento['Comienzo del Periodo Actual'])
    inicio_partido = datetime.fromtimestamp(evento['Inicio del Partido'])

    # Obtener o crear equipos
    equipo_local = get_or_create_equipo(evento['Equipo Local Id'], evento['Equipo Local'])
    equipo_visitante = get_or_create_equipo(evento['Equipo Visitante Id'], evento['Equipo Visitante'])

    # Obtener o crear torneo
    torneo = get_or_create_torneo(
        nombre=evento['Torneo'],
        sofascore_id=evento['Torneo Sofascore Id'],
        nombre_temporada=evento['Temporada'],
        año_temporada=evento['Año de Temporada']
    )

    extracted_info = {
        "id_sofascore_evento": evento['id_evento'],
        "torneo": torneo,
        "ronda": evento['Ronda'],
        "estado": evento['Estado'],
        "equipo_local": equipo_local,
        "equipo_visitante": equipo_visitante,
        "puntuacion_local": evento['Puntuación Local'],
        "puntuacion_visitante": evento['Puntuación Visitante'],
        "goles_tiempo_normal_local": evento['Goles en Tiempo Normal Local'],
        "goles_tiempo_normal_visitante": evento['Goles en Tiempo Normal Visitante'],
        "comienzo_periodo_actual": comienzo_periodo_actual,
        "inicio_partido": inicio_partido
    }
    
    partido = Partido(**extracted_info)
    partido.save()


def get_or_create_player(sofascore_id, nombre, nacionalidad, posicion, fecha_nacimiento):
    player, created = Player.objects.get_or_create(
        sofascore_id=sofascore_id,
        defaults={
            'nombre': nombre,
            'nacionalidad': nacionalidad,
            'posicion': posicion,
            'fecha_nacimiento': datetime.fromtimestamp(fecha_nacimiento)
        }
    )
    if created:
        print(f"Jugador creado: {nombre} (ID: {sofascore_id})")
    return player

def heatmapPlayerToDatabase(evento_id, player_id):
    response_heat = requests.get(f'https://api.sofascore.com/api/v1/event/{evento_id}/player/{player_id}/heatmap')
    if response_heat.status_code == 200:
        heatmap_data = response_heat.json().get('heatmap', [])
        
        player = Player.objects.get(sofascore_id=player_id)
        partido = Partido.objects.get(id_sofascore_evento=evento_id)
        
        heatmap_entry = HeatMapPlayerMatch(
            player=player,
            partido=partido,
            heatmap=heatmap_data
        )
        
        heatmap_entry.save()


def managersToDatabase(evento):
    response_managers = requests.get(f'https://api.sofascore.com/api/v1/event/{evento["id_evento"]}/managers')
    if response_managers.status_code == 200:
        managers_data = response_managers.json()
        
        partido = Partido.objects.get(id_sofascore_evento=evento['id_evento'])
        
        home_team = Equipo.objects.get(sofascore_id=evento['Equipo Local Id'])
        away_team = Equipo.objects.get(sofascore_id=evento['Equipo Visitante Id'])
        
        ManagerTeamPartido.objects.create(
            partido=partido,
            equipo=home_team,
            manager_sofascore_id=managers_data['homeManager']['id'],
            manager_name=managers_data['homeManager']['name']
        )
        
        ManagerTeamPartido.objects.create(
            partido=partido,
            equipo=away_team,
            manager_sofascore_id=managers_data['awayManager']['id'],
            manager_name=managers_data['awayManager']['name']
        )

def retrieveDataLineupsSofascore(evento):
    response = requests.get(f'https://api.sofascore.com/api/v1/event/{evento["id_evento"]}/lineups')
    if response.status_code == 200:
        players_stats = response.json()
        sofascore_teams_of_events = [players_stats['home'], players_stats['away']]
        partido = Partido.objects.get(id_sofascore_evento=evento['id_evento'])        
        for team_lineup in sofascore_teams_of_events:
            for player_info in team_lineup['players']:    
                player = player_info['player']
                try:
                    player_obj = get_or_create_player(
                        player['id'],
                        player['name'],
                        player['country']['name'],
                        player['position'],
                        player['dateOfBirthTimestamp']
                    )
                    heatmapPlayerToDatabase(evento["id_evento"], player['id'])
                    player_data = {
                        "player": player_obj,
                        "partido": partido,
                        "numero_camiseta": player_info.get('shirtNumber', 0),
                        "suplente": player_info.get('substitute', False),
                        "total_pases": player_info['statistics'].get('totalPass', 0),
                        "pases_precisos": player_info['statistics'].get('accuratePass', 0),
                        "total_balones_en_largo": player_info['statistics'].get('totalLongBalls', 0),
                        "balones_en_largo_completados": player_info['statistics'].get('accurateLongBalls', 0),
                        "total_centros": player_info['statistics'].get('totalCross', 0),
                        "centros_completados": player_info['statistics'].get('accurateCross', 0),
                        "duelos_aereos_perdidos": player_info['statistics'].get('aerialLost', 0),
                        "duelos_aereos_ganados": player_info['statistics'].get('aerialWon', 0),
                        "minutos_jugados": player_info['statistics'].get('minutesPlayed', 0),
                        "duelos_perdidos": player_info['statistics'].get('duelLost', 0),
                        "duelos_ganados": player_info['statistics'].get('duelWon', 0),
                        "tiros_fuera": player_info['statistics'].get('shotOffTarget', 0),
                        "tiros_dentro": player_info['statistics'].get('onTargetScoringAttempt', 0),
                        "goles": player_info['statistics'].get('goals', 0),
                        "sofascore_rating": player_info['statistics'].get('rating', 0),
                        "perdida_de_posesion": player_info['statistics'].get('possessionLostCtrl', 0),
                        "fouls": player_info['statistics'].get('fouls', 0),
                        "total_tackle": player_info['statistics'].get('totalTackle', 0),
                        "dispossessed": player_info['statistics'].get('dispossessed', 0),
                        "total_offside": player_info['statistics'].get('totalOffside', 0),
                        "touches": player_info['statistics'].get('touches', 0),
                        "key_pass": player_info['statistics'].get('keyPass', 0),
                        "was_fouled": player_info['statistics'].get('wasFouled', 0),
                        "total_contest": player_info['statistics'].get('totalContest', 0),
                        "won_contest": player_info['statistics'].get('wonContest', 0),
                        "total_clearance": player_info['statistics'].get('totalClearance', 0),
                        "interception_won": player_info['statistics'].get('interceptionWon', 0),
                        "big_chance_missed": player_info['statistics'].get('bigChanceMissed', 0),
                        "blocked_scoring_attempt": player_info['statistics'].get('blockedScoringAttempt', 0),
                        "big_chance_created": player_info['statistics'].get('bigChanceCreated', 0),
                        "outfielder_block": player_info['statistics'].get('outfielderBlock', 0),
                        "challenge_lost": player_info['statistics'].get('challengeLost', 0),
                        "goal_assist": player_info['statistics'].get('goalAssist', 0),
                        "captain": player_info.get('captain', False),
                        "hit_woodwork": player_info['statistics'].get('hitWoodwork', 0),
                        "penalty_won": player_info['statistics'].get('penaltyWon', 0),
                        "expected_goals": player_info['statistics'].get('expectedGoals', 0),
                        "expected_assists": player_info['statistics'].get('expectedAssists', 0),
                        "own_goals": player_info['statistics'].get('ownGoals', 0),
                        "error_lead_to_a_shot": player_info['statistics'].get('errorLeadToAShot', 0),
                        "error_lead_to_a_goal": player_info['statistics'].get('errorLeadToAGoal', 0),
                        "total_keeper_sweeper": player_info['statistics'].get('totalKeeperSweeper', 0),
                        "accurate_keeper_sweeper": player_info['statistics'].get('accurateKeeperSweeper', 0),
                        "saved_shots_from_inside_the_box": player_info['statistics'].get('savedShotsFromInsideTheBox', 0),
                        "saves": player_info['statistics'].get('saves', 0),
                        "punches": player_info['statistics'].get('punches', 0),
                        "good_high_claim": player_info['statistics'].get('goodHighClaim', 0),
                        "goals_prevented": player_info['statistics'].get('goalsPrevented', 0)
                    }

                    SofascoreStatsJugador.objects.create(**player_data)
                    time.sleep(2)
                except:
                    pass

def retrieveDataLineUpFbref(evento,scraper):
    match_stats = scraper.scrape_match(evento['enlace'])
    partido = Partido.objects.get(id_sofascore_evento=evento['id_evento'])    
    sfbref_teams_of_events = [match_stats["Away Player Stats"][0], match_stats["Home Player Stats"][0]]
    for team in sfbref_teams_of_events:
        df3 = team
        fbref_match_stats_away = df3["Summary"].values[0]
        
        fbref_match_stats_away.columns = [col[-1] for col in fbref_match_stats_away.columns.values]
        fbref_match_stats_away.rename(columns={fbref_match_stats_away.columns[-1]: 'Player ID'}, inplace=True)

        for index, row in fbref_match_stats_away.iterrows():
            try:                
                numero_camiseta = int(row['#']) if pd.notnull(row['#']) else None
                sofascore_stat = SofascoreStatsJugador.objects.get(partido=partido, numero_camiseta=numero_camiseta)            
                player = sofascore_stat.player

                FbrefStatsJugador.objects.create(
                    player=player,
                    partido=partido,
                    numero_camiseta=row['#'],
                    Min=row['Min'],
                    Gls=row['Gls'],
                    Ast=row['Ast'],
                    Sh=row['Sh'],
                    SoT=row['SoT'],
                    CrdY=row['CrdY'],
                    CrdR=row['CrdR'],
                    Fls=row['Fls'],
                    Fld=row['Fld'],
                    Off=row['Off'],
                    Crs=row['Crs'],
                    TklW=row['TklW'],
                    Int=row['Int'],
                    OG=row['OG'],
                    PKatt=row['PKatt'],
                    PKwon=row['PKwon'],
                    PK=row['PK'],
                    PKcon=row['PKcon'],
                    Pos=row['Pos'],
                    edad_dia_partido=row['Age'],
                    nation=row['Nation'],
                    fbref_player_id=row['Player ID']
                )
            except SofascoreStatsJugador.DoesNotExist:
                print(f"Estadística de jugador no encontrada para el partido {evento['id_evento']} y camiseta {row['#']}")
            except Partido.DoesNotExist:
                print(f"Partido con ID {evento['id_evento']} no encontrado")
            except Exception as e:
                print(f"Error al guardar las estadísticas del jugador: {e}")

class Command(BaseCommand):
    help = 'Llena la base de datos con datos iniciales'

    def handle(self, *args, **kwargs):
        scraper = sfc.FBRef()
        try:
            links_campeonato_nacional = scraper.get_match_links(2023, 'Chilean Primera Division') 
        except:    
            traceback.print_exc()
        finally:    
            scraper.close()

        partidos = []
        for i in range(1, 31):
            ronda = requests.get('https://api.sofascore.com/api/v1/unique-tournament/11653/season/48017/events/round/' + str(i)).json()
            ended_events_info = [extract_event_info(event) for event in ronda['events'] if event['status']['description'] == 'Ended']
            for event_info in ended_events_info:
                partidos.append(event_info)

        partidos_con_enlaces, enlaces_sin_partido = encontrar_enlaces(partidos, links_campeonato_nacional)

        for evento in partidos_con_enlaces:
            eventInfoToDatabase(evento)     
            time.sleep(2)       
            retrieveDataLineupsSofascore(evento)
            retrieveDataLineUpFbref(evento,scraper)
            managersToDatabase(evento)
