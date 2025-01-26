from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from api_connection import APIConnection, APIConnectionFactory


class BaseCommand(ABC):
    """
    Classe base para comandos da interface CLI.
    """

    @abstractmethod
    def execute(self) -> None:
        """
        Executa o comando.
        """
        pass


class AskModelCommand(BaseCommand):
    """
    Comando concreto para fazer perguntas ao modelo.
    """

    def __init__(self, model_connection: APIConnection, question: str) -> None:
        """
        Inicializa o comando com a conexão do modelo e a pergunta.

        Args:
            model_connection (APIConnection): Conexão com o modelo de IA
            question (str): Pergunta a ser enviada ao modelo
        """
        self.model_connection = model_connection
        self.question = question

    def execute(self) -> None:
        try:
            response = self.model_connection.send_request(self.question)
            answer = self.model_connection.get_response(response)
            print(f"Resposta: {answer}")
        except Exception as e:
            print(f"Erro ao processar pergunta: {e}")


class CommandInvoker:
    """
    Invocador que executa os comandos.
    """

    def __init__(self) -> None:
        """
        Inicializa o invocador.
        """
        self.command: Optional[BaseCommand] = None

    def set_command(self, command: BaseCommand) -> None:
        """
        Define o comando a ser executado.

        Args:
            command (BaseCommand): Comando a ser executado
        """
        self.command = command

    def execute_command(self) -> None:
        """
        Executa o comando atual.
        """
        if self.command:
            self.command.execute()
