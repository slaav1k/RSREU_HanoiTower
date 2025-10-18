from typing import List, Any, Tuple

from Node import Node


class Tree:
    """Класс, представляющий дерево состояний."""
    def __init__(self, root_situation: Any):
        self.root = Node(situation=root_situation, depth=0)  # Корневой узел с начальным состоянием и глубиной 0

    def get_path_to_node(self, node: Node) -> List[Tuple[str, str]]:
        """Получить путь (список ходов) от корня до указанного узла."""
        path = []
        current = node
        while current.move is not None:
            path.append(current.move)
            current = current.parent
        return path[::-1]