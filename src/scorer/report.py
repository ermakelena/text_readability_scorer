import json
from typing import Dict
from datetime import datetime
from analyzer import TextAnalyzer


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