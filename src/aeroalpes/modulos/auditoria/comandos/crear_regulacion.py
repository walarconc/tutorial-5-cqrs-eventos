from aeroalpes.modulos.auditoria.aplicacion.dto import RegulacionDTO, RequisitoDTO
from aeroalpes.seedwork.aplicacion.comandos import Comando
from aeroalpes.modulos.vuelos.aplicacion.dto import ItinerarioDTO, ReservaDTO
from .base import CrearRegulacionBaseHandler
from dataclasses import dataclass, field
from aeroalpes.seedwork.aplicacion.comandos import ejecutar_commando as comando

from aeroalpes.modulos.vuelos.dominio.entidades import Reserva
from aeroalpes.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from aeroalpes.modulos.vuelos.aplicacion.mapeadores import MapeadorReserva
from aeroalpes.modulos.vuelos.infraestructura.repositorios import RepositorioReservas

@dataclass
class CrearRegulacion(Comando):
    id: str
    nombre: str
    region: str    
    version: str    
    requisitos: list[RequisitoDTO]
    fecha_actualizacion: str        


class CrearRegulacionHandler(CrearRegulacionBaseHandler):
    
    def handle(self, comando: CrearRegulacion):
        print("===============================ACA EJECUTA COMANDO HANDLRES FOR CrearRegulacionHandler")
        regulacion_dto = RegulacionDTO(
                id=comando.id,
                nombre=comando.nombre,
                region=comando.region,                
                version=comando.version,
                requisitos=comando.requisitos,
                fecha_actualizacion=comando.fecha_actualizacion)

        reserva: Reserva = self.fabrica_vuelos.crear_objeto(reserva_dto, MapeadorReserva())
        reserva.crear_reserva(reserva)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioReservas.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, reserva)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearRegulacion)
def ejecutar_comando_crear_regulacion(comando: CrearRegulacion):
    print("============ENTRA HANDLRES FOR CrearRegulacionHandler")
    handler = CrearRegulacionHandler()
    handler.handle(comando)
    