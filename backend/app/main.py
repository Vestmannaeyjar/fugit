from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Contact

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    return db.query(Contact).filter(Contact.id == contact_id).first()


@app.post("/contacts/")
def create_contact(first_name: str, last_name:str, email: str, phone: str, db: Session = Depends(get_db)):
    db_contact = Contact(first_name=first_name, last_name=last_name, email=email, phone=phone)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

