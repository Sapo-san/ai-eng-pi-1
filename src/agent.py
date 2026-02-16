'''
Definición de la clase agente
'''
from time import perf_counter
from datetime import datetime
from pathlib import Path
from os import getenv
from decimal import Decimal
import csv
from json import loads, dumps
from log_gen import log
from openai import OpenAI
import tiktoken



class Agent:
    '''
    Agente de soporte al cliente
    '''
    # Modelos permitidos
    ALLOWED_MODELS = [
        'gpt-4o-mini', # por defecto
        'gpt-4o',
        'gpt-5-mini',
    ]

    # Prices (USD) per 1M tokens
    # [15-02-2026] Fuente: https://developers.openai.com/api/docs/pricing
    MODEL_PRICING = {
        'gpt-4o-mini' : { # Modelo Barato
            'in': Decimal("0.15"),
            'out': Decimal("0.60"),
        }, 
        'gpt-4o' : { # Modelo caro, Oof
            'in': Decimal("2.50"),
            'out': Decimal("10.00"),
        },
        'gpt-5-mini' : {
            'in': Decimal("0.25"),
            'out': Decimal("2.00"),
        },
    }


    def __init__(self):
        '''
        Inicializa el modelo.
        '''
        try:
            # Inicializar libreria de OpenAI
            self.client = OpenAI()
            self.model = 'gpt-4o-mini' # por defecto
            self.temperature = 0.2 # por defecto

            # tiktoken encoder
            self.enc = tiktoken.encoding_for_model(self.model)

            # Metrics
            self.metrics = []

            # Cargar Prompt principal
            with open('../prompts/main_prompt.md') as prompt_file:
                self.system_prompt = prompt_file.read()
        except:
            log('Falló la inicialización del agente', 'error')
    
        log('Agente inicializado exitosamente.')
        return

    def setmodel(self, model):
        '''
        Establece el modelo a consultar
        '''
        
        if model in self.ALLOWED_MODELS:
            self.model = model
            log(f'Modelo cambiado a: {model}')

            # Cambiar encoder al modelo correspondiente
            self.enc = tiktoken.encoding_for_model(self.model)

        else:
            raise Exception('Modelo no permitido.')

    def settemp(self, temp: float):
        '''
        Establece la temperatura del modelo
        '''

        if temp < 0 and temp > 1:
            raise Exception('Valor fuera de rango.')
        self.temperature = temp
        log(f'Temperatura cambiada a {self.temperature}.')

    def estimar_tokens_onetime(self, texto):
        '''
        Suma la cantidad total de tokens de una única consulta al modelo
        Incluye en el cálculo el system prompt.
        '''
        # Sumar tokens
        total = 11 # Base para un único mensaje (sin memoria)
        total += len(self.enc.encode(self.system_prompt))
        total += len(self.enc.encode(texto))
        return total

    def guardar_metricas(self, timestamp, tokens_prompt, tokens_completion, tokens_total, response_time):
        '''
        guarda métricas en la memoria del agente como una lista
        
        recibe:
        - timestamp (str)
        - tokens_prompt => autoexplicativo
        - tokens_completion => tokens respuesta
        - tokens_total => suma de los dos anteriores
        - response_time => latencia

        adicionalmente, dependiendo del modelo actual, calcula el costo de la llamada en USD
        '''
        in_price = self.MODEL_PRICING[self.model]['in']
        out_price = self.MODEL_PRICING[self.model]['out']

        cost_call = ((Decimal(tokens_prompt) * in_price ) + (Decimal(tokens_completion) * out_price)) / Decimal("1000000")

        metricas_llamada = [
            timestamp,
            tokens_prompt,
            tokens_completion,
            tokens_total,
            f"{response_time:.0f}",
            f"{cost_call}USD"
        ]

        try:
            METRICS_FOLDER = str(getenv('METRICS_FOLDER'))
            
            if METRICS_FOLDER == 'None':
                raise Exception('METRICS_FOLDER inválida.')

            metrics_path = Path(METRICS_FOLDER)

            ruta = metrics_path / "metrics.csv"
            
            with ruta.open("a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)

                # Si el archivo está vacío → escribir header
                if ruta.stat().st_size == 0:
                    writer.writerow(
                        ["timestamp",
                         "tokens_prompt", 
                         "tokens_completion",
                         "tokens_total",
                         "response_time",
                         "estimated_cost_usd"]
                    )
                writer.writerow(metricas_llamada)
            
            log(f'Métricas escritas: {metricas_llamada}')

        except Exception as err:
            log(f'Error intentando escribir métricas: {err}', 'error')
            
        return

    def validar_respuesta(self, response, retries):
        try:
            
            # Si es JSON, deberia cargarse correctamente
            json_data = loads(response.output_text)

            if 'error' in json_data.keys():
                raise Exception('Respuesta devuelve json con clave de error')

            '''
            Esta parte de la verificación es dependiente del prompt
            por los campos que se especifican
            '''
            if 'chain_of_thought' not in json_data.keys():
                raise Exception('Error de formato, campo "chain_of_thought" no existe')  
            if 'opener' not in json_data.keys():
                raise Exception('Error de formato, campo "opener" no existe')
            if 'confianza' not in json_data.keys():
                raise Exception('Error de formato, campo "confianza" no existe')  

            if len(json_data['chain_of_thought']) != 3:
                raise Exception('Error de formato, CoT no tiene exactamente 3 pasos.') 
                      
            if json_data['confianza'] > 1 or json_data['confianza'] < 0:
                raise Exception('Error de formato, confianza fuera de rango')           
            
            log('Formato JSON válido de respuesta.')
            return True
            

        except Exception as err:
            log(f'Formato JSON inválido: {str(err)} | intento {retries} fallido, reintentando...', 'error')
            return False
        
    def onetime_query_model(self, mensaje: str):
        '''
        Hace una única consulta al modelo (sin memoria)

        Antes de enviar la consulta, estima la cantidad de tokens de la entrada.
        
        Al enviar la consulta, registra la cantidad de tokens totales devueltos 
        por el modelo.
        '''
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": mensaje},
        ]

        estimacion_tokens = self.estimar_tokens_onetime(mensaje)
        log(f'Tokens estimados: {estimacion_tokens}')

        logtext_mensaje = mensaje.replace("\n", "\\n")
        logtext_system_prompt = self.system_prompt.replace("\n", "\\n")

        log(f'Consultando API... | Texto consulta: {logtext_mensaje} | Main Prompt: {logtext_system_prompt}')

        valid_answer = False
        retries = 0
        while not valid_answer and retries < 3:
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            t1 = perf_counter()
            response = self.client.responses.create(
                model=self.model,
                input=messages,
                temperature=self.temperature,
            )

            t2 = perf_counter()
            response_time = (t2 - t1) * 1000
            
            # Uso
            tokens_prompt = response.usage.input_tokens
            tokens_completion = response.usage.output_tokens
            tokens_total = response.usage.total_tokens

            log(f'Respuesta de API recibida | Tiempo: {response_time:.0f} ms | Tokens - prompt: {tokens_prompt}, respuesta: {tokens_completion}, total: {tokens_total} | Respuesta: {response.output_text}')

            # Métricas
            self.guardar_metricas(timestamp, tokens_prompt, tokens_completion, tokens_total, response_time)

            # Verificar validez de respuesta (Formato JSON)
            valid_answer = self.validar_respuesta(response, retries) # Recibe retries para logging

            if not valid_answer:
                retries += 1

        if not valid_answer and retries >= 3:
            log(f'No se pudo generar una respuesta válida', 'error')
            return dumps({ 'Error': 'No se pudo generar una respuesta válida'})
        
        # Retornar texto de la respuesta si es válido
        return response.output_text