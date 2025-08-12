
import pytest
from unittest.mock import patch, MagicMock
from decouple import UndefinedValueError

from supabase_service import SupaBaseService, is_valid_name, is_valid_br_number

# Testes para as funções auxiliares

@pytest.mark.parametrize("name, expected", [
    ("Valid Name", True),
    ("  Another Valid Name  ", True),
    ("", False),
    ("   ", False),
    (None, False)
])
def test_is_valid_name(name, expected):
    assert is_valid_name(name) == expected

@pytest.mark.parametrize("phone_number, expected", [
    ("5511987654321", True),
    ("5599912345678", True),
    ("551198765432", False),  # Dígitos a menos
    ("55119876543210", False), # Dígitos a mais
    ("11987654321", False),    # Sem código do país
    ("551187654321", False),   # Sem o nono dígito
    ("invalid_number", False),
    (None, False),
    (12345, False)
])
def test_is_valid_br_number(phone_number, expected):
    assert is_valid_br_number(phone_number) == expected

# Testes para a classe SupaBaseService

@patch('supabase_service.create_client')
@patch('supabase_service.config')
def test_supabase_service_init_success(mock_config, mock_create_client):
    mock_config.side_effect = ['test_url', 'test_key']
    
    service = SupaBaseService()
    
    mock_create_client.assert_called_once_with(supabase_url='test_url', supabase_key='test_key')
    assert service.client is not None

@patch('supabase_service.config')
def test_supabase_service_init_fail(mock_config):
    mock_config.side_effect = UndefinedValueError()
    
    with pytest.raises(UndefinedValueError):
        SupaBaseService()

@patch('supabase_service.create_client')
@patch('supabase_service.config')
def test_get_contacts_success(mock_config, mock_create_client):
    mock_config.side_effect = ['test_url', 'test_key']
    
    mock_response = MagicMock()
    mock_response.data = [
        {'nome_contato': 'Valid Contact 1', 'numero_telefone': '5511987654321'},
        {'nome_contato': 'Valid Contact 2', 'numero_telefone': '5521912345678'},
        {'nome_contato': 'Invalid Contact', 'numero_telefone': '12345'},
        {'nome_contato': '', 'numero_telefone': '5511987654321'},
        {'nome_contato': 'Another Invalid', 'numero_telefone': None}
    ]
    
    mock_client = MagicMock()
    mock_client.table().select().execute.return_value = mock_response
    mock_create_client.return_value = mock_client
    
    service = SupaBaseService()
    contacts = service.get_contacts()
    
    assert len(contacts) == 2
    assert contacts[0]['nome_contato'] == 'Valid Contact 1'
    assert contacts[1]['numero_telefone'] == '5521912345678'

@patch('supabase_service.create_client')
@patch('supabase_service.config')
def test_get_contacts_no_data(mock_config, mock_create_client):
    mock_config.side_effect = ['test_url', 'test_key']
    
    mock_response = MagicMock()
    mock_response.data = []
    
    mock_client = MagicMock()
    mock_client.table().select().execute.return_value = mock_response
    mock_create_client.return_value = mock_client
    
    service = SupaBaseService()
    contacts = service.get_contacts()
    
    assert contacts == []

@patch('supabase_service.logging')
@patch('supabase_service.create_client')
@patch('supabase_service.config')
def test_get_contacts_exception(mock_config, mock_create_client, mock_logging):
    mock_config.side_effect = ['test_url', 'test_key']
    
    mock_client = MagicMock()
    mock_client.table().select().execute.side_effect = Exception("Test Exception")
    mock_create_client.return_value = mock_client
    
    service = SupaBaseService()
    contacts = service.get_contacts()
    
    assert contacts == []
    mock_logging.error.assert_called_once_with('Erro ao buscar contatos no supa base Test Exception')
