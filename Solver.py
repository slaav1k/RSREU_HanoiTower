from typing import List, Tuple, Optional, Any

class Solver:
    """Универсальный решатель на основе поиска в глубину для задач с состояниями."""
    def __init__(self, max_depth: int = 7):
        self.max_depth = max_depth

    def solve(self, current_situation: Any, goal_situation: Any, get_next_situations: callable) -> Optional[List[Tuple[str, str]]]:
        """
        Ищет решение с помощью DFS.
        Args:
            current_situation: Текущее состояние (например, кортежи дисков для A, B, C).
            goal_situation: Целевое состояние.
            get_next_situations: Функция, возвращающая список (next_situation, move) для возможных ходов.
        Returns:
            Список шагов (например, (source, destination)) или None, если решение не найдено.
        """
        stack = [(current_situation, [], set([current_situation]), 0)]  # situation, path_moves, path_situations, depth
        while stack:
            situation, path, path_situations, depth = stack.pop()

            # 1. Достигнута целевая ситуация?
            if situation == goal_situation:
                return path

            # 2. Достигли лимита глубины?
            if depth >= self.max_depth:
                continue  # Тупик

            # 4. Есть другие ходы?
            for next_situation, move in get_next_situations(situation):
                # 3. Были ли мы в этой ситуации раньше? (только в текущем пути)
                if next_situation not in path_situations:
                    new_path = path + [move]
                    new_path_situations = path_situations.copy()
                    new_path_situations.add(next_situation)
                    stack.append((next_situation, new_path, new_path_situations, depth + 1))

        return None  # Решение не найдено в пределах глубины