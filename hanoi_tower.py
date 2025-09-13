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
            self.print_move(disk, source, destination)
            self.print_state()

    def print_move(self, disk, source, destination):
        """Вывести шаг перемещения диска."""
        print(f"Шаг {self.move_count}: Переместить диск {disk} с {source} на {destination}")

    def print_state(self):
        """Вывести текущее состояние стержней."""
        for rod in self.rods.values():
            print(rod)
        print("-" * 30)

    def get_move_count(self):
        """Вернуть общее количество шагов."""
        return self.move_count