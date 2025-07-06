import pytest
from sqlalchemy.exc import IntegrityError
from app.models import Contact


def test_contact_creation(test_db):
    """Test básico de creación de contacto"""
    contact = Contact(
        name="Test User",
        email="test@example.com",
        phone="123456789"
    )
    test_db.add(contact)
    test_db.commit()
    
    assert contact.id is not None
    assert contact.name == "Test User"
    assert contact.email == "test@example.com"
    assert contact.phone == "123456789"


def test_contact_unique_email_constraint(test_db):
    """Test que verifica que el email debe ser único"""
    # Crear primer contacto
    contact1 = Contact(
        name="User 1",
        email="same@example.com",
        phone="123456789"
    )
    test_db.add(contact1)
    test_db.commit()
    
    # Intentar crear segundo contacto con mismo email
    contact2 = Contact(
        name="User 2",
        email="same@example.com",  # Mismo email
        phone="987654321"
    )
    test_db.add(contact2)
    
    # Debe lanzar error de integridad
    with pytest.raises(IntegrityError):
        test_db.commit()


def test_contact_string_representation(test_db):
    """Test de representación string del modelo"""
    contact = Contact(
        name="Test User",
        email="test@example.com",
        phone="123456789"
    )
    test_db.add(contact)
    test_db.commit()
    
    # Verificar que se puede convertir a string sin errores
    str_repr = str(contact)
    assert isinstance(str_repr, str)


def test_contact_required_fields(test_db):
    """Test que verifica campos requeridos"""
    # Los campos pueden ser None en el modelo, pero Pydantic debe validar
    contact = Contact(name=None, email=None, phone=None)
    test_db.add(contact)
    
    # Esto debería funcionar a nivel de modelo (SQLAlchemy no valida por defecto)
    # La validación se hace en Pydantic
    test_db.commit()
    assert contact.id is not None


def test_contact_update(test_db):
    """Test de actualización de contacto"""
    contact = Contact(
        name="Original Name",
        email="original@example.com",
        phone="123456789"
    )
    test_db.add(contact)
    test_db.commit()
    
    # Actualizar datos
    contact.name = "Updated Name"
    contact.email = "updated@example.com"
    test_db.commit()
    
    # Verificar cambios
    updated_contact = test_db.query(Contact).filter(Contact.id == contact.id).first()
    assert updated_contact.name == "Updated Name"
    assert updated_contact.email == "updated@example.com"
    assert updated_contact.phone == "123456789"  # Sin cambios


def test_contact_deletion(test_db):
    """Test de eliminación de contacto"""
    contact = Contact(
        name="To Delete",
        email="delete@example.com",
        phone="123456789"
    )
    test_db.add(contact)
    test_db.commit()
    
    contact_id = contact.id
    
    # Eliminar contacto
    test_db.delete(contact)
    test_db.commit()
    
    # Verificar que fue eliminado
    deleted_contact = test_db.query(Contact).filter(Contact.id == contact_id).first()
    assert deleted_contact is None
