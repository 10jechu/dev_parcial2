from sqlmodel import SQLModel, Field
from datetime import datetime
import enum

class EstadoCliente(str, enum.Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"
    ELIMINADO = "Eliminado"

class Cliente(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    email: str
    estado: EstadoCliente = EstadoCliente.ACTIVO
    premium: bool = False
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True  # Permite manejar tipos como datetime
        from_attributes = True  # Asegura que se serialicen los atributos
