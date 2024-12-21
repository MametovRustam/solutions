import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SPLIT_SYMBOL = '.\n'


def get_article(path: str) -> str:
    with open(path, 'r') as file:
        file_article = file.read()
    return file_article


def get_correct_article() -> str:
    return get_article(os.path.join(BASE_DIR, '4_safe_text', 'articles', 'correct_article.txt'))


def get_wrong_article() -> str:
    return get_article(os.path.join(BASE_DIR, '4_safe_text', 'articles', 'wrong_article.txt'))


def recover_article() -> str:
    wrong_article = get_wrong_article()
    reversed_article = wrong_article[::-1]
    cleaned_article = reversed_article.replace("!", "")
    sentences = cleaned_article.split('\n')
    corrected_sentences = []
    for sentence in sentences:
        if sentence.startswith('.'):
            corrected_sentences.append(sentence[1:] + '.')
        else:
            corrected_sentences.append(sentence)

    corrected_article = '\n'.join(corrected_sentences)
    final_article = corrected_article.replace("WOOF-WOOF", "CAT")

    final_sentences = []
    for sentence in final_article.split('\n'):
        if sentence:
            sentence = sentence.lower().capitalize()
        final_sentences.append(sentence)

    final_article = '\n'.join(final_sentences)

    final_article = '\n'.join(reversed(final_sentences))

    return final_article

