import pulsar
from pulsar.schema import *

from aeroalpes.modulos.vuelos.infraestructura.schema.v1.eventos import EventoReservaCreada, ReservaCreadaPayload
from aeroalpes.modulos.vuelos.infraestructura.schema.v1.comandos import ComandoCrearReserva, ComandoCrearReservaPayload
from aeroalpes.seedwork.infraestructura import utils

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        print("======ENTRAAAAAA _publicar_mensaje EN PULSAR:")
        print(mensaje)
        print(topico)
        print(schema)
        print("======ENTRAAAAAA _publicar_mensaje EN PULSAR:")
        print(mensaje)
        print(topico)
        print(schema)
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoReservaCreada))
        publicador.send(mensaje)
        cliente.close()
        print("======FINNNNN _publicar_mensaje")
        print("======FINNNNN _publicar_mensaje")

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        print("======ENTRAAAAAA-publicar_evento EN PULSAR")
        print(evento)
        print(topico)
        payload = ReservaCreadaPayload(
            id_reserva=str(evento.id_reserva), 
            id_cliente=str(evento.id_cliente), 
            estado=str(evento.estado), 
            fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
        )
        evento_integracion = EventoReservaCreada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoReservaCreada))
        print("======FINNNNN publicar_evento")
        print("======FINNNNN publicar_evento")

    def publicar_comando(self, comando, topico):
        print("======ENTRAAAAAA publicar_comando EN PULSAR")
        print(comando)
        print(topico)
        print("======ENTRAAAAAA publicar_comando EN PULSAR")
        print(comando)
        print(topico)
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = ComandoCrearReservaPayload(
            id_usuario=str(comando.id_usuario)
            # agregar itinerarios
        )
        comando_integracion = ComandoCrearReserva(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearReserva))
        print("======FINNNNN publicar_comando")
        print("======FINNNNN publicar_comando")
