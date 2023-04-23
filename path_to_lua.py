def generate_instructions(a, b, direction):
    # a and b are tuples representing coordinates
    # e.g. (0, 0) and (1, 1)
    instructions = []


def algo_to_lua(path):

    # path is a list of tuples, each tuple is a coordinate
    # e.g. [(0,0), (1,0), (2,0), (2,1), (2,2), (1,2), (0,2), (0,1), (0,0)]

    # The turtle will start at (0,0) and face east, which is the positive x direction

    # directions:
    # 0 = north
    # 1 = east
    # 2 = south
    # 3 = west

    # This program generates the instructions to get the turtle from (0,0) to (0,0) again

    # if the turtle ever comes back to (0,0) it will refuel

    instructions = []

    for i in range(len(path) - 1):

if __name__ == "__main__":

    path = [(0, 0), (1, 1), (2, 1), (3, 1), (3, 2), (2, 2), (1, 2), (1, 3), (2, 3), (3, 3), (0, 0)]

    instructions = algo_to_lua(path)
