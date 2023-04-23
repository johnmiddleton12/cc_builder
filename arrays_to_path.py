from collections import deque

def find_next_block(matrix, current_pos):
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

def find_path_to_next_block(matrix, current_pos):
    visited = set()
    queue = deque([(current_pos, [])])

    while queue:
        (x, y), path = queue.popleft()
        
        if matrix[y][x] == 1:
            return path
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(matrix[0]) and 0 <= ny < len(matrix) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))
    return None

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def turtle_path(matrix, max_fuel):
    matrix = [list(row) for row in matrix]
    current_pos = (0, 0)
    path = [current_pos]
    remaining_fuel = max_fuel

    while True:
        # next_block = find_next_block(matrix, current_pos)
        # if next_block is None:
            # break
        
        path_to_next_block = find_path_to_next_block(matrix, current_pos)
        if path_to_next_block is None:
            break

        next_block = path_to_next_block[0]
        
        dist_to_block = distance(current_pos, next_block)
        dist_to_start = distance(next_block, (0, 0))

        #TODO: add the path to the start from last block visited 

        if dist_to_block + dist_to_start > remaining_fuel:
            path.append((0, 0))
            remaining_fuel = max_fuel

        #TODO: add the path from the start to the next block
        
        path.append(next_block)
        remaining_fuel -= dist_to_block
        current_pos = next_block
        matrix[next_block[1]][next_block[0]] = 0

    path.append((0, 0))
    return path

if __name__ == "__main__":
    matrix = [(0,0,0,0,0),(0,1,1,1,0),(0,1,1,1,0),(0,1,1,1,0),(0,0,0,0,0)]
    # matrix = [(0, 0, 1), (1, 1, 1), (1, 0, 0)]
    max_fuel = 11
    # max_fuel = 6
    print(turtle_path(matrix, max_fuel))