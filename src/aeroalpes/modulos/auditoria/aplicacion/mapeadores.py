from aeroalpes.seedwork.aplicacion.dto import Mapeador as AppMap
from aeroalpes.seedwork.dominio.repositorios import Mapeador as RepMap
from aeroalpes.modulos.auditoria.dominio.entidades import Regulacion, Aeropuerto
from aeroalpes.modulos.auditoria.dominio.objetos_valor import Requisito, Odo, Segmento, Leg
from .dto import RequisitoDTO, RegulacionDTO
from .dto import ReservaDTO, ItinerarioDTO, OdoDTO, SegmentoDTO, LegDTO

from datetime import datetime

class MapeadorAuditoriaDTOJson(AppMap):
    def _procesar_requisito(self, requisito: dict) -> RequisitoDTO:
        return RequisitoDTO(requisito.get("codigo"), requisito.get("descripcion"), requisito.get("obligatorio"))
    
    def externo_a_dto(self, externo: dict) -> RegulacionDTO:
        reserva_dto = RegulacionDTO()

        for req in externo.get('requisitos', list()):
            reserva_dto.requisitos.append(self._procesar_requisito(req))

        return reserva_dto

    def dto_a_externo(self, dto: ReservaDTO) -> dict:
        return dto.__dict__

class MapeadorRegulacion(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def _procesar_requisito(self, requisito_dto: RequisitoDTO) -> Requisito:
        return Requisito(requisito_dto.codigo, requisito_dto.descripcion, requisito_dto.obligatorio)

    def obtener_tipo(self) -> type:
        return Reserva.__class__

    def locacion_a_dict(self, locacion):
        if not locacion:
            return dict(codigo=None, nombre=None, fecha_actualizacion=None, fecha_creacion=None)
        
        return dict(
                    codigo=locacion.codigo
                ,   nombre=locacion.nombre
                ,   fecha_actualizacion=locacion.fecha_actualizacion.strftime(self._FORMATO_FECHA)
                ,   fecha_creacion=locacion.fecha_creacion.strftime(self._FORMATO_FECHA)
        )
        

    def entidad_a_dto(self, entidad: Reserva) -> ReservaDTO:
        
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        itinerarios = list()

        for itin in entidad.itinerarios:
            odos = list()
            for odo in itin.odos:
                segmentos = list()
                for seg in odo.segmentos:
                    legs = list()
                    for leg in seg.legs:
                        fecha_salida = leg.fecha_salida.strftime(self._FORMATO_FECHA)
                        fecha_llegada = leg.fecha_llegada.strftime(self._FORMATO_FECHA)
                        origen = self.locacion_a_dict(leg.origen)
                        destino = self.locacion_a_dict(leg.destino)
                        leg = LegDTO(fecha_salida=fecha_salida, fecha_llegada=fecha_llegada, origen=origen, destino=destino)
                        
                        legs.append(leg)

                    segmentos.append(SegmentoDTO(legs))
                odos.append(OdoDTO(segmentos))
            itinerarios.append(ItinerarioDTO(odos))
        
        return ReservaDTO(fecha_creacion, fecha_actualizacion, _id, itinerarios)

    def dto_a_entidad(self, dto: RegulacionDTO) -> Regulacion:
        regulacion = Regulacion()
        regulacion.requisitos = list()

        requisitos_dto: list[RequisitoDTO] = dto.requisitos

        for req in requisitos_dto:
            regulacion.requisitos.append(self._procesar_requisito(req))
        
        return regulacion



