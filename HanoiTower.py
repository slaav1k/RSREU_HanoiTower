from typing import Union, Dict, List, Tuple
from Rod import Rod

def score_situation(situation: Tuple[Tuple[int, ...], Tuple[int, ...], Tuple[int, ...]], num_disks: int) -> float:
    """
    Оценить состояние: меньший счёт = лучшее состояние.
    Критерии:
    - Количество дисков на стержне C, в правильном порядке (больше = лучше).
    - Количество дисков на A и B (меньше = лучше).
    """
    rod_a, rod_b, rod_c = situation
    score = 0.0

    target_c = tuple(range(num_disks, 0, -1))
    correct_disks = 0
    for i, disk in enumerate(rod_c):
        if i < len(target_c) and disk == target_c[i]:
            correct_disks += 1
    score -= 10 * correct_disks

    score += 5 * (len(rod_a) + len(rod_b))

    return score

def get_next_situations(situation: Tuple[Tuple[int, ...], Tuple[int, ...], Tuple[int, ...]], num_disks: int, gradient: bool = False) -> List[Tuple[Tuple[Tuple[int, ...], Tuple[int, ...], Tuple[int, ...]], Tuple[str, str]]]:
    """Генерировать возможные следующие состояния и соответствующие ходы."""
    rod_names = ['A', 'B', 'C']
    rods = {name: list(disks) for name, disks in zip(rod_names, situation)}  # Временные списки для симуляции

    next_situations = []
    for source_idx, source in enumerate(rod_names):
        if not rods[source]:
            continue
        disk = rods[source][-1]  # Верхний диск
        for dest_idx, dest in enumerate(rod_names):
            if source == dest:
                continue
            if not rods[dest] or rods[dest][-1] > disk:  # Можно перемещать только на больший диск или пустой
                # Симулировать ход
                new_rods = {k: v[:] for k, v in rods.items()}
                new_rods[source].pop()
                new_rods[dest].append(disk)
                new_situation = (
                    tuple(new_rods['A']),
                    tuple(new_rods['B']),
                    tuple(new_rods['C'])
                )
                next_situations.append((new_situation, (source, dest)))

    if gradient:
        next_situations.sort(key=lambda x: score_situation(x[0], num_disks), reverse=True)

    return next_situations


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
            for disk in range(self.num_disks, 0, -1):
                self.rods['A'].push(disk)
        elif isinstance(num_disks_or_rods, dict):
            # Второй случай: инициализация с заданными стержнями
            self.rods: Dict[str, Rod] = num_disks_or_rods
            self.num_disks: int = sum(len(rod.disks) for rod in num_disks_or_rods.values())
        else:
            raise TypeError("Аргумент должен быть либо int, либо Dict[str, Rod]")

        # Целевая ситуация: все диски на стержне C в порядке [num_disks, ..., 1]
        self.target_situation: Tuple[Tuple[int, ...], Tuple[int, ...], Tuple[int, ...]] = (
            (),  # A пусто
            (),  # B пусто
            tuple(range(self.num_disks, 0, -1))  # C: [n, n-1, ..., 1]
        )

        # Проверка начальной ситуации
        self.validate_initial_situation()

    def validate_initial_situation(self) -> None:
        """Проверить, что диски лежат правильно: на каждом стержне от большого к малому снизу вверх,
        все диски уникальны и от 1 до num_disks."""
        all_disks = []
        for rod in self.rods.values():
            disks = rod.disks
            # Проверка порядка: должен быть убывающим (большой снизу [начало списка], малый сверху [конец])
            if disks and disks != sorted(disks, reverse=True):
                raise ValueError(f"Диски на стержне {rod.name} не в правильном порядке: должны быть от большого к малому снизу вверх.")
            all_disks.extend(disks)

        # Проверка уникальности и полноты
        if sorted(all_disks) != list(range(1, self.num_disks + 1)):
            raise ValueError("Не все диски присутствуют, есть дубликаты или неверные значения (должны быть от 1 до num_disks).")

    def move_disk(self, source: str, destination: str) -> None:
        """Переместить диск с одного стержня на другой."""
        disk = self.rods[source].pop()
        if disk is not None:
            if not self.rods[destination].disks or self.rods[destination].disks[-1] > disk:
                self.rods[destination].push(disk)
                self.move_count += 1
                self.print_move(disk, source, destination)
                self.print_situation()
            else:
                self.rods[source].push(disk)  # Вернуть диск обратно
                print(f"Нельзя переместить диск {disk} на {destination}: нарушен порядок (нельзя класть больший на меньший).")
                # raise ValueError(f"Нельзя переместить диск {disk} на {destination}: нарушен порядок (нельзя класть больший на меньший).")

    def print_move(self, disk: int, source: str, destination: str) -> None:
        """Вывести шаг перемещения диска."""
        print(f"Шаг {self.move_count}: Переместить диск {disk} с {source} на {destination}")

    def print_situation(self) -> None:
        """Вывести текущее состояние стержней."""
        for rod in self.rods.values():
            print(rod)
        print("-" * 30)

    @staticmethod
    def print_given_situation(rods: Dict[str, Rod]) -> None:
        """Вывести состояние переданных стержней."""
        for rod in rods.values():
            print(rod)
        print("-" * 30)

    def get_move_count(self) -> int:
        """Вернуть общее количество шагов."""
        return self.move_count

    def is_solved(self) -> bool:
        """Проверить, достигнута ли целевая ситуация."""
        return self.get_situation() == self.target_situation

    def get_situation(self) -> Tuple[Tuple[int, ...], Tuple[int, ...], Tuple[int, ...]]:
        """Получить текущее состояние как кортеж кортежей дисков (A, B, C)."""
        return (
            tuple(self.rods['A'].disks),
            tuple(self.rods['B'].disks),
            tuple(self.rods['C'].disks)
        )

