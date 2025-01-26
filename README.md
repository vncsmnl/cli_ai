# CLI for Interaction with AI Models

This project is a command-line interface (CLI) that allows interaction with language models such as ChatGPT and other LLMs (Groq, Anthropic, etc.). It provides functionalities to send questions to the models, compare answers using different evaluation strategies, and log responses in different formats.

## Project Structure

The project consists of several modules, each responsible for a specific part of the functionality:

1. **`observers.py`**: Implements the Observer design pattern, allowing different observers to be notified about new responses from the models. It includes observers that display responses on the console, save them to JSON files, and log them.

2. **`evaluation_strategy.py`**: Defines evaluation strategies for comparing model responses. Strategies include word count, semantic similarity using TF-IDF, and text similarity using sequence alignment algorithms.

3. **`commands.py`**: Implements the Command design pattern, allowing commands to be defined and executed. It includes a command to send questions to AI models.

4. **`cli.py`**: Contains the main logic of the command-line interface, including menu displays, command execution, and response comparison.

5. **`api_connection.py`**: Defines connections to language model APIs, including ChatGPT and Groq. It uses the Factory design pattern to create instances of connections based on the API type.

## Features

### Observers

- **ConsoleObserver**: Displays model responses directly in the console.
- **FileObserver**: Saves responses to a JSON file, allowing for persistent storage.
- **LogObserver**: Logs responses to a log file, useful for auditing and later analysis.

### Evaluation Strategies

- **WordCountStrategy**: Compares responses based on word count, providing basic statistics such as difference and ratio of words.
- **SemanticSimilarityStrategy**: Evaluates semantic similarity between responses using TF-IDF and cosine similarity.
- **TextSimilarityStrategy**: Compares responses using sequence alignment algorithms to determine text similarity.

### Commands

- **AskModelCommand**: Sends a question to an AI model and displays the response. It uses the appropriate API connection for the selected model.

### CLI

- **Main Menu**: Allows the user to choose between different AI models, compare responses, or exit the program.
- **Response Comparison**: Compares the latest responses from the models using all available evaluation strategies.
- **Command Execution**: Allows the user to send questions to models and process responses.

## Setup

The project uses environment variables to store API keys. These keys should be defined in a `.env` file in the root directory of the project:

```
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
```

## Running the Application

To run the CLI, simply execute the `cli.py` script:

```bash
python cli.py
```

Make sure all dependencies are installed and that the API keys are configured correctly.

## Dependencies

- Python 3.x
- Libraries: `requests`, `nltk`, `sklearn`, `numpy`, `dotenv`
- NLTK Resources: `punkt`, `stopwords`

## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests for improvements and fixes.