from superbase_service import SupaBaseService
from zapi_service import ZAPIService
from decouple import UndefinedValueError
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    """
    Função principal responsável por iniciar o processo de envio de mensagens.
    Esta função executa as seguintes etapas:
    1. Inicializa os serviços SupaBaseService e ZAPIService.
    2. Recupera a lista de contatos do SupaBaseService.
    3. Para cada contato, obtém o nome e o número de telefone e envia uma mensagem de saudação utilizando o ZAPIService.
    4. Registra logs informativos sobre o início e o fim do processo.
    5. Em caso de erro inesperado ou de valor indefinido, registra logs críticos.
    Exceções tratadas:
    - Exception: Captura erros inesperados durante a execução.
    - UndefinedValueError: Captura interrupções devido a valores indefinidos.
    """

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