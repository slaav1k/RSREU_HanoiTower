"""
Solver.py
==========
Дата: 08.11.2025
Разработчик: Архипкин Вячеслав
==========
Описание:
---------
Универсальный решатель задач поиска в пространстве состояний.
Реализует стратегии:
1. Поиск в глубину
2. Поиск в ширину
3. Ветви и границы
"""

import heapq
from collections import deque
from ctypes.wintypes import MAX_PATH
from typing import List, Tuple, Optional, Any, Set

from Node import Node
from Tree import Tree


class Solver:
    """Универсальный решатель на основе поиска в глубину (а можно и в ширину) для задач с состояниями."""
    MAX_PATH = float('inf')

    def __init__(self, max_depth: int = 7, num_disks=3, gradient=False):
        self.max_depth = max_depth
        self.num_disks = num_disks
        self.gradient = gradient

    def _heuristic(self, situation):
        """
        Эвристика: насколько состояние "далеко" от цели.
        Меньше = лучше (ближе к цели).
        """
        a, b, c = situation
        target = tuple(range(self.num_disks, 0, -1))  # Цель: (3,2,1) на C

        # Сколько дисков уже правильно на C (снизу вверх)
        correct = sum(1 for i, d in enumerate(c) if i < len(target) and d == target[i])

        # Каждый "неправильный" диск требует минимум 1 хода
        misplaced = self.num_disks - correct

        # Диски на A и B — тоже плохо (штраф)
        penalty = len(a) + len(b)

        return misplaced + 0.1 * penalty

    def solve(self, current_situation: Any, goal_situation: Any, get_next_situations: callable) -> Optional[
        List[Tuple[str, str]]]:
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
        # stack = [(current_situation, 0, None)]
        stack = [(current_situation, [], 0)]
        visited = {current_situation}  # Множество посещённых состояний
        # path = []  # Текущий путь (список ходов)

        while stack:
            # situation, depth, move = stack.pop()
            situation, path, depth = stack.pop()

            # Если это не начальное состояние, добавляем ход в путь
            # if move is not None:
            #     path.append(move)
            #     visited.add(situation)

            # Достигнута целевая ситуация?
            if situation == goal_situation:
                return path.copy()  # Возвращаем копию текущего пути

            # Достигли лимита глубины?
            if depth >= self.max_depth:
                # if move is not None:
                #     path.pop()  # Откатываем ход
                #     visited.remove(situation)  # Удаляем состояние из посещённых
                continue

            # Получаем следующие возможные состояния
            any_moves_added = False
            next_situations = get_next_situations(situation, num_disks=self.num_disks, gradient=self.gradient)
            for next_situation, next_move in next_situations:
                if next_situation not in visited:
                    visited.add(next_situation)
                    new_path = path + [next_move]  # копия пути + новый ход
                    stack.append((next_situation, new_path, depth + 1))
                    # stack.append((next_situation, depth + 1, next_move))
                    any_moves_added = True

            # Если не добавили новых ходов и это не начальное состояние, откатываем
            # if move is not None and not any_moves_added:
            #     path.pop()
            #     visited.remove(situation)

        return None

    def solve_wide(self, current_situation: Any, goal_situation: Any, get_next_situations: callable) -> Optional[
        List[Tuple[str, str]]]:
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
            next_situations = get_next_situations(current_node.situation, num_disks=self.num_disks,
                                                  gradient=self.gradient)
            for next_situation, move in next_situations:
                if next_situation not in visited:
                    # Создаём новый узел с увеличенной глубиной
                    new_node = Node(next_situation, parent=current_node, move=move, depth=current_node.depth + 1)
                    current_node.add_child(new_node)
                    visited.add(next_situation)
                    queue.append(new_node)

        return None

    def solve_branches_and_bounds(self, current_situation: Any, goal_situation: Any, get_next_situations: callable) -> \
            Optional[List[Tuple[str, str]]]:
        """
        Ищет решение с стратегии ветвей и границ.
        Args:
            current_situation: Текущее состояние (например, кортежи дисков для A, B, C).
            goal_situation: Целевое состояние.
            get_next_situations: Функция, возвращающая список (next_situation, move) для возможных ходов.
        Returns:
            Список шагов (например, (source, destination)) или None, если решение не найдено.
        """
        # Инициализация дерева и очереди
        tree = Tree(current_situation)
        queue = []  # храним узлы в приоритетной очереди
        start_h = self._heuristic(current_situation)
        heapq.heappush(queue, (start_h, 0, tree.root))  # (f, g, node) упорядочиваем узлы

        visited = {current_situation: 0}  # Множество посещённых состояний
        best_cost = MAX_PATH  # длина кратчайшего пути
        goal_node = None  # узел с целевой ситуацией

        # g - текущее количество шагов от начального состояния,
        # для ханойской башни где каждый шаг равноценный - бесмысленно,
        # т.к. дублирует Node.deapth
        # но у нас же универсальный решатель)))
        # h - оценочное количество шагов до целевого состояния
        # f = g + h
        while queue:
            f, g, current_node = heapq.heappop(queue)

            # Если уже нашли путь короче — пропускаем
            if g > visited.get(current_node.situation, MAX_PATH):
                continue

            # Достигнута целевая ситуация? Если да, а вдруг есть путь короче?
            if current_node.situation == goal_situation:
                if g < best_cost:
                    best_cost = g
                    goal_node = current_node
                # А вдруг есть короче?
                continue

            # если f >= лучший_полный_путь - отбрасываем
            if best_cost != MAX_PATH and f >= best_cost:
                continue

            # Проверка на превышение максимальной глубины
            if g >= self.max_depth:
                continue

            # Получаем следующие возможные состояния
            next_situations = get_next_situations(current_node.situation, num_disks=self.num_disks,
                                                  gradient=self.gradient)
            for next_situation, move in next_situations:
                new_g = g + 1

                # Уже были с меньшим g?
                if next_situation in visited and visited[next_situation] <= new_g:
                    continue

                # Создаём новый узел с увеличенной глубиной
                new_node = Node(next_situation, parent=current_node, move=move, depth=current_node.depth + 1)
                current_node.add_child(new_node)
                visited[next_situation] = new_g

                h = self._heuristic(next_situation)
                f_new = new_g + h

                # если f_new >= лучший_полный - отбрасываем
                if best_cost != MAX_PATH and f_new >= best_cost:
                    continue

                heapq.heappush(queue, (f_new, new_g, new_node))

        return tree.get_path_to_node(goal_node) if goal_node else None
