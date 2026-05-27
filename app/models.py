"""
models.py — Definición de los modelos ORM de SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String
from app.database import Base


class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
