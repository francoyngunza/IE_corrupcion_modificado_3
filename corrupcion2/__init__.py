from otree.api import *

from random import randint  # Importa la función randint para generar un valor aleatorio.

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'corrupcion2'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 5
    dotacion = 50
    Ciudadano1_ROLE = 'Ciudadano1'
    Ciudadano2_ROLE = 'Ciudadano2'
    Oficial_ROLE = 'Oficial'
    Monitor_ROLE = 'Monitor'


class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    subsession.group_randomly()


class Group(BaseGroup):
    gato = models.BooleanField(initial=False)
    soborno_aceptado = models.BooleanField(initial=False)


class Player(BasePlayer):
    Pago_Jugador = models.CurrencyField()
    Ofrecer_Soborno = models.BooleanField(
        initial=False,
        choices=[
            [True, 'Ofrecer pago'],
            [False, 'No ofrecer pago']
        ]
    )

    Aceptar_Soborno = models.BooleanField(
        initial=False,
        choices=[
            [True, 'Aceptar pago'],
            [False, 'No aceptar pago']
        ]
    )

    PagoFinalAleatorio = models.CurrencyField() # Nuevo campo para el pago final aleatorio.

    # Método para calcular el pago final aleatorio.
    def calcular_pago_final(self):
        # Obtiene todos los Pago_Jugador de todas las rondas jugadas.
        pagos_anteriores = [p.Pago_Jugador for p in self.in_all_rounds()]

        # Selecciona un valor aleatorio entre los pagos anteriores.
        pago_elegido = pagos_anteriores[randint(0, len(pagos_anteriores) - 1)]

        # Suma 50 al valor elegido.
        self.PagoFinalAleatorio = (pago_elegido*0.03) +5

    p1 = models.BooleanField(
        choices=[
            [True, 'Verdadero'],
            [False, 'Falso']
        ]
    )

    p2 = models.BooleanField(
        choices=[
            [False, 'Verdadero'],
            [True, 'Solo al ciudadano 2']
        ]
    )

    p3 = models.BooleanField(
        choices=[
            [True, 'Verdadero'],
            [False, 'Falso']
        ]
    )

    p4 = models.BooleanField(
        choices=[
            [True, 'Verdadero'],
            [False, 'Falso']
        ]
    )

    p5 = models.BooleanField(
        choices=[
            [True, 'Verdadero'],
            [False, 'Falso']
        ]
    )

    p6 = models.BooleanField(
        choices=[
            [True, 'Verdadero'],
            [False, 'Falso']
        ]
    )

    p8 = models.BooleanField(
        choices=[
            [True, 'Femenino'],
            [False, 'Masculino']
        ]
    )

    p9 = models.IntegerField(label="Introduce tu edad"

                             )

    p10 = models.StringField(
        label="Selecciona tu carrera",
        choices=["Administración", "Contabilidad", "Derecho", "Economía", "Finanzas", "Ingenieria de la Información",
                 "Ingeniería Empresarial", "Marketing", "Negocios Internacionales", "Otra"]
    )

    p17 = models.StringField(
        label="Selecciona tu escala de pago UP",
        choices=["1", "2", "3", "4", "5", "6", "Prefiero no decirlo"]
    )

    p11 = models.StringField(
        label="Selecciona tu zona de residencia",
        choices=["Zona 1 (Puente Piedra, Comas, Carabayllo)",
                 "Zona 2 (Independencia, Los Olivos, San Martín de Porres)",
                 "Zona 3 (San Juan de Lurigancho)",
                 "Zona 4 (Cercado, Rímac, Breña, La Victoria)",
                 "Zona 5 (Ate, Chaclacayo, Lurigancho, Santa Anita, San Luis, El Agustino)",
                 "Zona 6 (Jesús María, Lince, Pueblo Libre, Magdalena, San Miguel)",
                 "Zona 7 (Miraflores, San Isidro, San Borja, Surco, La Molina)",
                 "Zona 8 (Surquillo, Barranco, Chorrillos, San Juan de Miraflores)",
                 "Zona 9 (Villa El Salvador, Villa María del Triunfo, Lurín, Pachacamác)",
                 "Zona 10 (Callao, Bellavista, La Perla, La Punta, Carmen de la Legua, Ventanilla",
                 "Otros"]

    )

    p12 = models.StringField(
        choices=["Derecha",
                 "Izquierda",
                 "Prefiero no decirlo"
                 ]
    )

    p13 = models.BooleanField(
        choices=[
            [True, 'Opción 1: Si sale cara gana 0, si sale sello gana 100.'],
            [False, 'Opción 2: Ganar 60 con certeza']
        ]
    )

    p14 = models.BooleanField(
        choices=[
            [True, 'Opción 1:  Si sale cara gana 0, si sale sello gana 100.'],
            [False, 'Opción 2: Ganar 50 con certeza']
        ]
    )

    p15 = models.BooleanField(
        choices=[
            [True, 'Opción 1:  Si sale cara gana 0, si sale sello gana 100.'],
            [False, 'Opción 2: Ganar 40 con certeza']
        ]
    )

    p16 = models.BooleanField(
        choices=[
            [True, 'Opción 1:  Si sale cara gana 0, si sale sello gana 100.'],
            [False, 'Opción 2: Ganar 30 con certeza']
        ]
    )

    monto_ciudadano_sinSoborno = models.IntegerField(initial=0)

    ambos_monto_ciudadano_conSoborno = models.IntegerField(initial=0)  # agregue choices, no sirve para nada
    ambos_monto_oficial_conSoborno = models.IntegerField(initial=0)

    monto_ciudadano_conSoborno = models.IntegerField(initial=0)

    monto_oficial_conSoborno = models.IntegerField(initial=0)


