class HanoiSolver:
    """Класс для решения задачи Ханойских башен."""
    def __init__(self):
        self.moves = []

    def solve(self, game, n=None, source='A', auxiliary='B', destination='C'):
        """Рекурсивно решает задачу Ханойских башен и возвращает список шагов."""
        if n is None:
            n = game.num_disks

        if n > 0:
            # Переместить n-1 дисков с source на auxiliary через destination
            self.solve(game, n - 1, source, destination, auxiliary)
            # Добавить шаг перемещения n-го диска с source на destination
            self.moves.append((source, destination))
            # Выполнить перемещение в игре
            game.move_disk(source, destination)
            # Переместить n-1 дисков с auxiliary на destination через source
            self.solve(game, n - 1, auxiliary, source, destination)

        return self.moves

    def get_solution(self, game):
        """Возвращает список шагов для решения задачи."""
        self.moves = []
        return self.solve(game)