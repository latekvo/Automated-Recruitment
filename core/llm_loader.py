import os

from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_google_genai import ChatGoogleGenerativeAI
from enum import Enum


class Models(Enum):
    GOOGLE = "gemini-pro"
    OLLAMA = "internlm2"


model = Models.GOOGLE


def get_key():
    if model == Models.GOOGLE:
        api_key = os.environ["GOOGLE_API_KEY"]
    elif model == Models.OLLAMA:
        api_key = None
    else:
        api_key = None

    return api_key


def get_llm():
    if model == Models.GOOGLE:
        return ChatGoogleGenerativeAI(model=Models.GOOGLE)
    elif model == Models.OLLAMA:
        return OllamaFunctions(model=Models.OLLAMA, format="json")
    else:
        raise Exception
