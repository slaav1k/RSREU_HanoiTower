"""
Node.py
==========
Дата: 08.11.2025
Разработчик: Архипкин Вячеслав
==========
Описание:
---------
Модуль, реализующий логику листа дерева.
"""
from typing import Any, Optional, Tuple


class Node:
    _id_counter = 0

    def __init__(self, situation: Any, parent: Optional['Node'] = None, move: Optional[Tuple[str, str]] = None,
                 depth: int = 0):
        """
        Класс, представляющий узел в дереве состояний
        :param situation: Текущее состояние (кортеж кортежей для A, B, C)
        :param parent: Родительский узел
        :param move: Ход, приведший к этому состоянию (например, ('A', 'B'))
        :param depth: Глубина узла в дереве
        """
        self.parent = parent
        self.children = []
        self.depth = depth
        self.move = move
        self.situation = situation
        self.id = Node._id_counter
        Node._id_counter += 1





    def add_child(self, child: 'Node') -> None:
        """
        Добавить дочерний узел
        :param child: Дочерний узел
        :return: Ничего
        """
        self.children.append(child)


    def __lt__(self, other: 'Node') -> bool:
        return self.id < other.id
