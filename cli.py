from typing import Dict, Optional
from api_connection import APIConnectionFactory
from commands import AskModelCommand, CommandInvoker
from evaluation_strategy import ResponseEvaluator
from observers import ResponseSubject, ConsoleObserver, FileObserver, LogObserver
import os
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()


class CLI:
    """
    Interface de linha de comando para interação com os modelos.
    """

    def __init__(self) -> None:
        """
        Inicializa a CLI com as conexões necessárias.
        """
        self.factory = APIConnectionFactory()
        self.invoker = CommandInvoker()
        self.models: Dict[str, str] = {
            "1": "chatgpt",
            "2": "groq"
        }
        self.evaluator = ResponseEvaluator()
        self.last_responses: Dict[str, str] = {}

        # Adicionar sujeito e observadores
        self.response_subject = ResponseSubject()

        # Adicionar diferentes tipos de observadores
        self.response_subject.attach(ConsoleObserver())
        self.response_subject.attach(FileObserver())
        self.response_subject.attach(LogObserver())

    def display_menu(self) -> None:
        """
        Exibe o menu principal.
        """
        print("\n=== Menu Principal ===")
        print("1. Usar ChatGPT")
        print("2. Usar Groq")
        print("3. Comparar últimas respostas")
        print("4. Sair")

    def compare_responses(self) -> None:
        """
        Compara as últimas respostas dos modelos.
        """
        if len(self.last_responses) < 2:
            print("Precisa ter pelo menos duas respostas para comparar!")
            return

        print("\n=== Comparação de Respostas ===")
        results = self.evaluator.evaluate_all(
            self.last_responses["chatgpt"],
            self.last_responses["groq"]
        )

        print("\nResultados da comparação:")
        for strategy_name, result in results.items():
            print(f"\n{strategy_name.upper()}:")
            for key, value in result.items():
                print(f"  {key}: {value}")

    def run(self) -> None:
        """
        Executa o loop principal da CLI.
        """
        while True:
            self.display_menu()
            choice = input("Escolha uma opção: ")

            if choice == "4":
                print("Saindo...")
                break

            if choice == "3":
                self.compare_responses()
                continue

            if choice not in self.models:
                print("Opção inválida!")
                continue

            # Obter a pergunta do usuário
            question = input("Digite sua pergunta: ")

            try:
                # Obter as chaves de API das variáveis de ambiente
                openai_api_key = os.getenv("OPENAI_API_KEY")
                groq_api_key = os.getenv("GROQ_API_KEY")

                if choice == "1" and not openai_api_key:
                    raise ValueError("Chave de API do ChatGPT não encontrada nas variáveis de ambiente.")
                if choice == "2" and not groq_api_key:
                    raise ValueError("Chave de API do Groq não encontrada nas variáveis de ambiente.")

                # Criar conexão com o modelo escolhido
                api_key = openai_api_key if choice == "1" else groq_api_key
                model_connection = self.factory.create_connection(self.models[choice], api_key)

                # Criar e executar o comando
                command = AskModelCommand(model_connection, question)
                self.invoker.set_command(command)
                self.invoker.execute_command()

                # Obter resposta e notificar observadores
                response = model_connection.get_response(
                    model_connection.send_request(question)
                )
                self.last_responses[self.models[choice]] = response

                # Notificar observadores sobre a nova resposta
                self.response_subject.set_response(
                    self.models[choice],
                    question,
                    response
                )

            except Exception as e:
                print(f"Erro: {e}")


def main() -> None:
    """
    Função principal que inicia a CLI.
    """
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    load_dotenv()
    main()