# PAGES


def set_payoffs(group):
    players = group.get_players()
    monitores = group.get_player_by_role(C.Monitor_ROLE)
    for player in players:
        if player.group.gato == 1:

            if player.role == C.Ciudadano1_ROLE:  # Empieza logica ciudadano1

                if player.group.soborno_aceptado == 1:
                    player.payoff = C.dotacion - cu(
                        3) + 18 - 2 * monitores.monto_ciudadano_conSoborno - 2 * monitores.ambos_monto_ciudadano_conSoborno
                    player.Pago_Jugador = player.payoff
                else:
                    player.payoff = C.dotacion - 2 * monitores.monto_ciudadano_sinSoborno
                    player.Pago_Jugador = player.payoff

            if player.role == C.Ciudadano2_ROLE:
                if player.group.soborno_aceptado == 1:
                    player.payoff = C.dotacion - cu(36)
                    player.Pago_Jugador = player.payoff
                else:
                    player.payoff = C.dotacion
                    player.Pago_Jugador = player.payoff

            if player.role == C.Oficial_ROLE:  # Empieza logica Oficial

                if player.group.soborno_aceptado == 1:
                    player.payoff = C.dotacion + cu(
                        3) + 18 - 2 * monitores.monto_oficial_conSoborno - 2 * monitores.ambos_monto_oficial_conSoborno
                    player.Pago_Jugador = player.payoff
                else:
                    player.payoff = C.dotacion
                    player.Pago_Jugador = player.payoff

            if player.role == C.Monitor_ROLE:
                player.payoff = C.dotacion - player.monto_oficial_conSoborno - player.ambos_monto_oficial_conSoborno - player.monto_ciudadano_sinSoborno - player.ambos_monto_ciudadano_conSoborno
                player.Pago_Jugador = player.payoff
        else:
            player.payoff = C.dotacion
            player.Pago_Jugador = player.payoff

        if player.round_number == C.NUM_ROUNDS:  # Verifica si es la última ronda.
               player.calcular_pago_final()  # Llama al método para calcular el pago final aleatorio.


class Control(Page):
    form_model = 'player'
    form_fields = ['p8', 'p9', 'p10', 'p17', 'p11', 'p12', 'p13', 'p14', 'p15', 'p16']
    timeout_seconds = 150

    # 5 variables.
    # 2 tipos de pregunta
    def is_displayed(self):
        # La página se mostrará si la ronda actual es menor o igual a 2
        return self.round_number <= 1


class Instrucciones(Page):
    timeout_seconds = 150

    def is_displayed(self):
        # La página se mostrará si la ronda actual es menor o igual a 2
        return self.round_number <= 1


