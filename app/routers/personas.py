"""
personas.py — Rutas de la API para el CRUD de Personas.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Persona
from app.schemas import PersonaCreate, PersonaOut, PersonaUpdate

router = APIRouter(prefix="/api/personas", tags=["Personas"])


@router.get("", response_model=list[PersonaOut])
def read_personas(db: Session = Depends(get_db)):
    return db.query(Persona).order_by(Persona.id.desc()).all()


@router.post("", response_model=PersonaOut)
def create_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    existing_persona = db.query(Persona).filter(Persona.email == persona.email).first()
    if existing_persona:
        raise HTTPException(status_code=400, detail="El email ya está registrado.")
    
    db_persona = Persona(
        nombre=persona.nombre, 
        edad=persona.edad, 
        email=persona.email
    )
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona


@router.put("/{persona_id}", response_model=PersonaOut)
def update_persona(
    persona_id: int, 
    persona: PersonaUpdate, 
    db: Session = Depends(get_db)
):
    db_persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada.")
    
    # Verificar si el email ya está en uso por otra persona
    email_owner = db.query(Persona).filter(Persona.email == persona.email, Persona.id != persona_id).first()
    if email_owner:
        raise HTTPException(status_code=400, detail="El email ya está en uso por otra persona.")

    db_persona.nombre = persona.nombre
    db_persona.edad = persona.edad
    db_persona.email = persona.email
    db.commit()
    db.refresh(db_persona)
    return db_persona


@router.delete("/{persona_id}")
def delete_persona(persona_id: int, db: Session = Depends(get_db)):
    db_persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada.")
    db.delete(db_persona)
    db.commit()
    return JSONResponse(content={"detail": "Persona eliminada"})
