from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship

class Usuarios(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    direccion = Column(String(50))
    tipo = Column(String(50))
    ciudad = Column(String(50))
    estado_geo = Column(Boolean, default=False)
    cargo = Column(String(50), nullable=True)

    longitud = Column(Float)
    latitud = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'usuarios',
        'polymorphic_on': tipo
    }

class Direccion(Base):
    __tablename__ = "direcciones"
    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True, index=True)

class UsuariosConGeo(Usuarios):
    __tablename__ = "usuarios_con_geo"
    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': True,
    }

class UsuariosSinGeo(Usuarios):
    __tablename__ = "usuarios_sin_geo"
    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': False,
    }

class Vendedor(Usuarios):
    __tablename__ = "vendedor"
    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    cargo = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'vendedor',
    }

class Asesor(Vendedor):
    __tablename__ = "asesor"
    id = Column(Integer, ForeignKey("vendedor.id"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'asesor',
    }

class Cajero(Vendedor):
    __tablename__ = "cajero"
    id = Column(Integer, ForeignKey("vendedor.id"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'cajero',
    }

class Comprador(Usuarios):
    __tablename__ = "comprador"
    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'comprador',
    }