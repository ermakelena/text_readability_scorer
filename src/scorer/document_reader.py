from typing import List

class DocumentReader:
    def __init__(self, file_path: str):
        """
        Конструктор класса DocumentReader.
        
        :param file_path: путь к файлу .txt
        """
        self.file_path = file_path
    
    def read_text(self) -> str:
        """
        Читает содержимое файла и возвращает текст.
        
        :return: строка с текстом документа
        """
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return f.read()