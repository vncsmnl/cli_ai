# CLI para interação com modelos de IA

Este projeto é uma interface de linha de comando (CLI) que permite a interação com modelos de linguagem de IA, como ChatGPT e Outras LLMs (Groq, Anthropic, etc). Ele oferece funcionalidades para enviar perguntas aos modelos, comparar respostas usando diferentes estratégias de avaliação e registrar as respostas em diferentes formatos.

## Estrutura do Projeto

O projeto é composto por vários módulos, cada um responsável por uma parte específica da funcionalidade:

1. **`observers.py`**: Implementa o padrão de projeto Observer, permitindo que diferentes observadores sejam notificados sobre novas respostas dos modelos. Inclui observadores que exibem respostas no console, salvam em arquivos JSON e registram em logs.

2. **`evaluation_strategy.py`**: Define estratégias de avaliação para comparar respostas dos modelos. As estratégias incluem contagem de palavras, similaridade semântica usando TF-IDF e similaridade de texto usando o algoritmo de sequência.

3. **`commands.py`**: Implementa o padrão de projeto Command, permitindo que comandos sejam definidos e executados. Inclui um comando para enviar perguntas aos modelos de IA.

4. **`cli.py`**: Contém a lógica principal da interface de linha de comando, incluindo a exibição de menus, a execução de comandos e a comparação de respostas.

5. **`api_connection.py`**: Define conexões com APIs de modelos de linguagem, incluindo ChatGPT e Groq. Utiliza o padrão de projeto Factory para criar instâncias de conexões com base no tipo de API.

## Funcionalidades

### Observadores

- **ConsoleObserver**: Exibe as respostas dos modelos diretamente no console.
- **FileObserver**: Salva as respostas em um arquivo JSON, permitindo o armazenamento persistente.
- **LogObserver**: Registra as respostas em um arquivo de log, útil para auditoria e análise posterior.

### Estratégias de Avaliação

- **WordCountStrategy**: Compara respostas com base na contagem de palavras, fornecendo estatísticas básicas como diferença e razão de palavras.
- **SemanticSimilarityStrategy**: Avalia a similaridade semântica entre respostas usando TF-IDF e similaridade do cosseno.
- **TextSimilarityStrategy**: Compara respostas usando o algoritmo de sequência para determinar a similaridade de texto.

### Comandos

- **AskModelCommand**: Envia uma pergunta a um modelo de IA e exibe a resposta. Utiliza a conexão com a API apropriada para o modelo escolhido.

### CLI

- **Menu Principal**: Permite ao usuário escolher entre diferentes modelos de IA, comparar respostas ou sair do programa.
- **Comparação de Respostas**: Compara as últimas respostas dos modelos usando todas as estratégias de avaliação disponíveis.
- **Execução de Comandos**: Permite ao usuário enviar perguntas aos modelos e processar as respostas.

## Configuração

O projeto utiliza variáveis de ambiente para armazenar chaves de API. As chaves devem ser definidas em um arquivo `.env` no diretório raiz do projeto:

```
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
```

## Execução

Para executar a CLI, basta rodar o script `cli.py`:

```bash
python cli.py
```

Certifique-se de que todas as dependências estão instaladas e que as chaves de API estão configuradas corretamente.

## Dependências

- Python 3.x
- Bibliotecas: `requests`, `nltk`, `sklearn`, `numpy`, `dotenv`
- Recursos NLTK: `punkt`, `stopwords`

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias e correções.
