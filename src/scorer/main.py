# Импорты не отсортированы

from src.scorer.analyzer import TextAnalyzer  # Неправильные импорты.
from src.scorer.document_reader import DocumentReader
from src.scorer.report import generate_report
from src.scorer.simplifier import suggest_improvements, save_recommendations
import os

# Определяем базовую директорию проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# BASE_DIR теперь = text_scorer  # Для кого этот комментарий?
TEXTS_DIR = os.path.join(BASE_DIR, "texts")


# Нет аннотации ни входных параметров, ни ретерна
def get_recommendations_with_choice(results):
    """
    Получает рекомендации с выбором формата вывода
    """
    print("\nФормат вывода рекомендаций:")
    print("1. Только в консоль")
    print("2. Только в JSON файл")
    print("3. И в консоль, и в JSON")

    rec_choice = input("Ваш выбор (1-3): ").strip()

    if rec_choice == "1":
        # Только вывод в консоль
        print("\n" + "=" * 50)
        print("РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ")
        print("=" * 50)
        suggest_improvements(results, show_json=False)

    elif rec_choice == "2":
        # Только сохранение в JSON
        print("\n" + "=" * 50)
        print("СОХРАНЕНИЕ РЕКОМЕНДАЦИЙ")
        print("=" * 50)

        # Сначала получаем рекомендации без вывода
        improvements = []
        if results["flesch_reading_ease"] < 60.0:
            improvements.append("Используйте более короткие предложения.")
            improvements.append("Избегайте сложных конструкций и длинных слов.")
        if results["flesch_kincaid_grade_level"] >= 12:
            improvements.append("Сделайте текст понятнее для широкой аудитории.")
        if results["gunning_fog_index"] > 12:
            improvements.append("Попробуйте упростить сложные слова и выражения.")

        if improvements:
            save_recommendations(results, improvements)
            print("✓ Рекомендации сохранены в JSON файл")
        else:
            print("Текст достаточно прост для восприятия!")
            print("Все метрики находятся в оптимальном диапазоне.")

    elif rec_choice == "3":
        # И вывод, и сохранение
        print("\n" + "=" * 50)
        print("РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ")
        print("=" * 50)

        # Получаем и выводим рекомендации
        suggest_improvements(results, show_json=True)

    else:
        print("Неверный выбор, использую вывод в консоль по умолчанию.")
        print("\n" + "=" * 50)
        print("РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ")
        print("=" * 50)
        suggest_improvements(results, show_json=False)


def main():
    print("Анализатор читаемости текста")
    print("=" * 50)

    while True:
        print("\nВыберите текст для анализа:")
        print("1. Легкий (easy.txt)")
        print("2. Средний (medium.txt)")
        print("3. Сложный (hard.txt)")
        print("4. Свой файл")
        print("5. Выйти")

        choice = input("Ваш выбор (1-5): ").strip()

        if choice == "5":
            print("Выход из программы.")
            break

        # Определяем путь к файлу
        if choice == "1":
            file_path = os.path.join(TEXTS_DIR, "easy.txt")
        elif choice == "2":
            file_path = os.path.join(TEXTS_DIR, "medium.txt")
        elif choice == "3":
            file_path = os.path.join(TEXTS_DIR, "hard.txt")
        elif choice == "4":
            file_path = input("Введите путь к файлу: ").strip()
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)
        else:
            print("Неверный выбор.")
            continue

        # Проверяем существование файла
        if not os.path.exists(file_path):
            print(f"Файл '{file_path}' не найден!")
            continue

        # Выбор формата вывода результатов анализа
        print("\nФормат вывода результатов анализа:")
        print("1. Текстовый вывод в консоль")
        print("2. Сохранить в JSON файл")
        print("3. И то, и другое")

        output_choice = input("Ваш выбор (1-3): ").strip()

        if output_choice == "1":
            output_format = "text"
        elif output_choice == "2":
            output_format = "json"
        elif output_choice == "3":
            output_format = "both"
        else:
            print("Неверный выбор, использую текстовый вывод по умолчанию.")
            output_format = "text"

        try:
            # Анализируем текст
            print(f"\nАнализирую файл: {os.path.basename(file_path)}")
            reader = DocumentReader(file_path)
            analyzer = TextAnalyzer(reader)
            results = analyzer.analyze()

            # Генерируем отчет в выбранном формате
            if output_format == "text":
                # Только текстовый вывод
                print("\n" + "=" * 50)
                print("РЕЗУЛЬТАТЫ АНАЛИЗА")
                print("=" * 50)
                report_text = generate_report(results, "text")
                print(report_text)

            elif output_format == "json":
                # Только JSON файл
                report_output = generate_report(results, "json")
                print(f"\n{report_output}")

            elif output_format == "both":
                # И текстовый вывод, и JSON файл
                print("\n" + "=" * 50)
                print("РЕЗУЛЬТАТЫ АНАЛИЗА")
                print("=" * 50)
                report_text = generate_report(results, "text")
                print(report_text)

                report_output = generate_report(results, "json")
                print(f"\n{report_output}")

            # Получаем рекомендации с выбором формата
            get_recommendations_with_choice(results)

        except FileNotFoundError:
            print(f"Ошибка: файл '{file_path}' не найден.")
        except Exception as e:
            print(f"Ошибка при анализе: {e}")


if __name__ == "__main__":
    # Проверяем наличие папки с текстами
    if not os.path.exists(TEXTS_DIR):
        print(f"Внимание: папка с текстами не найдена: {TEXTS_DIR}")
        print("Создайте папку 'texts' и добавьте файлы:")
        print("- easy.txt, medium.txt, hard.txt")
        print("\nИли используйте опцию 'Свой файл' для указания полного пути.")

    main()

# Нет пустой строки
