class PriorityQueue:
    def __init__(self):
        self._heap = []

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self._heap[index][0] > self._heap[parent][0]:
            self._swap(index, parent)
            self._heapify_up(parent)

    def _heapify_down(self, index):
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        highest = index
        if (left_child < len(self._heap) and
            self._heap[left_child][0] > self._heap[highest][0]):
            highest = left_child
        if (right_child < len(self._heap) and
            self._heap[right_child][0] > self._heap[highest][0]):
            highest = right_child
        if highest != index:
            self._swap(index, highest)
            self._heapify_down(highest)

    def insert(self, item, priority):
        self._heap.append((priority, item))
        self._heapify_up(len(self._heap) - 1)

    def pop(self):
        if len(self._heap) == 1:
            return self._heap.pop()[1]
        else:
            item = self._heap[0][1]
            self._heap[0] = self._heap.pop()
            self._heapify_down(0)
            return item

    def peek(self):
        return self._heap[0][1]

    def isEmpty(self):
        return len(self._heap) == 0