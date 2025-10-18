from collections import deque
from typing import List, Tuple, Optional, Any, Set

from Node import Node
from Tree import Tree


class Solver:
    """Универсальный решатель на основе поиска в глубину (а можно и в ширину) для задач с состояниями."""
    def __init__(self, max_depth: int = 7):
        self.max_depth = max_depth

    def solve(self, current_situation: Any, goal_situation: Any, get_next_situations: callable) -> Optional[List[Tuple[str, str]]]:
        """
        Ищет решение с помощью поиска в глубину.
        Args:
            current_situation: Текущее состояние (например, кортежи дисков для A, B, C).
            goal_situation: Целевое состояние.
            get_next_situations: Функция, возвращающая список (next_situation, move) для возможных ходов.
        Returns:
            Список шагов (например, (source, destination)) или None, если решение не найдено.
        """
        # Стек содержит: (situation, depth, move), где move — последний ход (или None для начального состояния)
        stack = [(current_situation, 0, None)]
        visited = {current_situation}  # Множество посещённых состояний
        path = []  # Текущий путь (список ходов)

        while stack:
            situation, depth, move = stack.pop()

            # Если это не начальное состояние, добавляем ход в путь
            if move is not None:
                path.append(move)
                visited.add(situation)

            # Достигнута целевая ситуация?
            if situation == goal_situation:
                return path.copy()  # Возвращаем копию текущего пути

            # Достигли лимита глубины?
            if depth >= self.max_depth:
                if move is not None:
                    path.pop()  # Откатываем ход
                    visited.remove(situation)  # Удаляем состояние из посещённых
                continue

            # Получаем следующие возможные состояния
            any_moves_added = False
            next_situations = get_next_situations(situation)
            for next_situation, next_move in reversed(next_situations):
                if next_situation not in visited:
                    stack.append((next_situation, depth + 1, next_move))
                    any_moves_added = True

            # Если не добавили новых ходов и это не начальное состояние, откатываем
            if move is not None and not any_moves_added:
                path.pop()
                visited.remove(situation)


        return None

    def solve_wide(self, current_situation: Any, goal_situation: Any, get_next_situations: callable) -> Optional[List[Tuple[str, str]]]:
        """
        Ищет решение с помощью поиска в ширину.
        Args:
            current_situation: Текущее состояние (например, кортежи дисков для A, B, C).
            goal_situation: Целевое состояние.
            get_next_situations: Функция, возвращающая список (next_situation, move) для возможных ходов.
        Returns:
            Список шагов (например, (source, destination)) или None, если решение не найдено.
        """
        # Инициализация дерева и очереди
        tree = Tree(current_situation)
        queue = deque([tree.root])  # Храним узлы дерева
        visited = {current_situation}  # Множество посещённых состояний

        while queue:
            current_node = queue.popleft()

            # Достигнута целевая ситуация?
            if current_node.situation == goal_situation:
                return tree.get_path_to_node(current_node)

            # Проверка на превышение максимальной глубины
            if current_node.depth >= self.max_depth:
                continue

            # Получаем следующие возможные состояния
            next_situations = get_next_situations(current_node.situation)
            for next_situation, move in next_situations:
                if next_situation not in visited:
                    # Создаём новый узел с увеличенной глубиной
                    new_node = Node(next_situation, parent=current_node, move=move, depth=current_node.depth + 1)
                    current_node.add_child(new_node)
                    visited.add(next_situation)
                    queue.append(new_node)

        return None