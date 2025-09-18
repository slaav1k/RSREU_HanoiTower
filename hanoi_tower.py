from typing import Union, Dict
from rod import Rod

class HanoiTower:
    """Класс, реализующий игру Ханойские башни."""
    def __init__(self, num_disks_or_rods: Union[int, Dict[str, Rod]]) -> None:
        """
        Инициализация игры Ханойские башни.
        Args:
            num_disks_or_rods: Либо количество дисков (int), либо словарь со стержнями (Dict[str, Rod]).
        """
        self.move_count: int = 0  # Счётчик шагов

        if isinstance(num_disks_or_rods, int):
            # Первый случай: инициализация с числом дисков
            self.num_disks: int = num_disks_or_rods
            self.rods: Dict[str, Rod] = {
                'A': Rod('A'),
                'B': Rod('B'),
                'C': Rod('C')
            }
            # Инициализация начального стержня A с дисками
            for disk in range(num_disks_or_rods, 0, -1):
                self.rods['A'].push(disk)
        elif isinstance(num_disks_or_rods, dict):
            # Второй случай: инициализация с заданными стержнями
            self.rods: Dict[str, Rod] = num_disks_or_rods
            self.num_disks: int = sum(len(x.disks) for x in num_disks_or_rods.values())
        else:
            raise TypeError("Аргумент должен быть либо int, либо Dict[str, Rod]")

    def move_disk(self, source, destination) -> None:
        """Переместить диск с одного стержня на другой."""
        disk = self.rods[source].pop()
        if disk is not None:
            self.rods[destination].push(disk)
            self.move_count += 1
            self.print_move(disk, source, destination)
            self.print_situation()

    def print_move(self, disk, source, destination) -> None:
        """Вывести шаг перемещения диска."""
        print(f"Шаг {self.move_count}: Переместить диск {disk} с {source} на {destination}")

    def print_situation(self):
        """Вывести текущее состояние стержней."""
        for rod in self.rods.values():
            print(rod)
        print("-" * 30)

    @staticmethod
    def print_given_situation(rods: Dict[str, Rod]) -> None:
        """Вывести состояние переданных стержней.
        Args:
            rods: Словарь стержней (Dict[str, Rod]).
        """
        for rod in rods.values():
            print(rod)
        print("-" * 30)

    def get_move_count(self) -> int:
        """Вернуть общее количество шагов."""
        return self.move_count