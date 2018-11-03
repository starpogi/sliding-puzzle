import collections
import math


MARKER = 0


class Point:

    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index


class Vertex:

    def __init__(self, value, marker=MARKER):
        self.value = value
        self.parent = None

        side_len = math.sqrt(len(self.value))

        if int(side_len) != side_len:
            raise ValueError("Grid has to be a square!")

        self.side_len = int(side_len)

        marker_index = self.value.index(marker)
        marker_x = marker_index % self.side_len
        marker_y = marker_index // self.side_len

        self.marker = Point(marker_x, marker_y, marker_index)

    def __repr__(self):
        return "%s" % self.value

    @property
    def pretty(self):
        grid = []

        for y in range(self.side_len):
            start = y * self.side_len
            end = (y * self.side_len) + self.side_len
            grid.append(" ".join(["%-2s" % x for x in self.value[start:end]]))

        return "\n".join([str(row) for row in grid])


def solve(vertex, solution):
    """
    TODO: Change algorithm from O(4^n) to O(n^4) or better.

    Potentially a selection sort, where if the swap index falls on the MARKER
    then do a shift.

    1 2
    3 *

    * 1 3 2

    * 1
    3 2


    3 1 * 2             1 * 3 2

    3 1                 1 *
    * 2                 3 2

    3 1                 1 2
    2 *                 3 *

    3 *
    2 1

    * 3
    2 1
    """
    candidates = []
    visited, queue = set(), collections.deque([vertex])

    while queue:
        vertex = queue.popleft()

        if vertex.value == solution:
            candidates.append(vertex)
            break

        moves = find_moves(vertex)

        for move in moves:
            new_vertex = Vertex(move)
            new_vertex.parent = vertex

            if str(new_vertex.value) not in visited:
                visited.add(str(new_vertex.value))
                queue.append(new_vertex)

            if new_vertex.value == solution:
                candidates.append(new_vertex)
                break

    return candidates


def show_path(vertex):
    path = []

    while vertex:
        path.append(vertex)
        vertex = vertex.parent

    return path


def find_neighbor_indices(vertex):
    """
    Return the indices of its 2D equivalent neighbors in a 1D array
    """
    neighbors = [
        vertex.marker.index - vertex.side_len,  # UP
        vertex.marker.index + vertex.side_len,  # DOWN
        vertex.marker.index - 1,                # LEFT
        vertex.marker.index + 1                 # RIGHT
    ]

    # Boundary checks
    # Check if we are in any boundary
    if vertex.marker.x == 0:
        del neighbors[2]

    if vertex.marker.x == vertex.side_len - 1:
        del neighbors[3]

    if vertex.marker.y == 0:
        del neighbors[0]

    if vertex.marker.y == vertex.side_len - 1:
        del neighbors[1]

    return neighbors


def find_moves(vertex):
    """ Lists all the possible moves for a marker piece indicated
    by MARKER. Max move one spot on all directions.

    1. Given
        1, 2, 3, 4, *, 5, 6, 7, 8

        or

        1 2 3
        4 * 5
        6 7 8

    2. Get the sqrt of the length
        3

    3. Do modulus math to find the x, y coordinates of a linear array element.
        x = index % side_len
        y = index // side_len

    4. Determine immediate neighbors with math.

    """
    moves = []
    mi = vertex.marker.index

    for neighbor in find_neighbor_indices(vertex):
        new_value = vertex.value[:]
        new_value[neighbor], new_value[mi] = new_value[mi], new_value[neighbor]
        moves.append(new_value)

    return moves

vertex = Vertex([1, 2, 3, 4, MARKER, 5, 6, 7, 8])
solutions = sorted([show_path(path)
                    for path in solve(vertex, [1, 2, 3, 4, 5, 6, 7, 8, MARKER])],
                   key=lambda x: len(x))

if solutions:
    for n in reversed(solutions[0]):
        print("-------")
        print(n.pretty)
        print("-------\n   |    \n   V    \n")
