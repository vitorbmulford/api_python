import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_healthcheck_endpoint(client):
    """Testa o endpoint de healthcheck"""
    response = client.get('/api/healthcheck')
    assert response.status_code == 200
    assert b'healthy' in response.data
    assert b'timestamp' in response.data