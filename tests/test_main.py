
import pytest
from unittest.mock import patch, MagicMock
from decouple import UndefinedValueError

from main import main

@patch('main.ZAPIService')
@patch('main.SupaBaseService')
def test_main_success(MockSupaBaseService, MockZAPIService):
    """
    Testa o fluxo de sucesso da função main.
    """
    mock_supabase_instance = MockSupaBaseService.return_value
    mock_zapi_instance = MockZAPIService.return_value
    
    mock_contacts = [
        {'nome_contato': 'Contact 1', 'numero_telefone': '5511987654321'},
        {'nome_contato': 'Contact 2', 'numero_telefone': '5521912345678'}
    ]
    mock_supabase_instance.get_contacts.return_value = mock_contacts
    
    main()
    
    assert mock_supabase_instance.get_contacts.call_count == 1
    assert mock_zapi_instance.send_greeting_message.call_count == 2
    mock_zapi_instance.send_greeting_message.assert_any_call(contact_name='Contact 1', phone_number='5511987654321')
    mock_zapi_instance.send_greeting_message.assert_any_call(contact_name='Contact 2', phone_number='5521912345678')

@patch('main.ZAPIService')
@patch('main.SupaBaseService')
def test_main_no_contacts(MockSupaBaseService, MockZAPIService):
    """
    Testa o fluxo quando não há contatos retornados.
    """
    mock_supabase_instance = MockSupaBaseService.return_value
    mock_zapi_instance = MockZAPIService.return_value
    
    mock_supabase_instance.get_contacts.return_value = []
    
    main()
    
    assert mock_supabase_instance.get_contacts.call_count == 1
    assert mock_zapi_instance.send_greeting_message.call_count == 0

@patch('main.logging')
@patch('main.SupaBaseService')
def test_main_undefined_value_error(MockSupaBaseService, mock_logging):
    """
    Testa o tratamento de UndefinedValueError.
    """
    MockSupaBaseService.side_effect = UndefinedValueError()
    
    main()
    
    mock_logging.critical.assert_called_once_with('Execução interrompida...')

@patch('main.logging')
@patch('main.SupaBaseService')
def test_main_unexpected_exception(MockSupaBaseService, mock_logging):
    """
    Testa o tratamento de exceções inesperadas.
    """
    MockSupaBaseService.side_effect = Exception("Unexpected Error")
    
    main()
    
    mock_logging.critical.assert_called_once_with('Ocorreu um erro inesperado: Unexpected Error')
