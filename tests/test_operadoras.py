import pytest
from app import create_app
from unittest.mock import patch

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.services.operadora_service.OperadoraService')
def test_busca_operadoras(MockOperadoraService, client):
    """Testa o endpoint de busca de operadoras"""
    
    # Configurar mock
    mock_service = MockOperadoraService.return_value
    mock_service.buscar_operadoras.return_value = {
        'termo_busca': 'teste',
        'resultados': [{'nome': 'Operadora Teste'}]
    }
    
    # Fazer requisição
    response = client.get('/api/busca_operadoras?q=teste')
    
    # Verificar resultados
    assert response.status_code == 200
    assert b'teste' in response.data
    assert b'Operadora Teste' in response.data

def test_busca_operadoras_termo_curto(client):
    """Testa validação de termo muito curto"""
    response = client.get('/api/busca_operadoras?q=a')
    assert response.status_code == 400
    assert b'pelo menos 2 caracteres' in response.data