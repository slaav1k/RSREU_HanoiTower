from rod import Rod


class HanoiTower:
    """Класс, реализующий игру Ханойские башни."""
    def __init__(self, num_disks):
        self.num_disks = num_disks  # Количество дисков
        self.rods = {
            'A': Rod('A'),
            'B': Rod('B'),
            'C': Rod('C')
        }
        self.move_count = 0  # Счётчик шагов

        # Инициализация начального стержня A с дисками
        for disk in range(num_disks, 0, -1):
            self.rods['A'].push(disk)

    def move_disk(self, source, destination):
        """Переместить диск с одного стержня на другой."""
        disk = self.rods[source].pop()
        if disk is not None:
            self.rods[destination].push(disk)
            self.move_count += 1
            print(f"Шаг {self.move_count}: Переместить диск {disk} с {source} на {destination}")
            self.print_state()

    def print_state(self):
        """Вывести текущее состояние стержней."""
        for rod in self.rods.values():
            print(rod)
        print("-" * 30)

    def solve(self, n=None, source='A', auxiliary='B', destination='C'):
        """Рекурсивно решить задачу Ханойских башен."""
        if n is None:
            n = self.num_disks

        if n > 0:
            # Переместить n-1 дисков с source на auxiliary через destination
            self.solve(n - 1, source, destination, auxiliary)
            # Переместить n-й диск с source на destination
            self.move_disk(source, destination)
            # Переместить n-1 дисков с auxiliary на destination через source
            self.solve(n - 1, auxiliary, source, destination)

    def get_move_count(self):
        """Вернуть общее количество шагов."""
        return self.move_count