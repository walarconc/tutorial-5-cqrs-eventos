""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import Regulacion
from .reglas import MinimoUnItinerario, RutaValida
from .excepciones import TipoObjetoNoExisteEnDominioVuelosExcepcion
from aeroalpes.seedwork.dominio.repositorios import Mapeador, Repositorio
from aeroalpes.seedwork.dominio.fabricas import Fabrica
from aeroalpes.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaRegulacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        print(f"=========VALIDAR LAS REGLAS entidad : {type(obj)}")
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            regulacion: Regulacion = mapeador.dto_a_entidad(obj)
            print(f"=========VALIDAR LAS REGLAS atributos {obj.__dict__}")
            self.validar_regla(MinimoUnItinerario(reserva.itinerarios))
            [self.validar_regla(RutaValida(ruta)) for itin in reserva.itinerarios for odo in itin.odos for segmento in odo.segmentos for ruta in segmento.legs]
            
            return reserva

@dataclass
class FabricaAuditorias(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Regulacion.__class__:
            fabrica_regulacion = _FabricaRegulacion()
            return fabrica_regulacion.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioVuelosExcepcion()

