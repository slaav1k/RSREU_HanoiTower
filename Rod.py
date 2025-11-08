"""
Rod.py
==========
Дата: 08.11.2025
Разработчик: Архипкин Вячеслав
==========
Описание:
---------
Вспомогательный одуль, реализующий логику дисков игры Ханойские башни
"""

class Rod:
    """Класс, представляющий стержень с дисками."""
    def __init__(self, name):
        self.name = name  # Имя стержня (A, B, C)
        self.disks = []   # Список дисков (меньший номер - меньший размер)

    def push(self, disk):
        """Добавить диск на стержень."""
        self.disks.append(disk)

    def pop(self):
        """Снять верхний диск со стержня."""
        if self.disks:
            return self.disks.pop()
        return None

    def __str__(self):
        """Строковое представление стержня."""
        return f"{self.name}: {self.disks if self.disks else 'пусто'}"