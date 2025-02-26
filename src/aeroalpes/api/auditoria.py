from aeroalpes.modulos.auditoria.aplicacion.mapeadores import MapeadorAuditoriaDTOJson
from aeroalpes.modulos.auditoria.comandos.crear_regulacion import CrearRegulacion
import aeroalpes.seedwork.presentacion.api as api
import json
from aeroalpes.modulos.vuelos.aplicacion.servicios import ServicioReserva
from aeroalpes.modulos.vuelos.aplicacion.dto import ReservaDTO
from aeroalpes.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request
from flask import Response
from aeroalpes.modulos.vuelos.aplicacion.mapeadores import MapeadorReservaDTOJson
from aeroalpes.modulos.vuelos.aplicacion.comandos.crear_reserva import CrearReserva
from aeroalpes.modulos.vuelos.aplicacion.queries.obtener_reserva import ObtenerReserva
from aeroalpes.seedwork.aplicacion.comandos import ejecutar_commando
from aeroalpes.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('auditoria', '/auditoria')

@bp.route('/auditoria-comando', methods=('POST',))
def auditoria_asincrona():
    try:
        print("===========Entra Endpoint auditoria_asincrona===============")
        print(request.json)
        print("===================================")
        regulacion_dict = request.json

        map_regulacion = MapeadorAuditoriaDTOJson()
        regulacion_dto = map_regulacion.externo_a_dto(regulacion_dict)

        comando = CrearRegulacion(regulacion_dto.id, regulacion_dto.nombre, regulacion_dto.region, regulacion_dto.version, regulacion_dto.requisitos, regulacion_dto.fecha_actualizacion)
        
        # TODO Reemplaze es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
