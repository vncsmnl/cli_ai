from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
import json
import logging


class Observer(ABC):
    """
    Interface base para observadores.
    """

    @abstractmethod
    def update(self, response_data: Dict[str, Any]) -> None:
        """
        Atualiza o observador com novos dados.

        Args:
            response_data (Dict[str, Any]): Dados da nova resposta
        """
        pass


class ResponseSubject:
    """
    Sujeito que mantém a lista de observadores e os notifica.
    """

    def __init__(self) -> None:
        """
        Inicializa o sujeito com uma lista vazia de observadores.
        """
        self._observers: List[Observer] = []
        self._current_response: Dict[str, Any] = {}

    def attach(self, observer: Observer) -> None:
        """
        Adiciona um novo observador.

        Args:
            observer (Observer): Observador a ser adicionado
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """
        Remove um observador.

        Args:
            observer (Observer): Observador a ser removido
        """
        self._observers.remove(observer)

    def notify(self) -> None:
        """
        Notifica todos os observadores sobre mudanças.
        """
        for observer in self._observers:
            observer.update(self._current_response)

    def set_response(self, model: str, question: str, response: str) -> None:
        """
        Define uma nova resposta e notifica os observadores.

        Args:
            model (str): Nome do modelo que gerou a resposta
            question (str): Pergunta feita ao modelo
            response (str): Resposta gerada
        """
        self._current_response = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "question": question,
            "response": response
        }
        self.notify()


class ConsoleObserver(Observer):
    """
    Observador que exibe as respostas no console.
    """

    def update(self, response_data: Dict[str, Any]) -> None:
        print("\n=== Nova Resposta Recebida ===")
        print(f"Modelo: {response_data['model']}")
        print(f"Horário: {response_data['timestamp']}")
        print(f"Pergunta: {response_data['question']}")
        print(f"Resposta: {response_data['response']}")
        print("=" * 30)


class FileObserver(Observer):
    """
    Observador que salva as respostas em um arquivo.
    """

    def __init__(self, filename: str = "responses.json") -> None:
        """
        Inicializa o observador de arquivo.

        Args:
            filename (str): Nome do arquivo para salvar as respostas
        """
        self.filename = filename

    def update(self, response_data: Dict[str, Any]) -> None:
        try:
            # Carregar respostas existentes
            try:
                with open(self.filename, 'r') as f:
                    responses = json.load(f)
            except FileNotFoundError:
                responses = []

            # Adicionar nova resposta
            responses.append(response_data)

            # Salvar todas as respostas
            with open(self.filename, 'w') as f:
                json.dump(responses, f, indent=2)

        except Exception as e:
            logging.error(f"Erro ao salvar resposta: {e}")


class LogObserver(Observer):
    """
    Observador que registra as respostas em um log.
    """

    def __init__(self, log_file: str = "responses.log") -> None:
        """
        Inicializa o observador de log.

        Args:
            log_file (str): Nome do arquivo de log
        """
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )

    def update(self, response_data: Dict[str, Any]) -> None:
        logging.info(
            f"Nova resposta do modelo {response_data['model']}: "
            f"Pergunta: {response_data['question']} | "
            f"Resposta: {response_data['response']}"
        )
