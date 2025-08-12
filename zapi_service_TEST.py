from decouple import config, UndefinedValueError
import logging
import requests
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import json

class ZAPIServiceTest:
    def __init__(self):
        try:
            instance_id = config('ZAPI_INSTANCE_ID')
            token = config('ZAPI_TOKEN')
            client_token = config('CLIENT_TOKEN')
        except UndefinedValueError:
            logging.error('Credenciais da Z-API não foram encontradas no arquivo .env ou nas variáveis de ambiente.')
            raise

        self.base_url = f'https://api.z-api.io/instances/{instance_id}/token/{token}'
        self.headers = {
            "content-type": "application/json",
            "client-token": f"{client_token}"
            }
        logging.info('Serviço Z-API iniciado com sucesso.')

    def send_greeting_message(self, contact_name, phone_number):
        url = f'{self.base_url}/send-text'

        test_phone = '5549998186440'
        test_msg = 'blabalbalbal'


        payload = {
            "phone": test_phone,
            "message": test_msg
        }

        try:
            logging.info(f"Enviando MENSAGEM DE TESTE FIXA para {test_phone}...")
            response = requests.post(url, data=json.dumps(payload), headers=self.headers)
            response.raise_for_status()
            logging.info(f'Mensagem para {contact_name} enviada com sucesso!')
            return True
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao enviar mensagem de teste: {e.response.text if e.response else str(e)}")
            return False
