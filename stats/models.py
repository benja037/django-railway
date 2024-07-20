from django.db import models

class Equipo(models.Model):
    nombre = models.CharField(max_length=255)
    sofascore_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.nombre

class Torneo(models.Model):
    nombre = models.CharField(max_length=255)
    sofascore_id = models.IntegerField(unique=True)
    nombre_temporada = models.CharField(max_length=255)
    año_temporada = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} - {self.nombre_temporada} ({self.año_temporada})"

class Partido(models.Model):
    id = models.AutoField(primary_key=True)
    id_sofascore_evento = models.IntegerField(unique=True)
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE)
    ronda = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    equipo_local = models.ForeignKey(Equipo, related_name='partidos_local', on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(Equipo, related_name='partidos_visitante', on_delete=models.CASCADE)
    puntuacion_local = models.IntegerField()
    puntuacion_visitante = models.IntegerField()
    goles_tiempo_normal_local = models.IntegerField()
    goles_tiempo_normal_visitante = models.IntegerField()
    comienzo_periodo_actual = models.DateTimeField()
    inicio_partido = models.DateTimeField()

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante} - {self.torneo.nombre} - Ronda {self.ronda}"
    
class Player(models.Model):
    sofascore_id = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=255, null=True, blank=True)
    nacionalidad = models.CharField(max_length=255, null=True, blank=True)
    posicion = models.CharField(max_length=50, null=True, blank=True)
    fecha_nacimiento = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre if self.nombre else "Unknown Player"

class SofascoreStatsJugador(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE,null=True,default=None)
    numero_camiseta = models.IntegerField()
    suplente = models.BooleanField(default=False)
    total_pases = models.IntegerField(default=0)
    pases_precisos = models.IntegerField(default=0)
    total_balones_en_largo = models.IntegerField(default=0)
    balones_en_largo_completados = models.IntegerField(default=0)
    total_centros = models.IntegerField(default=0)
    centros_completados = models.IntegerField(default=0)
    duelos_aereos_perdidos = models.IntegerField(default=0)
    duelos_aereos_ganados = models.IntegerField(default=0)
    minutos_jugados = models.IntegerField(default=0)
    duelos_perdidos = models.IntegerField(default=0)
    duelos_ganados = models.IntegerField(default=0)
    tiros_fuera = models.IntegerField(default=0)
    tiros_dentro = models.IntegerField(default=0)
    goles = models.IntegerField(default=0)
    sofascore_rating = models.FloatField(default=0.0)
    perdida_de_posesion = models.IntegerField(default=0)
    fouls = models.IntegerField(default=0)
    total_tackle = models.IntegerField(default=0)
    dispossessed = models.IntegerField(default=0)
    total_offside = models.IntegerField(default=0)
    touches = models.IntegerField(default=0)
    key_pass = models.IntegerField(default=0)
    was_fouled = models.IntegerField(default=0)
    total_contest = models.IntegerField(default=0)
    won_contest = models.IntegerField(default=0)
    total_clearance = models.IntegerField(default=0)
    interception_won = models.IntegerField(default=0)
    big_chance_missed = models.IntegerField(default=0)
    blocked_scoring_attempt = models.IntegerField(default=0)
    big_chance_created = models.IntegerField(default=0)
    outfielder_block = models.IntegerField(default=0)
    challenge_lost = models.IntegerField(default=0)
    goal_assist = models.IntegerField(default=0)
    captain = models.BooleanField(default=False)
    hit_woodwork = models.IntegerField(default=0)
    penalty_won = models.IntegerField(default=0)
    expected_goals = models.FloatField(default=0.0)
    expected_assists = models.FloatField(default=0.0)
    own_goals = models.IntegerField(default=0)
    error_lead_to_a_shot = models.IntegerField(default=0)
    error_lead_to_a_goal = models.IntegerField(default=0)
    total_keeper_sweeper = models.IntegerField(default=0)
    accurate_keeper_sweeper = models.IntegerField(default=0)
    saved_shots_from_inside_the_box = models.IntegerField(default=0)
    saves = models.IntegerField(default=0)
    punches = models.IntegerField(default=0)
    good_high_claim = models.IntegerField(default=0)
    goals_prevented = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.player.nombre} - {self.partido}"


class FbrefStatsJugador(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    numero_camiseta = models.IntegerField()
    Min = models.IntegerField()
    Gls = models.IntegerField()
    Ast = models.IntegerField()
    Sh = models.IntegerField()
    SoT = models.IntegerField()
    CrdY = models.IntegerField()
    CrdR = models.IntegerField()
    Fls = models.IntegerField()
    Fld = models.IntegerField()
    Off = models.IntegerField()
    Crs = models.IntegerField()
    TklW = models.IntegerField()
    Int = models.IntegerField()
    OG = models.IntegerField()
    PKatt = models.IntegerField()
    PKwon = models.IntegerField()
    PK = models.IntegerField()
    PKcon = models.IntegerField()
    Pos = models.CharField(max_length=10)
    edad_dia_partido = models.CharField(max_length=20)
    nation = models.CharField(max_length=10)  # Añadido Nation
    fbref_player_id = models.CharField(max_length=100)  # Añadido Player ID

class HeatMapPlayerMatch(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    heatmap = models.JSONField()

class ManagerTeamPartido(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    manager_sofascore_id = models.IntegerField()
    manager_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Manager {self.manager_name} for team {self.equipo.nombre} in match {self.partido.id_sofascore_evento}"