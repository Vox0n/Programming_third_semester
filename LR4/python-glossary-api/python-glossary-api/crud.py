from sqlalchemy.orm import Session
import schemas
import models


def get_terms(db: Session, skip: int = 0, limit: int = 100):
    """Получить все термины"""
    return db.query(models.GlossaryTerm).offset(skip).limit(limit).all()

def get_term(db: Session, term_id: int):
    """Получить термин по ID"""
    return db.query(models.GlossaryTerm).filter(models.GlossaryTerm.id == term_id).first()

def get_term_by_name(db: Session, term: str):
    """Получить термин по названию"""
    return db.query(models.GlossaryTerm).filter(models.GlossaryTerm.term == term).first()

def create_term(db: Session, term: schemas.GlossaryTermCreate):
    """Создать новый термин"""
    db_term = models.GlossaryTerm(**term.dict())
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    return db_term

def update_term(db: Session, term_id: int, term_update: schemas.GlossaryTermUpdate):
    """Обновить существующий термин"""
    db_term = get_term(db, term_id)
    if db_term:
        update_data = term_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_term, key, value)
        db.commit()
        db.refresh(db_term)
    return db_term

def delete_term(db: Session, term_id: int):
    """Удалить термин"""
    db_term = get_term(db, term_id)
    if db_term:
        db.delete(db_term)
        db.commit()
        return True
    return False