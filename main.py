import collections


MARKER = "*"


def to_mat(array):
    return [array[0:3]] + [array[3:6]] + [array[6:9]]


class Vertex:

    def __init__(self, value):
        self.value = value
        self.parent = None

    def __repr__(self):
        return "%s" % to_mat(self.value)


def solve(vertex, solution):
    candidates = []
    visited, queue = set(), collections.deque([vertex])

    while queue:
        vertex = queue.popleft()

        if vertex.value == solution:
            candidates.append(vertex)
            break

        moves = find_moves(vertex.value)

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


def find_moves(array):
    """ Lists all the possible moves for a marker piece indicated
    by MARKER. Max move one spot on all directions.
    """
    moves = []

    x, y = 0, 0
    array = to_mat(array)

    for row, row_val in enumerate(array):
        for col, _ in enumerate(row_val):
            if array[row][col] == MARKER:
                x = col
                y = row

    shifts = []

    # UP
    if y - 1 >= 0:
        shifts.append((x, y - 1))

    # DOWN
    if y + 1 < 3:
        shifts.append((x, y + 1))

    # LEFT
    if x - 1 >= 0:
        shifts.append((x - 1, y))

    # RIGHT
    if x + 1 < 3:
        shifts.append((x + 1, y))

    # marker_index = array.index(MARKER)
    #
    # # Backward 2
    # backward = [marker_index - ((i + 1) * 2) + 1
    #             for i, _ in enumerate(array[:marker_index][1::-2][:2])]
    # print(backward)
    # # Forward 2
    # forward = [marker_index + ((i + 1) * 2) - 1
    #            for i, _ in enumerate(array[marker_index + 1:][1::2][:2])]
    # print(forward)
    # shifts = forward + backward
    #
    for shift in shifts:
        move = [row[:] for row in array]
        sx, sy = shift
        move[sy][sx], move[y][x] = move[y][x], move[sy][sx]
        moves.append(move[0] + move[1] + move[2])

    return moves

vertex = Vertex([1, 2, 3, 4, "*", 5, 6, 7, 8])
solutions = sorted([show_path(path)
                    for path in solve(vertex, [1, 2, 3, 4, 5, 6, 7, 8, "*"])],
                   key=lambda x: len(x))

if solutions:
    x = solutions[1]

    for n in x:
        y = n.value
        print("%-2s %-2s %-2s\n%-2s %-2s %-2s\n%-2s %-2s %-2s\n" % (
            y[0], y[1], y[2],
            y[3], y[4], y[5],
            y[6], y[7], y[8]
        ))
