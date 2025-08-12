
import pytest
from unittest.mock import patch, MagicMock
from decouple import UndefinedValueError
import requests

from zapi_service import ZAPIService

@patch('zapi_service.config')
def test_zapi_service_init_success(mock_config):
    """
    Testa se a classe ZAPIService é inicializada com sucesso
    quando as credenciais são fornecidas.
    """
    mock_config.side_effect = ['test_instance_id', 'test_token', 'test_client_token']
    
    service = ZAPIService()
    
    assert service.base_url == 'https://api.z-api.io/instances/test_instance_id/token/test_token'
    assert service.headers == {
        "content-type": "application/json",
        "client-token": "test_client_token"
    }

@patch('zapi_service.config')
def test_zapi_service_init_fail(mock_config):
    """
    Testa se a classe ZAPIService lança uma exceção
    quando as credenciais não são encontradas.
    """
    mock_config.side_effect = UndefinedValueError()
    
    with pytest.raises(UndefinedValueError):
        ZAPIService()

@patch('zapi_service.requests.post')
@patch('zapi_service.config')
def test_send_greeting_message_success(mock_config, mock_post):
    """
    Testa se o método send_greeting_message retorna True
    quando a mensagem é enviada com sucesso.
    """
    mock_config.side_effect = ['test_instance_id', 'test_token', 'test_client_token']
    
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response
    
    service = ZAPIService()
    result = service.send_greeting_message('Test Contact', '123456789')
    
    assert result is True

@patch('zapi_service.requests.post')
@patch('zapi_service.config')
def test_send_greeting_message_fail(mock_config, mock_post):
    """
    Testa se o método send_greeting_message retorna False
    quando ocorre um erro no envio da mensagem.
    """
    mock_config.side_effect = ['test_instance_id', 'test_token', 'test_client_token']
    
    mock_post.side_effect = requests.exceptions.RequestException("Test Error")
    
    service = ZAPIService()
    result = service.send_greeting_message('Test Contact', '123456789')
    
    assert result is False
