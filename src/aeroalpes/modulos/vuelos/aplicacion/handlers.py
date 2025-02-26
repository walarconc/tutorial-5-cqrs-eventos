from aeroalpes.modulos.vuelos.dominio.eventos import ReservaCreada, ReservaCancelada, ReservaAprobada, ReservaPagada
from aeroalpes.seedwork.aplicacion.handlers import Handler
from aeroalpes.modulos.vuelos.infraestructura.despachadores import Despachador

class HandlerReservaIntegracion(Handler):

    @staticmethod
    def handle_reserva_creada(evento):
        print("=============Entra handle_reserva_creada===========")
        print(evento)        
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')
        print("=============FIN handle_reserva_creada===========")

    @staticmethod
    def handle_reserva_cancelada(evento):
        print("=============Entra handle_reserva_cancelada===========")
        print(evento)        
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')
        print("=============FIN handle_reserva_cancelada===========")

    @staticmethod
    def handle_reserva_aprobada(evento):
        print("=============Entra handle_reserva_aprobada===========")
        print(evento)        
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')
        print("=============FIN handle_reserva_aprobada===========")

    @staticmethod
    def handle_reserva_pagada(evento):
        print("=============Entra handle_reserva_pagada===========")
        print(evento)        
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')
        print("=============FIN handle_reserva_pagada===========")


    
