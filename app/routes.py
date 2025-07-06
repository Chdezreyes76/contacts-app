from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import ValidationError
from . import database, crud, schemas
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Variable global para override en tests
_test_db_callable = None

def get_db():
    if _test_db_callable is not None:
        # Usar callable de test si está configurado
        yield from _test_db_callable()
    else:
        # Usar sesión normal
        db = database.SessionLocal()
        try:
            yield db
        finally:
            db.close()

# Listar contactos
@router.get("/")
def read_contacts(request: Request, db: Session = Depends(get_db)):
    contacts = crud.get_contacts(db)
    return templates.TemplateResponse(request=request, name="list_contacts.html", context={"contacts": contacts})

# Formulario para crear contacto
@router.get("/new")
def create_contact_form(request: Request):
    return templates.TemplateResponse(request=request, name="form_contact.html", context={"action": "/create", "contact": None})

# Crear contacto
@router.post("/create")
def create_contact(request: Request, name: str = Form(...), email: str = Form(...), phone: str = Form(...), db: Session = Depends(get_db)):
    try:
        contact_in = schemas.ContactCreate(name=name, email=email, phone=phone)
        crud.create_contact(db, contact_in)
        return RedirectResponse(url="/", status_code=303)
    except ValidationError as e:
        # En caso de error de validación, mostrar el formulario con error
        return templates.TemplateResponse(
            request=request,
            name="form_contact.html", 
            context={
                "action": "/create",
                "contact": None,
                "error": f"Error de validación: {str(e)}",
                "name": name,
                "email": email,
                "phone": phone
            }
        )
    except Exception as e:
        # Otros errores
        return templates.TemplateResponse(
            request=request,
            name="form_contact.html", 
            context={
                "action": "/create",
                "contact": None,
                "error": f"Error: {str(e)}",
                "name": name,
                "email": email,
                "phone": phone
            }
        )

# Formulario para editar contacto
@router.get("/edit/{contact_id}")
def edit_contact_form(request: Request, contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)
    return templates.TemplateResponse(request=request, name="form_contact.html", context={"action": f"/edit/{contact_id}", "contact": contact})

# Editar contacto
@router.post("/edit/{contact_id}")
def edit_contact(request: Request, contact_id: int, name: str = Form(...), email: str = Form(...), phone: str = Form(...), db: Session = Depends(get_db)):
    try:
        contact_in = schemas.ContactUpdate(name=name, email=email, phone=phone)
        crud.update_contact(db, contact_id, contact_in)
        return RedirectResponse(url="/", status_code=303)
    except ValidationError as e:
        contact = crud.get_contact(db, contact_id)
        return templates.TemplateResponse(
            request=request,
            name="form_contact.html", 
            context={
                "action": f"/edit/{contact_id}",
                "contact": contact,
                "error": f"Error de validación: {str(e)}",
                "name": name,
                "email": email,
                "phone": phone
            }
        )

# Confirmación de borrado
@router.get("/delete/{contact_id}")
def delete_contact_confirm(request: Request, contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)
    return templates.TemplateResponse(request=request, name="confirm_delete.html", context={"contact": contact})

# Eliminar contacto
@router.post("/delete/{contact_id}")
def delete_contact(request: Request, contact_id: int, db: Session = Depends(get_db)):
    crud.delete_contact(db, contact_id)
    return RedirectResponse(url="/", status_code=303)
