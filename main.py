from HanoiTower import HanoiTower, get_next_situations
from Solver import Solver
from Rod import Rod

def main():
    try:
        num_disks = int(input("Введите количество дисков: "))
        if num_disks <= 0:
            raise ValueError("Количество дисков должно быть положительным.")

        num_moves = int(input("Введите максимальное количество шагов: "))
        if num_moves <= 0:
            num_moves = 2 ** num_disks - 1

        rods = {
            'A': Rod('A'),
            'B': Rod('B'),
            'C': Rod('C')
        }

        for disk in range(num_disks, 0, -1):
            rods['A'].push(disk)

        # rods['C'].push(3)  # Большой диск снизу
        # rods['C'].push(2)  # Средний диск
        # rods['A'].push(1)  # Малый диск на A

        game = HanoiTower(rods)
        print("Начальное состояние:")
        game.print_situation()

        solver = Solver(max_depth=num_moves)  # Оптимальная глубина для Ханойских башен
        # moves = solver.solve(game.get_situation(), game.target_situation, get_next_situations)
        moves = solver.solve_wide(game.get_situation(), game.target_situation, get_next_situations)

        # После получения moves:
        print("Путь валиден?", all((s, d) in [(s, d) for _, (s, d) in get_next_situations(game.get_situation())] for s, d in moves))

        if moves:
            print("Решение найдено:")
            for i, (source, destination) in enumerate(moves, 1):
                game.move_disk(source, destination)
            print(f"Решение завершено. Всего шагов: {game.get_move_count()}")
        else:
            print("Решение не найдено в пределах максимальной глубины.")

    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()