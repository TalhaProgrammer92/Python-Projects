class Node:
    def __init__(self, data: int, next = None):
        self.data: int = data
        self.next: Node | None = next

class List:
    def __init__(self, head: Node | None = None):
        self.head = head

    @property
    def data_list(self) -> list[int]:
        data: list[int] = []
        node: Node | None = self.head
        while node is not None:
            data.append(node.data)
            node = node.next

        return data

    @property
    def size(self) -> int:
        return len(self.data_list)

    # Method - Push data
    def push_front(self, data: int) -> None:
        node: Node = Node(data, self.head)
        self.head = node

    def __repr__(self) -> str:
        _: str = ''
        node: Node | None = self.head
        while node is not None:
            _ += str(node.data) + '->'
            node = node.next
        return _ + 'None'


if __name__ == '__main__':
    _list: List = List()

    _list.push_front(5)
    _list.push_front(4)
    _list.push_front(3)
    _list.push_front(2)
    _list.push_front(1)

    print(_list)
