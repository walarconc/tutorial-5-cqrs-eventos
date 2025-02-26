import aeroalpes.seedwork.presentacion.api as api
import json
from aeroalpes.modulos.vuelos.aplicacion.servicios import ServicioReserva
from aeroalpes.modulos.vuelos.aplicacion.dto import ReservaDTO
from aeroalpes.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from aeroalpes.modulos.vuelos.aplicacion.mapeadores import MapeadorReservaDTOJson
from aeroalpes.modulos.vuelos.aplicacion.comandos.crear_reserva import CrearReserva
from aeroalpes.modulos.vuelos.aplicacion.queries.obtener_reserva import ObtenerReserva
from aeroalpes.seedwork.aplicacion.comandos import ejecutar_commando
from aeroalpes.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('vuelos', '/vuelos')

@bp.route('/reserva', methods=('POST',))
def reservar():
    try:
        print("===========Entra Endpoint reservar===============")
        print(request.json)
        print("===================================")
        reserva_dict = request.json

        map_reserva = MapeadorReservaDTOJson()
        reserva_dto = map_reserva.externo_a_dto(reserva_dict)

        sr = ServicioReserva()
        dto_final = sr.crear_reserva(reserva_dto)

        return map_reserva.dto_a_externo(dto_final)
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/reserva-comando', methods=('POST',))
def reservar_asincrona():
    try:
        print("===========Entra Endpoint reservar_asincrona===============")
        print(request.json)
        print("===================================")
        reserva_dict = request.json

        map_reserva = MapeadorReservaDTOJson()
        reserva_dto = map_reserva.externo_a_dto(reserva_dict)

        comando = CrearReserva(reserva_dto.fecha_creacion, reserva_dto.fecha_actualizacion, reserva_dto.id, reserva_dto.itinerarios)
        
        # TODO Reemplaze es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
