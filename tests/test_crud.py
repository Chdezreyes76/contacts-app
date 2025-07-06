import pytest
from app import crud, schemas
from app.models import Contact


def test_create_contact(test_db, sample_contact_data):
    """Test de creación de contacto"""
    contact_create = schemas.ContactCreate(**sample_contact_data)
    contact = crud.create_contact(test_db, contact_create)
    
    assert contact.id is not None
    assert contact.name == sample_contact_data["name"]
    assert contact.email == sample_contact_data["email"]
    assert contact.phone == sample_contact_data["phone"]


def test_get_contact_by_id(test_db, created_contact):
    """Test de obtener contacto por ID"""
    contact = crud.get_contact(test_db, created_contact.id)
    
    assert contact is not None
    assert contact.id == created_contact.id
    assert contact.name == created_contact.name
    assert contact.email == created_contact.email
    assert contact.phone == created_contact.phone


def test_get_contact_nonexistent(test_db):
    """Test de obtener contacto que no existe"""
    contact = crud.get_contact(test_db, 999)
    assert contact is None


def test_get_contacts_empty(test_db):
    """Test de obtener lista de contactos cuando está vacía"""
    contacts = crud.get_contacts(test_db)
    assert contacts == []


def test_get_contacts_with_data(test_db):
    """Test de obtener lista de contactos con datos"""
    from app import schemas
    
    # Crear algunos contactos directamente
    contact1 = schemas.ContactCreate(name="Juan Pérez", email="juan@example.com", phone="123456789")
    contact2 = schemas.ContactCreate(name="María García", email="maria@example.com", phone="987654321")
    contact3 = schemas.ContactCreate(name="Carlos López", email="carlos@example.com", phone="555666777")
    
    crud.create_contact(test_db, contact1)
    crud.create_contact(test_db, contact2)
    crud.create_contact(test_db, contact3)
    
    contacts = crud.get_contacts(test_db)
    
    assert len(contacts) == 3
    contact_emails = [c.email for c in contacts]
    assert "juan@example.com" in contact_emails
    assert "maria@example.com" in contact_emails
    assert "carlos@example.com" in contact_emails


def test_update_contact_success(test_db, created_contact):
    """Test de actualización exitosa de contacto"""
    update_data = {
        "name": "Nombre Actualizado",
        "email": "nuevo@example.com",
        "phone": "999888777"
    }
    
    contact_update = schemas.ContactUpdate(**update_data)
    updated_contact = crud.update_contact(test_db, created_contact.id, contact_update)
    
    assert updated_contact is not None
    assert updated_contact.id == created_contact.id
    assert updated_contact.name == "Nombre Actualizado"
    assert updated_contact.email == "nuevo@example.com"
    assert updated_contact.phone == "999888777"


def test_update_contact_nonexistent(test_db):
    """Test de actualización de contacto que no existe"""
    update_data = {
        "name": "No Existe",
        "email": "noexiste@example.com",
        "phone": "000000000"
    }
    
    contact_update = schemas.ContactUpdate(**update_data)
    updated_contact = crud.update_contact(test_db, 999, contact_update)
    
    assert updated_contact is None


def test_update_contact_partial(test_db, created_contact):
    """Test de actualización parcial de contacto"""
    # Solo actualizar el nombre
    update_data = {
        "name": "Solo Nombre Actualizado",
        "email": created_contact.email,  # Mantener email original
        "phone": created_contact.phone   # Mantener teléfono original
    }
    
    contact_update = schemas.ContactUpdate(**update_data)
    updated_contact = crud.update_contact(test_db, created_contact.id, contact_update)
    
    assert updated_contact.name == "Solo Nombre Actualizado"
    assert updated_contact.email == created_contact.email
    assert updated_contact.phone == created_contact.phone


def test_delete_contact_success(test_db, created_contact):
    """Test de eliminación exitosa de contacto"""
    contact_id = created_contact.id
    
    deleted_contact = crud.delete_contact(test_db, contact_id)
    
    assert deleted_contact is not None
    assert deleted_contact.id == contact_id
    
    # Verificar que ya no existe
    contact = crud.get_contact(test_db, contact_id)
    assert contact is None


def test_delete_contact_nonexistent(test_db):
    """Test de eliminación de contacto que no existe"""
    deleted_contact = crud.delete_contact(test_db, 999)
    assert deleted_contact is None


def test_crud_full_cycle(test_db):
    """Test del ciclo completo CRUD"""
    # CREATE
    contact_data = {
        "name": "Ciclo Completo",
        "email": "ciclo@example.com",
        "phone": "123123123"
    }
    contact_create = schemas.ContactCreate(**contact_data)
    created = crud.create_contact(test_db, contact_create)
    
    assert created.id is not None
    
    # READ
    retrieved = crud.get_contact(test_db, created.id)
    assert retrieved.name == "Ciclo Completo"
    
    # UPDATE
    update_data = {
        "name": "Ciclo Actualizado",
        "email": "actualizado@example.com",
        "phone": "321321321"
    }
    contact_update = schemas.ContactUpdate(**update_data)
    updated = crud.update_contact(test_db, created.id, contact_update)
    
    assert updated.name == "Ciclo Actualizado"
    assert updated.email == "actualizado@example.com"
    
    # DELETE
    deleted = crud.delete_contact(test_db, created.id)
    assert deleted is not None
    
    # VERIFY DELETION
    final_check = crud.get_contact(test_db, created.id)
    assert final_check is None


def test_create_multiple_contacts(test_db):
    """Test de creación de múltiples contactos"""
    contacts_data = [
        {"name": "Usuario 1", "email": "user1@example.com", "phone": "111111111"},
        {"name": "Usuario 2", "email": "user2@example.com", "phone": "222222222"},
        {"name": "Usuario 3", "email": "user3@example.com", "phone": "333333333"}
    ]
    
    created_contacts = []
    for data in contacts_data:
        contact_create = schemas.ContactCreate(**data)
        contact = crud.create_contact(test_db, contact_create)
        created_contacts.append(contact)
    
    # Verificar que todos fueron creados
    assert len(created_contacts) == 3
    
    # Verificar que todos tienen ID único
    ids = [c.id for c in created_contacts]
    assert len(set(ids)) == 3  # Todos los IDs son únicos
    
    # Verificar que se pueden recuperar todos
    all_contacts = crud.get_contacts(test_db)
    assert len(all_contacts) == 3