class Instrucciones_roles(Page):
    timeout_seconds = 180

    def is_displayed(self):
        # La página se mostrará si la ronda actual es menor o igual a 2
        return self.round_number <= 1


class Comprension(Page):
    form_model = 'player'
    form_fields = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6']
    timeout_seconds = 120

    # 5 variables.
    # 2 tipos de pregunta
    def is_displayed(self):
        # La página se mostrará si la ronda actual es menor o igual a 2
        return self.round_number <= 1


class WaitPage_Ciudadano1(WaitPage):

    @staticmethod
    def is_displayed(player):
        return player.role == 'Ciudadano1'


class WaitPage_Ciudadano2(WaitPage):

    @staticmethod
    def is_displayed(player):
        return player.role == 'Ciudadano2'


class WaitPage_Oficial(WaitPage):

    @staticmethod
    def is_displayed(player):
        return player.role == 'Oficial'


class WaitPage_Monitor(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.role == 'Monitor'


class Ciudadano1(Page):
    form_model = 'player'
    form_fields = ['Ofrecer_Soborno']
    timeout_seconds = 90

    @staticmethod
    def is_displayed(player):
        return player.role == 'Ciudadano1'


class Ciudadano2(Page):
    form_model = 'player'
    timeout_seconds = 20

    @staticmethod
    def is_displayed(player):
        return player.role == 'Ciudadano2'


class WaitPageSoborno(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.Ofrecer_Soborno == False

    def after_all_players_arrive(group: Group):
        for p in group.get_players():
            if p.id_in_group == 1:
                group.gato = p.Ofrecer_Soborno


class Oficial(Page):
    form_model = 'player'
    form_fields = ['Aceptar_Soborno']
    timeout_seconds = 90

    @staticmethod
    def is_displayed(player):
        return player.group.gato and player.role == 'Oficial'


class WaitPageAceptarSoborno(WaitPage):

    @staticmethod
    def is_displayed(player):
        return player.Ofrecer_Soborno == False

    def is_displayed(player):
        group = player.group
        return group.gato

    def after_all_players_arrive(group: Group):
        for p in group.get_players():
            if p.id_in_group == 3:
                group.soborno_aceptado = p.Aceptar_Soborno


class MonitorsinSoborno(Page):
    form_model = 'player'
    form_fields = ['monto_ciudadano_sinSoborno']
    timeout_seconds = 90

    @staticmethod
    def is_displayed(player):
        group = player.group
        return (not player.group.soborno_aceptado) and player.role == 'Monitor' and group.gato


class MonitorconSoborno(Page):
    form_model = 'player'
    form_fields = ['ambos_monto_ciudadano_conSoborno', 'ambos_monto_oficial_conSoborno', 'monto_oficial_conSoborno',
                   'monto_ciudadano_conSoborno',

                   ]
    timeout_seconds = 90

    @staticmethod
    def is_displayed(player):
        group = player.group
        return player.group.soborno_aceptado and player.role == 'Monitor' and group.gato


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Resultados(Page):
    timeout_seconds = 15
    @staticmethod
    def vars_for_template(player):
        player_payoff = player.Pago_Jugador

        return dict(
            player_payoff = player_payoff
        )

class Final(Page):

    @staticmethod
    def vars_for_template(player):
        player_payoff = Player.PagoFinalAleatorio
        return dict(
            player_payoff = player_payoff
        )
    def is_displayed(player):
        return player.round_number >= 5
    

page_sequence = [  # Control,
    # Instrucciones,
    # Instrucciones_roles,
    # Comprension,
    WaitPage_Ciudadano2,
    WaitPage_Oficial,
    WaitPage_Monitor,
    Ciudadano1,
    Ciudadano2,
    # ResultadosSinSoborno,
    WaitPageSoborno,
    WaitPage_Ciudadano1,
    WaitPage_Ciudadano2,
    WaitPage_Monitor,
    Oficial,
    WaitPageAceptarSoborno,
    WaitPage_Ciudadano1,
    WaitPage_Ciudadano2,
    WaitPage_Oficial,
    MonitorsinSoborno,
    MonitorconSoborno,
    ResultsWaitPage,
    Resultados,
    Final]
