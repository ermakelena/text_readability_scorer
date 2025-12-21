# Импорты не отсортированы

from typing import Dict  # Такой способ аннотации типа устарел. Вместо него используйте `dict[..., ...]`
from src.scorer.document_reader import DocumentReader  # Неправильные импорты. Нельзя указывать src
from src.scorer.metrics import (
    calculate_flesch_reading_ease,
    calculate_flesch_kincaid_grade_level,
    calculate_gunning_fog_index,
    extract_metrics,
    count_syllables
)

# Правильные импорты:
# from .document_reader import DocumentReader
# from .metrics import (
#     calculate_flesch_reading_ease,
#     calculate_flesch_kincaid_grade_level,
#     calculate_gunning_fog_index,
#     extract_metrics,
#     count_syllables
# )


# Нет аннотации ретерна
class TextAnalyzer:
    def __init__(self, reader: DocumentReader):
        """
        Конструктор класса TextAnalyzer.

        :param reader: объект для чтения текста из файла
        """
        self.reader = reader

    def analyze(self) -> Dict[str, float]:
        """
        Выполняет полный анализ текста и возвращает словарь с результатами.

        :return: словарь с метриками
        """
        text = self.reader.read_text()
        words, sentences, complex_words = extract_metrics(text)
        syllable_count = sum(count_syllables(w) for w in text.split())

        results = {
            'flesch_reading_ease': calculate_flesch_reading_ease(words, sentences, syllable_count),
            'flesch_kincaid_grade_level': calculate_flesch_kincaid_grade_level(words, sentences, syllable_count),
            'gunning_fog_index': calculate_gunning_fog_index(words, complex_words, sentences)
        }
        return results

# Нет пустой строки
