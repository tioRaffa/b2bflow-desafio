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
    if not phone_number or not isinstance(phone_number, str):
        return False
    
    regex = r"^55[1-9]{2}9\d{8}$"
    if re.match(regex, phone_number):
        return True
    else:
        return False


class SupaBaseService:
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
                return None
            
            all_contacts = response.data
            valid_contacs = []

            logging.info(f'{len(all_contacts)} contatos encontrados')

            for contact in all_contacts:
                name = contact.get('nome_contato')
                phone = contact.get('numero_telefone')

                if is_valid_name(name) and is_valid_br_number(phone):
                    valid_contacs.append(contact)
                else:
                    logging.warning(f'Informaçoes de contato invalida: {name} - {phone}')

            
            logging.info(f'Validação concluida. {len(valid_contacs)} de {len(all_contacts)} são validos.')
            return valid_contacs
        
        except Exception as e:
            logging.error(f'Erro ao buscar contatos no supa base {e}')
            return None