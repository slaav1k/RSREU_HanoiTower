from typing import Any, Optional, Tuple


class Node:
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





    def add_child(self, child: 'Node') -> None:
        """
        Добавить дочерний узел
        :param child: Дочерний узел
        :return: Ничего
        """
        self.children.append(child)
