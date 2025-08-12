from decouple import config, UndefinedValueError
import logging
import requests
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ZAPIService:
    """
    Classe ZAPIService
    Esta classe fornece uma interface para integração com a API Z-API, permitindo o envio de mensagens de texto via WhatsApp.
    Métodos
    -------
    __init__():
        Inicializa a instância do serviço Z-API, carregando as credenciais necessárias a partir das variáveis de ambiente ou arquivo .env.
        Em caso de ausência das credenciais, registra um erro no log e lança uma exceção.
    
    send_greeting_message(contact_name: str, phone_number: str) -> bool:
        Envia uma mensagem de saudação personalizada para o número de telefone informado.
        Parâmetros:
            contact_name (str): Nome do contato que receberá a mensagem.
            phone_number (str): Número de telefone do destinatário (incluindo DDD e código do país).
        Retorna:
            bool: True se a mensagem for enviada com sucesso, False caso ocorra algum erro.
    """

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

    def send_greeting_message(self, contact_name: str, phone_number: str):
        url = f'{self.base_url}/send-text'
        payload = {
            "phone": phone_number,
            "message": f"Olá {contact_name}, tudo bem com você?"
        }

        try:
            logging.info(f'Enviando mensagem para {contact_name} - {phone_number} ...')
            response = requests.post(url=url, data=json.dumps(payload), headers=self.headers)
            response.raise_for_status()
            logging.info(f'Mensagem para {contact_name} enviada com sucesso!')
            return True
        except requests.exceptions.RequestException as e:
            logging.error(f'Erro ao enviar mensagem para {contact_name}: {e}')
            return False
