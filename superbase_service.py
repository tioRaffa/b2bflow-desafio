from decouple import config, UndefinedValueError
from supabase import create_client, Client
import logging
import re


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_valid_name(name):
    if not name or not name.strip():
        return False
    return True

def is_valid_br_number(phone_number):
    """
    Valida se o número de telefone fornecido é um número de celular brasileiro válido no formato internacional.
    Um número de celular brasileiro válido deve:
    - Ser uma string iniciada pelo código do país '55'
    - Ser seguido por um DDD de dois dígitos (de 11 a 99)
    - Ser seguido pelo dígito '9'
    - Ser seguido por mais 8 dígitos
    Args:
        phone_number (str): O número de telefone a ser validado.
    Returns:
        bool: True se o número corresponder ao formato esperado de celular brasileiro, False caso contrário.
    """
    if not phone_number or not isinstance(phone_number, str):
        return False
    
    regex = r"^55[1-9]{2}9\d{8}$"
    return bool(re.match(regex, phone_number))


class SupaBaseService:
    """
    Classe responsável por gerenciar a integração com o serviço Supabase para operações relacionadas a contatos.
    Métodos
    -------
    __init__():
        Inicializa o serviço Supabase, carregando as credenciais a partir das variáveis de ambiente ou arquivo .env.
        Em caso de falha ao encontrar as credenciais, registra um erro e interrompe a execução.
    
    get_contacts():
        Busca todos os contatos armazenados na tabela 'contatos' do Supabase, retornando apenas aqueles que possuem nome e número de telefone válidos.
        Realiza validação dos dados e registra logs informativos e de advertência conforme necessário.
        Retorna uma lista de contatos válidos ou uma lista vazia em caso de erro ou ausência de dados.
    """
    
    def __init__(self):
        try:
            supabase_url = config('SUPABASE_URL')
            supabase_key = config('SUPABASE_KEY')
        except UndefinedValueError:
            logging.error('Credenciais do Supabase não foram encontradas no arquivo .env ou nas variáveis de ambiente.')
            raise

        self.client: Client = create_client(supabase_key=supabase_key, supabase_url=supabase_url)
        logging.info('Serviço Supabase iniciado com sucesso.')

    
    def get_contacts(self):
        try:
            logging.info('Buscando contatos na supabase..')
            response = self.client.table('contatos').select('nome_contato, numero_telefone').execute()

            if not response.data:
                return []
            
            all_contacts = response.data
            valid_contacts = []

            logging.info(f'{len(all_contacts)} contatos encontrados')

            for contact in all_contacts:
                name = contact.get('nome_contato')
                phone = contact.get('numero_telefone')

                if is_valid_name(name) and is_valid_br_number(phone):
                    valid_contacts.append(contact)
                else:
                    logging.warning(f'Informaçoes de contato invalida: {name} - {phone}')

            
            logging.info(f'Validação concluida. {len(valid_contacts)} de {len(all_contacts)} são validos.')
            return valid_contacts
        
        except Exception as e:
            logging.error(f'Erro ao buscar contatos no supa base {e}')
            return []