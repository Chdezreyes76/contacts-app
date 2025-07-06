import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database import Base
from app.main import app
from app import routes
from app.models import Contact


# Base de datos en memoria para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_engine():
    """Crea un engine de base de datos de prueba en memoria"""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_db(test_engine):
    """Crea una sesión de base de datos de prueba"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function") 
def client():
    """Cliente de pruebas de FastAPI con base de datos de test independiente"""
    # Crear engine y tablas específicamente para este cliente
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Override de la dependencia de base de datos usando el mecanismo en routes.py
    routes._test_db_callable = override_get_db
    
    # Crear cliente de pruebas
    with TestClient(app) as test_client:
        yield test_client
    
    # Limpiar override después del test
    routes._test_db_callable = None
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_contact_data():
    """Datos de ejemplo para crear contactos"""
    return {
        "name": "Juan Pérez",
        "email": "juan.perez@example.com",
        "phone": "123456789"
    }


@pytest.fixture
def sample_contact_data_2():
    """Segundo conjunto de datos de ejemplo"""
    return {
        "name": "María García",
        "email": "maria.garcia@example.com",
        "phone": "987654321"
    }


@pytest.fixture
def created_contact(test_db, sample_contact_data):
    """Fixture que crea un contacto en la base de datos de prueba"""
    from app import crud, schemas
    
    contact_create = schemas.ContactCreate(**sample_contact_data)
    contact = crud.create_contact(test_db, contact_create)
    return contact
