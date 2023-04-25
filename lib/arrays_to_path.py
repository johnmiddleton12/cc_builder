from collections import deque

def find_next_block(matrix, current_pos):

    if current_pos == (-1, 0):
        current_pos = (0, 0)

    visited = set()
    queue = deque([current_pos])
    
    while queue:
        x, y = queue.popleft()
        
        if matrix[y][x] == 1:
            return (x, y)
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(matrix[0]) and 0 <= ny < len(matrix) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
    return None

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def array_to_path(matrix, fuel, starting_pos, layer):
    """Converts a 2D array of blocks to an array of positions for the turtle to move to

    If the turtle doesn't have enough fuel to make it to the next block, it will
    return to the position (-1, 0) to refuel. These positions are parsed separately

    Parameters:
    matrix (list): A 2D array of blocks
    fuel (int): The amount of fuel the turtle has
    starting_pos (tuple): The starting position of the turtle
    layer (int): The layer the turtle is currently on, used to calculate fuel usage
        going down to fuel layer and back up

    Returns:
    list: A list of positions for the turtle to move to
    int: The remaining fuel
    tuple: The final position of the turtle
    """

    print("Finding path...")
    # print("Starting position: {}".format(starting_pos))
    # print("Matrix: {}".format(matrix))
    matrix = [list(row) for row in matrix]
    current_pos = starting_pos
    path = [current_pos]
    remaining_fuel = fuel

    while True:
        next_block = find_next_block(matrix, current_pos)
        if next_block is None:
            break
        
        dist_to_block = distance(current_pos, next_block)
        dist_to_start = distance(next_block, (-1, 0))

        if dist_to_block + dist_to_start > remaining_fuel - (2 * (layer + 1)):
            if current_pos == (-1, 0):
                raise Exception("Not enough fuel to complete path")
            path.append((-1, 0))
            remaining_fuel = fuel
            current_pos = (-1, 0)
            continue
        
        path.append(next_block)

        remaining_fuel -= dist_to_block
        current_pos = next_block
        matrix[next_block[1]][next_block[0]] = 0

    return path, fuel, current_pos

if __name__ == "__main__":
    layer0 = [(1,1,1,1,1), (1,1,1,1,1), (1,1,1,1,1), (1,1,1,1,1), (1,1,1,1,1)]
    layer1 = [(0,0,0,0,0),(0,1,1,1,0),(0,1,1,1,0),(0,1,1,1,0),(0,0,0,0,1)]
    layer2 = [(0,0,0,0,0),(0,0,0,0,0),(0,0,1,0,0),(0,0,0,0,0),(0,0,0,0,0)]
    fuel = 100000
    # matrix = [(0, 0, 1), (1, 1, 1), (1, 0, 0)]
    # max_fuel = 11

    start_pos = (-1, 0)

    path0, fuel, start_pos = array_to_path(layer0, fuel, start_pos)
    path1, fuel, start_pos = array_to_path(layer1, fuel, start_pos)
    path2, fuel, start_pos = array_to_path(layer2, fuel, start_pos)

    print(path0)
    print(path1)
    print(path2)