from superbase_service import SupaBaseService
from zapi_service import ZAPIService
from decouple import UndefinedValueError
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info('Iniciando processo de envio de mensagem..')

    try:
        superbase_service = SupaBaseService()
        zapi_service = ZAPIService()

        contacts = superbase_service.get_contacts()

        for contac in contacts:
            name = contac.get('nome_contato')
            phone = contac.get('numero_telefone')
            zapi_service.send_greeting_message(contact_name=name, phone_number=phone)
    
    except Exception as e:
        logging.critical(f'Ocorreu um erro inesperado: {e}')
    except UndefinedValueError:
        logging.critical('Execução interrompida...')

    logging.info('Processo Finalizado')

if __name__ == '__main__':
    main()