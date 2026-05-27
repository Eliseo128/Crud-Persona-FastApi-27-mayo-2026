"""
schemas.py — Esquemas de validación de Pydantic (V2 compatible).
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class PersonaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    edad: int = Field(..., ge=0, le=120)
    email: EmailStr


class PersonaCreate(PersonaBase):
    pass


class PersonaUpdate(PersonaBase):
    pass


class PersonaOut(PersonaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
