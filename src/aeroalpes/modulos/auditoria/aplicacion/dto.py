from dataclasses import dataclass, field
from aeroalpes.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class RequisitoDTO(DTO):
    codigo: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    obligatorio: str = field(default_factory=bool)

@dataclass(frozen=True)
class RegulacionDTO(DTO):
    id: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    region: str = field(default_factory=str)
    version: str = field(default_factory=str)
    requisitos: list[RequisitoDTO] = field(default_factory=list)
    fecha_actualizacion: str = field(default_factory=str)    
    