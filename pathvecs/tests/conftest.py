import spacy
import pytest

@pytest.fixture(scope="session")
def en_vocab():
    return spacy.util.get_lang_class("en")().vocab
