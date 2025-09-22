class Node:
    def __init__(self, data: int, next = None):
        self.data: int = data
        self.next: Node | None = next


class List:
    def __init__(self, head: Node | None = None):
        self.head: Node | None = head
        self.tail: Node | None = head

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

    # Method - Get a node at specific index
    def at(self, index: int) -> Node | None:
        node: Node | None = self.head

        # Find node at index, starts from 0
        for i in range(index):
            if node is None:
                return
            node = node.next

        return node

    # Method - Push data
    def push_front(self, data: int) -> None:
        node: Node = Node(data)
        if self.head == self.tail and self.tail is None:
            self.tail = node
        else:
            node.next = self.head
        self.head = node

    def push_back(self, data: int) -> None:
        node: Node = Node(data)
        if self.head == self.tail and self.head is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node

    # Method - Pop data
    def pop_back(self) -> None:
        node: Node | None = self.tail

        if node is None:
            return

        # Find 2nd last node
        tail: Node = self.head
        while tail.next is not node:
            tail = tail.next

        # Update tail
        self.tail = tail
        self.tail.next = None

        # Remove the tail
        del node

    def pop_front(self) -> None:
        node: Node | None = self.head

        if node is None:
            return

        # Update head
        self.head = self.head.next
        node.next = None

        # Remove head
        del node

    def __repr__(self) -> str:
        _: str = ''
        node: Node | None = self.head
        while node is not None:
            _ += str(node.data) + '->'
            node = node.next
        return _ + 'None'


if __name__ == '__main__':
    _list: List = List()

    _list.push_back(2)
    _list.push_back(1)
    _list.push_back(5)
    _list.push_back(3)
    _list.push_back(4)

    # print('Original:', _list, sep='\t')

    # Sort the list -- Bubble Sort Algorithm
    size: int = _list.size
    for i in range(size - 1):
        swapped: bool = False

        for j in range(size - i - 1):
            node1: Node = _list.at(j)
            node2: Node = node1.next

            # Debugging...
            print('List:\t', _list)
            print(f"Node1:\t{node1 if node1 is None else node1.data} | Node2:\t{node2 if node2 is None else node2.data}",
                  f"Head:\t{_list.head.data} | Tail:\t{_list.tail.data}", sep=' || ')

            # Compare & Swap
            if node1.data > node2.data:
                # Update head
                if _list.head is node1:
                    _list.head = node2

                # Update tail
                if _list.tail is node2:
                    _list.tail = node1

                # Swap nodes
                node1.next = node2.next
                node2.next = node1

                swapped = True

            if swapped:
                # Debugging...
                print("[Swapped]")
                n1: Node = _list.at(j)
                n2: Node = n1.next
                print(
                    f"Node1:\t{n1 if n1 is None else n1.data} | Node2:\t{n2 if n2 is None else n2.data}",
                    f"Head:\t{_list.head.data} | Tail:\t{_list.tail.data}", sep=' || ', end='\n\n')

            # Break the loop if no swap happened
            if not swapped:
                i = size    # Outer loop
                break       # Inner loop

    # print('Sorted:', _list, sep='\t')
