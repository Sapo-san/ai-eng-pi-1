'''
Logging del PI
'''
import logging
from datetime import datetime
import os

# Crear nombre dinámico del archivo: log-YYYY-MM-DD.txt
fecha = datetime.now().strftime("%Y-%m-%d")
nombre_archivo = f"log-{fecha}.txt"

LOG_FOLDER = os.getenv('LOG_FOLDER')
LOG_CONFIG = os.getenv('LOG_CONFIG')

if LOG_FOLDER and LOG_CONFIG:
    if LOG_CONFIG not in ('print', 'file', 'both', 'none'):
        raise Exception('LOG_CONFIG no tiene valor correcto.')

    # Guardarlo en carpeta logs
    os.makedirs(LOG_FOLDER, exist_ok=True)
    ruta_log = os.path.join(LOG_FOLDER, nombre_archivo)

    # Configuración básica
    logging.basicConfig(
        filename=ruta_log,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging_functions =  {
        'debug': logging.debug,
        'info': logging.info,
        'warning': logging.warning,
        'error': logging.error,
        'critical': logging.critical,

    }

    def log(logtxt: str, level: str = 'info'):
        '''
        Función para logging del proyecto

        Recibe logtxt como texto a loggear, opcionalmente level como el nivel de logging
        '''
        if LOG_CONFIG == 'none':
            return None

        fecha_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if LOG_CONFIG in ('print', 'both'):
            print(f'[{fecha_str} {level.upper()}] {logtxt}')
        if LOG_CONFIG in ('file', 'both'):
            logging_functions[level](logtxt)
        return
else:
    raise Exception('no estan definidas las variables de entorno LOG_FOLDER and LOG_CONFIG')