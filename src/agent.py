'''
Definición de la clase agente
'''
from log_gen import log
from openai import OpenAI

class Agent:
    '''
    Agente de soporte al cliente
    '''

    def __init__(self):
        try:
            # Cargar Prompt principal
            with open('../prompts/main_prompt.txt') as prompt_file:
                self.system_prompt = prompt_file.read()

            # Inicializar libreria de OpenAI
            self.client = OpenAI()
            self.model = 'gpt-4o-mini' # por defecto
            self.temperature = 0.2 # por defecto
        except:
            log('Falló la inicialización del agente', 'error')
    
        log('Agente inicializado exitosamente.')
        return


    def setmodel(self, model):
        '''
        cambia el modelo por defecto
        '''
        ALLOWED_MODELS = [
            'gpt-4o-mini', # por defecto
            'gpt-4o',
            'gpt-5-mini',
        ]

        if model in ALLOWED_MODELS:
            self.model = model
            log(f'Modelo cambiado a: {model}')
        else:
            raise Exception('Modelo no permitido.')

    def settemp(self, temp: float):
        if temp < 0 and temp > 1:
            raise Exception('Valor fuera de rango.')
        self.temperature = temp
        log(f'Temperatura cambiada a {self.temperature}.')


    def query_model(self, mensaje):
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": mensaje},
        ]

        print(messages)

        log('Consultando API...')

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=None, # Controla la creatividad de las respuestas
        )

        log('Respuesta de API recibida.')

        print(response.choices[0].message.content)
        return 

    
        

    








client = OpenAI()

response = client.responses.create(
    model="gpt-5.2",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
