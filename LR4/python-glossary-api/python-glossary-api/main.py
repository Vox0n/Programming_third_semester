from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List

import crud, models, schemas
from database import SessionLocal, engine, get_db
from create_tables import create_tables

# Создаем таблицы при запуске
create_tables()

# Создаем приложение FastAPI
app = FastAPI(
    title="Python Glossary API",
    description="API для глоссария терминов Python",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.get("/", include_in_schema=False)
def read_root():
    """Перенаправление на документацию"""
    return RedirectResponse(url="/docs")


@app.get("/terms", response_model=List[schemas.GlossaryTerm])
def read_terms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех терминов"""
    terms = crud.get_terms(db, skip=skip, limit=limit)
    return terms


@app.get("/terms/{term_id}", response_model=schemas.GlossaryTerm)
def read_term(term_id: int, db: Session = Depends(get_db)):
    """Получить информацию о термине по ID"""
    term = crud.get_term(db, term_id=term_id)
    if term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    return term


@app.get("/terms/search/{term_name}", response_model=schemas.GlossaryTerm)
def read_term_by_name(term_name: str, db: Session = Depends(get_db)):
    """Получить информацию о термине по названию"""
    term = crud.get_term_by_name(db, term=term_name)
    if term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    return term


@app.post("/terms", response_model=schemas.GlossaryTerm, status_code=status.HTTP_201_CREATED)
def create_new_term(term: schemas.GlossaryTermCreate, db: Session = Depends(get_db)):
    """Добавить новый термин"""
    # Проверяем, не существует ли уже термин
    db_term = crud.get_term_by_name(db, term=term.term)
    if db_term:
        raise HTTPException(status_code=400, detail="Term already exists")
    return crud.create_term(db=db, term=term)


@app.put("/terms/{term_id}", response_model=schemas.GlossaryTerm)
def update_existing_term(term_id: int, term: schemas.GlossaryTermUpdate, db: Session = Depends(get_db)):
    """Обновить существующий термин"""
    db_term = crud.update_term(db, term_id=term_id, term_update=term)
    if db_term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    return db_term


@app.delete("/terms/{term_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_term(term_id: int, db: Session = Depends(get_db)):
    """Удалить термин"""
    success = crud.delete_term(db, term_id=term_id)
    if not success:
        raise HTTPException(status_code=404, detail="Term not found")
    return None


# Добавляем начальные данные при первом запуске
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже данные
        existing_terms = crud.get_terms(db)
        if not existing_terms:
            # Добавляем примеры терминов Python
            initial_terms = [
                schemas.GlossaryTermCreate(
                    term="Variable",
                    definition="A named location in memory used to store data",
                    category="Basics",
                    example="x = 5"
                ),
                schemas.GlossaryTermCreate(
                    term="Function",
                    definition="A block of code that performs a specific task",
                    category="Basics",
                    example="def greet(name):\n    return f'Hello {name}'"
                ),
                schemas.GlossaryTermCreate(
                    term="List",
                    definition="An ordered, mutable collection of items",
                    category="Data Structures",
                    example="my_list = [1, 2, 3, 'apple']"
                ),
                schemas.GlossaryTermCreate(
                    term="Dictionary",
                    definition="An unordered collection of key-value pairs",
                    category="Data Structures",
                    example="my_dict = {'name': 'John', 'age': 30}"
                ),
                schemas.GlossaryTermCreate(
                    term="Class",
                    definition="A blueprint for creating objects",
                    category="OOP",
                    example="class Dog:\n    def __init__(self, name):\n        self.name = name"
                )
            ]

            for term_data in initial_terms:
                crud.create_term(db, term_data)

            db.commit()
            print("Initial glossary terms added successfully!")
    finally:
        db.close()