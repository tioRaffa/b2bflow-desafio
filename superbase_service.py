from decouple import config, UndefinedValueError
from supabase import create_client, Client
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SuperBaseService:
    def __init__(self):
        try:
            superbase_url = config('SUPERBASE_URL')
            superbase_key = config('SUPERBASE_KEY')
        except UndefinedValueError:
            logging.error('Credenciais do Supabase não foram encontradas no arquivo .env ou nas variáveis de ambiente.')
            raise

        self.client: Client = create_client(supabase_key=superbase_key, supabase_url=superbase_url)
        logging.info('Serviço Superbase inciado com sucesso.')

    
    def get_contacts(self):
        try:
            logging.info('Buscando contatos na superbase..')
            response = self.client.table('contatos').select('nome_contato, numero_telefone').execute()
            if response.data:
                logging.info(f'{len(response.data)} contatos encontrados')
                return response.data
            else:
                logging.warning('Nenhum contato encontrado')
                return []
        except Exception as e:
            logging.error(f'Erro ao buscar contatos no super base {e}')
            return None