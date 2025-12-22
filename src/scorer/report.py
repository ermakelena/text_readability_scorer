# Импорты не отсортированы

import json
from typing import Dict  # Такой способ аннотации типа устарел.
from datetime import datetime
from src.scorer.analyzer import TextAnalyzer  # Неправильные импорты.
from src.scorer.metrics import select_metrics, show_metric_selection_menu


def generate_report(analysis_results: Dict[str, float], output_format: str = "text") -> str:
    """
    Генерирует отчёт по проведённому анализу текста.

    :param analysis_results: словарь с результатом анализа
    :param output_format: формат вывода ("text", "json", или "both")
    :return: строка с отчетом (пустая для JSON-файла)
    """
    report_text = ""

    if output_format in ["text", "both"]:
        report_text += "\n*** Отчет о читаемости текста ***\n\n"
        report_text += f"Flesch Reading Ease: {analysis_results['flesch_reading_ease']:.2f}\n"
        report_text += f"Flesch-Kincaid Grade Level: {analysis_results['flesch_kincaid_grade_level']:.2f}\n"
        report_text += f"Gunning Fog Index: {analysis_results['gunning_fog_index']:.2f}\n\n"

    if output_format in ["json", "both"]:
        # Создаем структурированный отчет для JSON
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "flesch_reading_ease": round(analysis_results['flesch_reading_ease'], 2),
                "flesch_kincaid_grade_level": round(analysis_results['flesch_kincaid_grade_level'], 2),
                "gunning_fog_index": round(analysis_results['gunning_fog_index'], 2)
            },
            "interpretation": {
                "flesch_reading_ease": _interpret_flesch(analysis_results['flesch_reading_ease']),
                "flesch_kincaid_grade_level": _interpret_kincaid(analysis_results['flesch_kincaid_grade_level']),
                "gunning_fog_index": _interpret_gunning_fog(analysis_results['gunning_fog_index'])
            }
        }

        # Генерируем имя файла с временной меткой
        filename = f"readability_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        if output_format in ["json", "both"]:
            report_text += f"\nJSON отчет сохранен в файл: {filename}"

    return report_text

# Нет аннотации ни входных параметров, ни ретерна
def _interpret_flesch(score: float) -> str:
    """Интерпретация результата Flesch Reading Ease."""
    if score >= 90:
        return "Очень легко (5-й класс)"
    elif score >= 80:
        return "Легко (6-й класс)"
    elif score >= 70:
        return "Довольно легко (7-й класс)"
    elif score >= 60:
        return "Стандартный (8-9-й классы)"
    elif score >= 50:
        return "Довольно сложный (10-12-й классы)"
    elif score >= 30:
        return "Сложный (студенты вузов)"
    else:
        return "Очень сложный (выпускники вузов)"


def _interpret_kincaid(score: float) -> str:
    """Интерпретация результата Flesch-Kincaid Grade Level."""
    return f"Уровень {score:.1f} класса"


def _interpret_gunning_fog(score: float) -> str:
    """Интерпретация результата Gunning Fog Index."""
    if score <= 6:
        return "Легко (детская литература)"
    elif score <= 8:
        return "Доступно (массовый читатель)"
    elif score <= 10:
        return "Средне (газеты, журналы)"
    elif score <= 12:
        return "Сложно (академические тексты)"
    else:
        return "Очень сложно (специализированная литература)"
