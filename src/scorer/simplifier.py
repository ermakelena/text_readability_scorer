# Импорты не отсортированы

from typing import Dict  # Такой способ аннотации типа устарел.
import json
from datetime import datetime


def suggest_improvements(results: Dict[str, float], min_readability_score: float = 60.0,
                         show_json: bool = True) -> None:
    """
    Формирует список конкретных рекомендаций по улучшению читаемости текста.

    :param results: словарь с результатами анализа
    :param min_readability_score: минимальный порог удобства чтения
    :param show_json: сохранять ли рекомендации в JSON файл
    """
    improvements = []

    # Рекомендации на основе Flesch Reading Ease
    if results["flesch_reading_ease"] < min_readability_score:
        improvements.append("Используйте более короткие предложения.")
        improvements.append("Избегайте сложных конструкций и длинных слов.")
        improvements.append("Разбейте длинные предложения на несколько коротких.")
        improvements.append("Используйте активный залог вместо пассивного.")

    # Рекомендации на основе Flesch-Kincaid Grade Level
    if results["flesch_kincaid_grade_level"] >= 12:
        improvements.append("Сделайте текст понятнее для широкой аудитории.")
        improvements.append("Замените специальные термины на общеупотребительные слова.")
        improvements.append("Добавьте пояснения к сложным понятиям.")
        improvements.append("Используйте примеры для иллюстрации сложных идей.")

    # Рекомендации на основе Gunning Fog Index
    if results["gunning_fog_index"] > 12:
        improvements.append("Попробуйте упростить сложные слова и выражения.")
        improvements.append("Сократите количество слов с тремя и более слогами.")
        improvements.append("Используйте синонимы с меньшим количеством слогов.")
        improvements.append("Избегайте цепочек прилагательных и наречий.")

    # Дополнительные рекомендации на основе комбинации метрик
    if results["flesch_reading_ease"] < 50 and results["gunning_fog_index"] > 15:
        improvements.append("Текст слишком сложен. Рассмотрите возможность полного переписывания.")
        improvements.append("Определите целевую аудиторию и адаптируйте текст под её уровень.")

    if results["flesch_kincaid_grade_level"] > 15:
        improvements.append("Текст требует высшего образования для понимания. Упростите.")
        improvements.append("Добавьте краткое содержание или аннотацию в начале.")

    # Положительные отзывы для хороших текстов
    if results["flesch_reading_ease"] >= 70:
        improvements.append("Текст хорошо сбалансирован по сложности.")
    if results["flesch_kincaid_grade_level"] < 10:
        improvements.append("Уровень сложности подходит для большинства читателей.")
    if results["gunning_fog_index"] < 10:
        improvements.append("Использование сложных слов оптимально.")

    if improvements:
        print("\nРекомендации по улучшению:")
        print("-" * 50)
        for i, suggestion in enumerate(improvements, start=1):
            print(f"{i}. {suggestion}")

        # Сохранение рекомендаций в JSON (если разрешено)
        if show_json:
            save_recommendations(results, improvements)
    else:
        print("\nВаш текст достаточно прост для восприятия!")
        print("Все метрики находятся в оптимальном диапазоне.")


def save_recommendations(results: Dict[str, float], improvements: list) -> None:
    """
    Сохраняет рекомендации в JSON файл.

    :param results: результаты анализа
    :param improvements: список рекомендаций
    """
    recommendations_data = {
        "timestamp": datetime.now().isoformat(),
        "original_metrics": {
            "flesch_reading_ease": round(results['flesch_reading_ease'], 2),
            "flesch_kincaid_grade_level": round(results['flesch_kincaid_grade_level'], 2),
            "gunning_fog_index": round(results['gunning_fog_index'], 2)
        },
        "improvements": improvements,
        "summary": {
            "total_recommendations": len(improvements),
            "by_category": {
                "flesch_reading_ease": sum(1 for s in improvements if "предложени" in s or "конструкц" in s),
                "flesch_kincaid": sum(1 for s in improvements if "аудитори" in s or "термин" in s),
                "gunning_fog": sum(1 for s in improvements if "слог" in s or "слов" in s)
            }
        }
    }

    filename = f"improvements_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(recommendations_data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Рекомендации сохранены в файл: {filename}")
    print("-" * 50)

# Нет пустой строки
