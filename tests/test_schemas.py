import pytest
from pydantic import ValidationError
from app.schemas import ContactCreate, ContactUpdate, ContactOut, ContactBase


def test_contact_base_valid_data():
    """Test de validación con datos válidos"""
    contact_data = {
        "name": "Juan Pérez",
        "email": "juan@example.com",
        "phone": "123456789"
    }
    
    contact = ContactBase(**contact_data)
    assert contact.name == "Juan Pérez"
    assert contact.email == "juan@example.com"
    assert contact.phone == "123456789"


def test_contact_create_schema():
    """Test del schema ContactCreate"""
    contact_data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "555123456"
    }
    
    contact = ContactCreate(**contact_data)
    assert contact.name == "Test User"
    assert contact.email == "test@example.com"
    assert contact.phone == "555123456"


def test_contact_update_schema():
    """Test del schema ContactUpdate"""
    contact_data = {
        "name": "Updated User",
        "email": "updated@example.com",
        "phone": "999888777"
    }
    
    contact = ContactUpdate(**contact_data)
    assert contact.name == "Updated User"
    assert contact.email == "updated@example.com"
    assert contact.phone == "999888777"


def test_contact_out_schema():
    """Test del schema ContactOut con ID"""
    contact_data = {
        "id": 1,
        "name": "Output User",
        "email": "output@example.com",
        "phone": "111222333"
    }
    
    contact = ContactOut(**contact_data)
    assert contact.id == 1
    assert contact.name == "Output User"
    assert contact.email == "output@example.com"
    assert contact.phone == "111222333"


def test_invalid_email_format():
    """Test que verifica validación de email inválido"""
    contact_data = {
        "name": "Test User",
        "email": "invalid-email",  # Email inválido
        "phone": "123456789"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        ContactCreate(**contact_data)
    
    # Verificar que el error es sobre el email
    errors = exc_info.value.errors()
    assert any("email" in str(error) for error in errors)


def test_missing_required_fields():
    """Test que verifica campos requeridos faltantes"""
    # Test sin nombre
    with pytest.raises(ValidationError):
        ContactCreate(email="test@example.com", phone="123456789")
    
    # Test sin email
    with pytest.raises(ValidationError):
        ContactCreate(name="Test User", phone="123456789")
    
    # Test sin teléfono
    with pytest.raises(ValidationError):
        ContactCreate(name="Test User", email="test@example.com")



def test_contact_model_dump():
    """Test de serialización del modelo"""
    contact_data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "123456789"
    }
    
    contact = ContactCreate(**contact_data)
    dumped = contact.model_dump()
    
    assert dumped["name"] == "Test User"
    assert dumped["email"] == "test@example.com"
    assert dumped["phone"] == "123456789"


def test_contact_json_schema():
    """Test de generación de JSON schema"""
    schema = ContactCreate.model_json_schema()
    
    assert "properties" in schema
    assert "name" in schema["properties"]
    assert "email" in schema["properties"]
    assert "phone" in schema["properties"]
    assert "required" in schema
    assert "name" in schema["required"]
    assert "email" in schema["required"]
    assert "phone" in schema["required"]


@pytest.mark.parametrize("email", [
    "valid@example.com",
    "user.name@domain.co.uk",
    "test+tag@example.org",
    "123@domain.com"
])
def test_valid_email_formats(email):
    """Test con diferentes formatos de email válidos"""
    contact_data = {
        "name": "Test User",
        "email": email,
        "phone": "123456789"
    }
    
    contact = ContactCreate(**contact_data)
    assert contact.email == email


@pytest.mark.parametrize("email", [
    "invalid-email",
    "@domain.com",
    "user@",
    "user..name@domain.com",
    "user@domain",
    ""
])
def test_invalid_email_formats(email):
    """Test con diferentes formatos de email inválidos"""
    contact_data = {
        "name": "Test User",
        "email": email,
        "phone": "123456789"
    }
    
    with pytest.raises(ValidationError):
        ContactCreate(**contact_data)
