from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import requests
from dotenv import load_dotenv
import os
from groq import Groq
from openai import OpenAI


class APIConnection(ABC):
    """
    Interface base para conexões com APIs de modelos de linguagem.

    Esta classe abstrata define os métodos comuns que todas as implementações
    de conexão com API devem ter.
    """

    @abstractmethod
    def send_request(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Envia uma requisição para a API.

        Args:
            prompt (str): O texto de entrada para o modelo
            **kwargs: Argumentos adicionais específicos da API

        Returns:
            Dict[str, Any]: Resposta da API em formato de dicionário

        Raises:
            ConnectionError: Se houver falha na conexão com a API
        """
        pass

    @abstractmethod
    def get_response(self, response: Dict[str, Any]) -> str:
        """
        Processa a resposta da API e extrai o texto gerado.

        Args:
            response (Dict[str, Any]): Resposta da API em formato de dicionário

        Returns:
            str: Texto processado da resposta
        """
        pass


class BaseAPIConnection(APIConnection):
    """
    Classe base que contém a lógica comum para enviar requisições a APIs.
    """

    def __init__(self, api_key: str, model: str) -> None:
        """
        Inicializa a conexão com a API.

        Args:
            api_key (str): Chave de API
            model (str): Modelo a ser usado
        """
        self.api_key = api_key
        self.model = model

    def send_request(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Envia uma requisição para a API.

        Args:
            prompt (str): O texto de entrada para o modelo
            **kwargs: Argumentos adicionais específicos da API

        Returns:
            Dict[str, Any]: Resposta da API em formato de dicionário
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return completion
        except Exception as e:
            print(f"Erro ao enviar requisição para a API: {str(e)}")
            return {}

    def get_response(self, response: Dict[str, Any]) -> str:
        """
        Processa a resposta da API e extrai o conteúdo gerado.

        Args:
            response (Dict[str, Any]): Resposta da API em formato de dicionário

        Returns:
            str: Texto processado da resposta
        """
        try:
            return response.choices[0].message.content
        except AttributeError as e:
            print(f"Erro ao acessar atributos da resposta: {str(e)}")
            return ""
        except Exception as e:
            print(f"Erro inesperado ao processar a resposta: {str(e)}")
            return ""


class ChatGPTConnection(BaseAPIConnection):
    """
    Implementação da conexão com a API do ChatGPT.
    """

    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        """
        Inicializa a conexão com a API do ChatGPT.

        Args:
            api_key (str): Chave de API do OpenAI
            model (str, optional): Modelo a ser usado. Defaults to "gpt-4o-mini"
        """
        super().__init__(api_key, model)
        self.client = OpenAI(api_key=api_key)


class GroqConnection(BaseAPIConnection):
    """
    Implementação da conexão com a API do Groq.
    """

    def __init__(self, api_key: str, model: str = "deepseek-r1-distill-llama-70b") -> None:
        """
        Inicializa a conexão com a API do Groq.

        Args:
            api_key (str): Chave de API do serviço Groq
            model (str, optional): Modelo a ser usado. Defaults to "llama-3.1-8b-instant"
        """
        super().__init__(api_key, model)
        self.client = Groq(api_key=api_key)


class APIConnectionFactory:
    """
    Factory para criar instâncias de conexões com APIs.
    """

    @staticmethod
    def create_connection(api_type: str, api_key: Optional[str] = None, **kwargs: Any) -> Optional[APIConnection]:
        """
        Cria uma instância de conexão com API baseada no tipo especificado.

        Args:
            api_type (str): Tipo de API ("chatgpt" ou "groq")
            api_key (str, optional): Chave de API para o serviço. Se não fornecida, 
                                   será buscada nas variáveis de ambiente
            **kwargs: Argumentos adicionais para a inicialização da conexão

        Returns:
            Optional[APIConnection]: Instância da conexão ou None se o tipo for inválido

        Raises:
            ValueError: Se o tipo de API não for suportado ou se a chave API não for encontrada
        """
        if api_type.lower() == "chatgpt":
            api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("API key não encontrada para ChatGPT. Verifique se a chave está configurada no .env")
            return ChatGPTConnection(api_key, **kwargs)
        elif api_type.lower() == "groq":
            api_key = api_key or os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("API key não encontrada para Groq. Verifique se a chave está configurada no .env")
            return GroqConnection(api_key, **kwargs)
        else:
            raise ValueError(f"Tipo de API não suportado: {api_type}")
