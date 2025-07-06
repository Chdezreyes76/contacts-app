import pytest
from fastapi import status


def test_get_new_contact_form(client):
    """Test del formulario de nuevo contacto"""
    response = client.get("/new")
    
    assert response.status_code == status.HTTP_200_OK
    assert "Crear Contacto" in response.text
    assert '<form method="post"' in response.text
    assert 'name="name"' in response.text
    assert 'name="email"' in response.text
    assert 'name="phone"' in response.text


def test_create_contact_success(client, sample_contact_data):
    """Test de creación exitosa de contacto"""
    response = client.post("/create", data=sample_contact_data)
    
    # Debe redirigir a la página principal
    assert response.status_code == status.HTTP_200_OK  # Follow redirect
    assert "Juan Pérez" in response.text
    assert "juan.perez@example.com" in response.text


def test_create_contact_invalid_email(client):
    """Test de creación de contacto con email inválido"""
    invalid_data = {
        "name": "Test User",
        "email": "invalid-email",
        "phone": "123456789"
    }
    
    response = client.post("/create", data=invalid_data)
    
    # Debe mostrar error en el formulario
    assert response.status_code == status.HTTP_200_OK
    assert "Error de validación" in response.text


def test_create_contact_missing_data(client):
    """Test de creación de contacto con datos faltantes"""
    incomplete_data = {
        "name": "Test User",
        # Falta email y phone
    }
    
    response = client.post("/create", data=incomplete_data)
    
    # FastAPI debe rechazar la request
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_form_validation_errors_display(client):
    """Test que verifica que los errores de validación se muestran correctamente"""
    # Datos con email inválido
    invalid_data = {
        "name": "Test User",
        "email": "not-an-email",
        "phone": "123456789"
    }
    
    response = client.post("/create", data=invalid_data)
    
    assert response.status_code == status.HTTP_200_OK
    assert "Error de validación" in response.text
    # Verificar que los datos se mantienen en el formulario
    assert "Test User" in response.text
    assert "not-an-email" in response.text
    assert "123456789" in response.text
