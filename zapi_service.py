from decouple import config, UndefinedValueError
import logging
import requests
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ZAPIService:
    def __init__(self):
        try:
            instance_id = config('ZAPI_INSTANCE_ID')
            token = config('ZAPI_TOKEN')
        except UndefinedValueError:
            logging.error('Credenciais da Z-API não foram encontradas no arquivo .env ou nas variáveis de ambiente.')
            raise

        self.base_url = f'https://api.z-api.io/instances/{instance_id}/token/{token}'
        self.headers = {'Content-Type': 'application/json'}
        logging.info('Serviço Z-API iniciado com sucesso.')

    def send_greeting_message(self, contact_name, phone_number):
        url = f'{self.base_url}/send-text'
        payload = {
            "phone": phone_number,
            "message": f"Olá {contact_name}, tudo bem com você?"
        }

        try:
            logging.info(f'Enviando mensagem para {contact_name} - {phone_number} ...')
            response = requests.post(url=url, json=payload, headers=self.headers)
            response.raise_for_status()
            logging.info(f'Mensagem para {contact_name} enviada com sucesso!')
            return True
        except requests.exceptions.RequestException as e:
            logging.error(f'Erro ao enviar mensagem para {contact_name}: {e}')
            return False
