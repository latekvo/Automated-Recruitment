import os
import getpass

from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_google_genai import ChatGoogleGenerativeAI
from enum import Enum


class Models(Enum):
    GOOGLE = "gemini-pro"
    OLLAMA = "internlm2"


model = Models.GOOGLE


def get_llm():
    if model == Models.GOOGLE:
        if "GOOGLE_API_KEY" not in os.environ:
            os.environ["GOOGLE_API_KEY"] = getpass.getpass(
                "Provide your Google API Key"
            )

        return ChatGoogleGenerativeAI(model=Models.GOOGLE)
    elif model == Models.OLLAMA:
        return OllamaFunctions(model=Models.OLLAMA, format="json")
    else:
        raise Exception
