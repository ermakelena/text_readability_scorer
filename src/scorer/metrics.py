import re
from typing import Tuple, Dict


def count_words(text: str) -> int:
    """Подсчет количества слов."""
    words = text.split()
    return len(words)


def count_sentences(text: str) -> int:
    """Подсчет количества предложений."""
    sentences = re.findall(r'[.?!]+', text)
    return len(sentences)


def count_syllables(word: str) -> int:
    """Подсчет слогов в слове."""
    vowels = 'aeiouy'
    word = word.lower().strip(".,:;")
    if not word:
        return 0
    num_vowels = sum([1 for char in word if char in vowels])
    return max(num_vowels, 1)


def calculate_flesch_reading_ease(total_words: int, total_sentences: int, syllable_count: int) -> float:
    """Вычисление индекса Flesch Reading Ease."""
    return 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (syllable_count / total_words)


def calculate_flesch_kincaid_grade_level(total_words: int, total_sentences: int, syllable_count: int) -> float:
    """Вычисление уровня образования Flesch-Kincaid Grade Level."""
    return 0.39 * (total_words / total_sentences) + 11.8 * (syllable_count / total_words) - 15.59


def calculate_gunning_fog_index(total_words: int, complex_word_count: int, total_sentences: int) -> float:
    """Вычисление индекса Gunning Fog."""
    avg_sentence_length = total_words / total_sentences
    percent_complex_words = (complex_word_count / total_words) * 100
    return 0.4 * (avg_sentence_length + percent_complex_words)


def is_complex_word(word: str) -> bool:
    """Проверка является ли слово сложным (более двух слогов)."""
    return count_syllables(word) > 2


def extract_metrics(text: str) -> Tuple[int, int, int]:
    """
    Возвращает кортеж из общего числа слов, предложений и сложных слов.

    :param text: исходный текст
    :return: tuple of (words, sentences, complex_words)
    """
    words = count_words(text)
    sentences = count_sentences(text)
    complex_words = sum(is_complex_word(w) for w in text.split())
    return words, sentences, complex_words


def select_metrics(analysis_results: Dict[str, float], metric_choice: str = "all") -> Dict[str, float]:
    """
    Возвращает выбранные пользователем метрики или их среднее.

    :param analysis_results: словарь со всеми метриками
    :param metric_choice: выбор метрики ("flesch", "kincaid", "gunning", "average", "all")
    :return: словарь с выбранными метриками
    """
    choices = {
        "flesch": {"flesch_reading_ease": analysis_results["flesch_reading_ease"]},
        "kincaid": {"flesch_kincaid_grade_level": analysis_results["flesch_kincaid_grade_level"]},
        "gunning": {"gunning_fog_index": analysis_results["gunning_fog_index"]},
        "average": {
            "average_readability": (
                                           analysis_results["flesch_reading_ease"] +
                                           (100 - analysis_results[
                                               "flesch_kincaid_grade_level"] * 6.67) +  # Нормализация Kincaid
                                           (100 - analysis_results["gunning_fog_index"] * 8.33)
                                   # Нормализация Gunning Fog
                                   ) / 3
        },
        "all": analysis_results
    }

    return choices.get(metric_choice, analysis_results)


def show_metric_selection_menu() -> str:
    """
    Показывает меню выбора метрик.

    :return: выбранная опция
    """
    print("\n" + "=" * 50)
    print("Выбор метрик для отображения:")
    print("=" * 50)
    print("1. Flesch Reading Ease (легкость чтения)")
    print("2. Flesch-Kincaid Grade Level (уровень образования)")
    print("3. Gunning Fog Index (сложность текста)")
    print("4. Средний показатель читаемости")
    print("5. Все метрики (полный отчет)")
    print("0. Выход")
    print("=" * 50)

    while True:
        try:
            choice = input("Выберите опцию (0-5): ").strip()
            options = {
                "1": "flesch",
                "2": "kincaid",
                "3": "gunning",
                "4": "average",
                "5": "all",
                "0": "exit"
            }

            if choice in options:
                return options[choice]
            else:
                print("Пожалуйста, введите число от 0 до 5")
        except KeyboardInterrupt:
            return "exit"