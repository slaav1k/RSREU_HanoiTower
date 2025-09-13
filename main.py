from hanoi_tower import HanoiTower
from hanoi_solver import HanoiSolver

def main():
    try:
        num_disks = int(input("Введите количество дисков: "))
        if num_disks <= 0:
            raise ValueError("Количество дисков должно быть положительным.")

        game = HanoiTower(num_disks)
        print("Начальное состояние:")
        game.print_state()

        solver = HanoiSolver()
        print("Решение:")
        moves = solver.get_solution(game)
        print(f"Решение завершено. Всего шагов: {game.get_move_count()}")
        # print("Список шагов:", moves)

    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()