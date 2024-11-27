from collections import Counter
import string 

def top_10_most_common_words(text: str) -> dict[str, int]:
    """Функция возвращает топ 10 слов, встречающихся в тексте.

    Args:
        text: исходный текст

    Returns:
        словарь типа {слово: количество вхождений}
    """

   
    text = text.lower()
    
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = text.translate(translator)
    words = cleaned_text.split()
    filtered_words = [word for word in words if len(word) >= 3]
    word_counts = Counter(filtered_words)
    sorted_word_counts = dict(sorted(word_counts.items(), key=lambda item: (-item[1], item[0])))
    most_common = dict(list(sorted_word_counts.items())[:10])
    
    return most_common

