import os
import json
from dotenv import load_dotenv
from typing import Optional, Union, List, Dict, Any

# PyTorch
import torch

# Gensim
from gensim import downloader
from gensim.models import KeyedVectors
from gensim.parsing.preprocessing import (
                        strip_multiple_whitespaces,
                        strip_numeric,
                        strip_punctuation,
                        strip_short
                        )

# NLTK
from nltk.tokenize import word_tokenize

# Transformers
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Levenshtein
from Levenshtein import ratio as levenshtein_distance


# Set project directory and load environment variables
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(PROJECT_DIR, ".env"))

# Load corrected dictionary from a JSON file
CORRECTED_DICT_LOCAL_PATH = os.path.join(
    os.getenv("DATA_PATH"),
    os.getenv("CORRECTED_DICT")
)
CORRECTED_DICT = json.load(
    open(
        os.path.join(
            PROJECT_DIR,
            CORRECTED_DICT_LOCAL_PATH
            )
        )
    )
# Set the path to the GloVe model from environment variables
GLOVE_LOCAL_PATH = os.path.join(
    os.getenv("RESOURCES_PATH"),
    os.getenv("GLOVE_PATH")
)
GLOVE_PATH = os.path.join(PROJECT_DIR, GLOVE_LOCAL_PATH)


def load_glove_model() -> List[Any]:
    """
    Loads the GloVe model from a local file if available,
    otherwise downloads it

    Returns:
        Either a dictionary with words as keys and their embeddings as values
        or a KeyedVectors object
    """

    try:
        print(f"Trying to load GloVe model from {GLOVE_PATH}")
        glove_model = KeyedVectors.load_word2vec_format(
            GLOVE_PATH, binary=False
        )
    except Exception:
        print("GloVe model not found locally, downloading it...")
        glove_model = downloader.load("glove-wiki-gigaword-300")
    finally:
        print("GloVe model loaded successfully")
        return glove_model.index_to_key


def simple_cleaning(text: str) -> str:
    """
    Performs simple text cleaning operations on the input text

    Args:
        text: The text to clean
    Returns:
        The cleaned text
    """

    text = strip_multiple_whitespaces(text)
    text = strip_numeric(text)
    text = strip_punctuation(text)
    text = strip_short(text)

    text = text.lower()

    return text


def vocabulary_coverage(words: List[str],
                        glove_vocab: List[Any]) -> List[str]:
    """
    Computes the vocabulary coverage of words using the GloVe model

    Args:
        words: List of words to check for coverage
        glove_vocab: The GloVe vocabulary used for checking word coverage
    Returns:
        List of out-of-vocabulary words
    """

    oov_words = [word for word in words if word not in glove_vocab]

    return oov_words


def correct_text_on_the_fly(words: List[str],
                            glove_vocab: List[Any],
                            ratio_threshold: float = 0.7) -> Dict[str, str]:
    """
    Corrects text on the fly using the Levenshtein ratio
    to find the closest words in the GloVe model

    Args:
        words: List of words to correct
        glove_vocab: The GloVe vocabulary used for correction
        ratio_threshold: Threshold for accepting a correction
            based on the Levenshtein ratio
    Returns:
        Dictionary mapping initial words to their corrected form
    """

    corrected_words = {word: word for word in words}
    for word in words:
        best_match, best_ratio = None, 0
        for glove_word in glove_vocab:
            ratio = levenshtein_distance(word, glove_word)
            if ratio > best_ratio:
                best_match, best_ratio = glove_word, ratio
        if best_ratio > ratio_threshold:
            corrected_words[word] = best_match

    return corrected_words


def lazy_teacher_pipeline(text: Union[str, List[str]],
                          model: AutoModelForSequenceClassification,
                          tokenizer: AutoTokenizer,
                          glove_vocab: Optional[List[Any]],
                          on_the_fly: bool = False,
                          device: str = "cpu") -> List[int]:
    """
    Predicts the rating of text using a sequence classification model

    Args:
        text: The text or list of texts to predict
        model: The sequence classification model used for prediction
        tokenizer: The tokenizer for preparing input data
        glove_model: The GloVe model used for correcting text
        on_the_fly: Flag to determine if text should be corrected on the fly
        device: The computation device ('cpu' or 'cuda' or 'mps')

    Returns:
        List of predicted ratings
    """

    if isinstance(text, str):
        text = [text]

    text = [simple_cleaning(text) for text in text]
    tokenized_texts = [word_tokenize(text) for text in text]
    words_not_in_glove = [
        vocabulary_coverage(tokenized_text, glove_vocab)
        for tokenized_text in tokenized_texts
    ]
    if on_the_fly:
        corrected_words = [
            correct_text_on_the_fly(word_not_in_glove, glove_vocab)
            for word_not_in_glove in words_not_in_glove
        ]
        corrected_texts = [
            [corrected_words[i].get(word, word) for word in tokenized_text]
            for i, tokenized_text in enumerate(tokenized_texts)
        ]
    else:
        corrected_words = [{
            word: CORRECTED_DICT.get(word, word)
            for word in word_not_in_glove
        } for word_not_in_glove in words_not_in_glove]

        corrected_texts = [
            [corrected_words[i].get(word, word) for word in tokenized_text]
            for i, tokenized_text in enumerate(tokenized_texts)
        ]

    text = [" ".join(cleaned_text) for cleaned_text in corrected_texts]

    model.to(device)
    inputs = tokenizer(
        text,
        padding=True,
        truncation=True,
        return_tensors="pt"
    ).to(device)
    model.eval()
    with torch.inference_mode():
        logits = model(**inputs).logits

    return (logits.argmax(-1) + 1).tolist()
