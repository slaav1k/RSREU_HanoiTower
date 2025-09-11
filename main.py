from hanoi_tower import HanoiTower
from hanoi_tower_heuristic import HanoiTowerHeuristic


def main():
    try:
        num_disks = int(input("Введите количество дисков: "))
        if num_disks <= 0:
            raise ValueError("Количество дисков должно быть положительным.")

        # game = HanoiTower(num_disks)
        game = HanoiTowerHeuristic(num_disks)
        print("Начальное состояние:")
        game.print_state()
        print("Решение:")
        game.solve()
        print(f"Решение завершено. Всего шагов: {game.get_move_count()}")

    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()