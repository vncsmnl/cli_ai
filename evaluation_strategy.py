from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union
from difflib import SequenceMatcher
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download recursos necessários do NLTK
nltk.download('punkt')
nltk.download('stopwords')


class EvaluationStrategy(ABC):
    """
    Interface base para estratégias de avaliação de respostas.
    """

    @abstractmethod
    def evaluate(self, response1: str, response2: str) -> Dict[str, Any]:
        """
        Avalia e compara duas respostas.

        Args:
            response1 (str): Primeira resposta para comparação
            response2 (str): Segunda resposta para comparação

        Returns:
            Dict[str, Any]: Resultados da avaliação
        """
        pass


class WordCountStrategy(EvaluationStrategy):
    """
    Estratégia que compara respostas baseada em contagem de palavras.
    """

    def evaluate(self, response1: str, response2: str) -> Dict[str, Any]:
        """
        Avalia respostas contando palavras e calculando estatísticas básicas.
        """
        words1 = word_tokenize(response1.lower())
        words2 = word_tokenize(response2.lower())

        return {
            "words_response1": len(words1),
            "words_response2": len(words2),
            "difference": abs(len(words1) - len(words2)),
            "ratio": len(words1) / len(words2) if len(words2) > 0 else float('inf')
        }


class SemanticSimilarityStrategy(EvaluationStrategy):
    """
    Estratégia que compara respostas baseada em similaridade semântica.
    """

    def evaluate(self, response1: str, response2: str) -> Dict[str, Any]:
        """
        Avalia respostas usando TF-IDF e similaridade do cosseno.
        """
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([response1, response2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

        return {
            "semantic_similarity": similarity,
            "similarity_percentage": f"{similarity * 100:.2f}%"
        }


class TextSimilarityStrategy(EvaluationStrategy):
    """
    Estratégia que compara respostas baseada em similaridade de texto.
    """

    def evaluate(self, response1: str, response2: str) -> Dict[str, Any]:
        """
        Avalia respostas usando o algoritmo de sequência.
        """
        similarity = SequenceMatcher(None, response1, response2).ratio()

        return {
            "text_similarity": similarity,
            "similarity_percentage": f"{similarity * 100:.2f}%"
        }


class ResponseEvaluator:
    """
    Classe que utiliza as estratégias de avaliação.
    """

    def __init__(self) -> None:
        """
        Inicializa o avaliador com as estratégias disponíveis.
        """
        self.strategies: Dict[str, EvaluationStrategy] = {
            "word_count": WordCountStrategy(),
            "semantic": SemanticSimilarityStrategy(),
            "text": TextSimilarityStrategy()
        }

    def evaluate_responses(self,
                           response1: str,
                           response2: str,
                           strategy_name: str) -> Dict[str, Any]:
        """
        Avalia duas respostas usando a estratégia especificada.

        Args:
            response1 (str): Primeira resposta
            response2 (str): Segunda resposta
            strategy_name (str): Nome da estratégia a ser usada

        Returns:
            Dict[str, Any]: Resultados da avaliação

        Raises:
            ValueError: Se a estratégia não existir
        """
        if strategy_name not in self.strategies:
            raise ValueError(f"Estratégia '{strategy_name}' não encontrada")

        strategy = self.strategies[strategy_name]
        return strategy.evaluate(response1, response2)

    def evaluate_all(self, response1: str, response2: str) -> Dict[str, Dict[str, Any]]:
        """
        Avalia duas respostas usando todas as estratégias disponíveis.

        Args:
            response1 (str): Primeira resposta
            response2 (str): Segunda resposta

        Returns:
            Dict[str, Dict[str, Any]]: Resultados de todas as avaliações
        """
        results = {}
        for strategy_name in self.strategies:
            results[strategy_name] = self.evaluate_responses(
                response1, response2, strategy_name
            )
        return results
