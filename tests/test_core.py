import pytest
from unittest.mock import patch, MagicMock
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

from agent import Agent


# ----------------------------------------
# Fixtures
# ----------------------------------------

@pytest.fixture
def agente():
    """Instancia fresh de Core para cada test."""
    return Agent()

# ----------------------------------------
# Tests estructurales básicos
# ----------------------------------------

def test_agent_instance_creation(agente):
    """El objeto debe crearse sin errores."""
    assert isinstance(agente, Agent)


def test_agent_default_settings(agente):
    """configs por defecto correctas"""

    # Modelo
    assert isinstance(agente.model, str)
    assert agente.model == 'gpt-4o-mini'
    
    # Temp
    assert isinstance(agente.temperature, float)
    assert agente.temperature == 0.2

# ----------------------------------------
# Tests funcionales deterministas
# ----------------------------------------

def test_change_settings(agente):
    """
    Test simple determinista.
    Ajusta según tu lógica real.
    """
    agente.settemp(0.8)
    assert agente.temperature == 0.8

    agente.setmodel('gpt-5-mini')
    assert agente.model == 'gpt-5-mini'

# ----------------------------------------
# Tests de estimación de tokens
# ----------------------------------------

@pytest.mark.parametrize(
    "input_text, expected_response",
    [
        # 1
        ("hay 20 tokens en este mensaje", 20),
        # 2
        (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", 
            35
        ),
    ],
)
def test_tokens_estimates(agente, input_text, expected_response):
    agente.setmodel('gpt-4o-mini')
    agente.system_prompt = 'Test Prompt'
    
    result = agente.estimar_tokens_onetime(input_text)

    assert expected_response == result
