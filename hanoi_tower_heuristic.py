from rod import Rod


class HanoiTowerHeuristic:
    """Класс, реализующий эвристическое решение Ханойских башен."""
    def __init__(self, num_disks):
        self.num_disks = num_disks
        self.rods = {
            'A': Rod('A'),
            'B': Rod('B'),
            'C': Rod('C')
        }
        self.move_count = 0
        self.visited = set()  # Множество для хранения посещённых состояний
        for disk in range(num_disks, 0, -1):
            self.rods['A'].push(disk)

    def print_state(self):
        """Вывести текущее состояние стержней."""
        for rod in self.rods.values():
            print(rod)
        print("-" * 30)

    def evaluate(self, state=None):
        """Оценочная функция: число дисков на стержне C."""
        if state is None:
            return len(self.rods['C'].disks)
        return len(state['C'].disks)

    def is_valid_move(self, source, dest):
        """Проверка допустимости хода."""
        if not self.rods[source].disks:
            return False
        source_disk = self.rods[source].disks[-1]
        if not self.rods[dest].disks:
            return True
        return source_disk < self.rods[dest].disks[-1]

    def get_possible_moves(self):
        """Вернуть список допустимых ходов."""
        moves = []
        for source in ['A', 'B', 'C']:
            for dest in ['A', 'B', 'C']:
                if source != dest and self.is_valid_move(source, dest):
                    moves.append((source, dest))
        return moves

    def get_state(self):
        """Получить строковое представление текущего состояния."""
        return str([(rod_name, rod.disks[:]) for rod_name, rod in self.rods.items()])

    def evaluate_after_move(self, move):
        """Оценить состояние после хода (для сортировки)."""
        source, dest = move
        source_disk = self.rods[source].disks[-1]
        self.rods[source].pop()
        self.rods[dest].push(source_disk)
        score = self.evaluate()
        self.rods[dest].pop()
        self.rods[source].push(source_disk)
        return score

    def solve(self):
        """Эвристический поиск в глубину."""
        self.visited.clear()
        def dfs():
            # Проверяем, достигнута ли цель
            if len(self.rods['C'].disks) == self.num_disks:
                return True
            # Проверяем, не посещали ли это состояние
            state = self.get_state()
            if state in self.visited:
                return False
            self.visited.add(state)
            # Получаем возможные ходы и сортируем по оценочной функции
            moves = self.get_possible_moves()
            moves.sort(key=lambda m: self.evaluate_after_move(m), reverse=True)
            for source, dest in moves:
                disk = self.rods[source].pop()
                self.rods[dest].push(disk)
                self.move_count += 1
                print(f"Шаг {self.move_count}: Переместить диск {disk} с {source} на {dest}")
                self.print_state()
                if dfs():
                    return True
                # Откатываем ход
                self.rods[dest].pop()
                self.rods[source].push(disk)
            return False

        if dfs():
            return True
        return False

    def get_move_count(self):
        """Вернуть общее количество шагов."""
        return self.move_count