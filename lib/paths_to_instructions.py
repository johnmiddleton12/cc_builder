def generate_direction_instruction(direction, correct_direction):
    """Generates instructions to turn from one direction to another

    Parameters:
    direction (int): The current direction
    correct_direction (int): The direction to turn to

    Returns:
    list: A list of instructions to turn from one direction to another
    """

    instructions = []

    if direction == correct_direction:
        return instructions

    if direction == 0:
        if correct_direction == 1:
            instructions.append("turnRight()")
        elif correct_direction == 2:
            instructions.append("turnRight()")
            instructions.append("turnRight()")
        elif correct_direction == 3:
            instructions.append("turnLeft()")
    elif direction == 1:
        if correct_direction == 0:
            instructions.append("turnLeft()")
        elif correct_direction == 2:
            instructions.append("turnRight()")
        elif correct_direction == 3:
            instructions.append("turnRight()")
            instructions.append("turnRight()")
    elif direction == 2:
        if correct_direction == 0:
            instructions.append("turnRight()")
            instructions.append("turnRight()")
        elif correct_direction == 1:
            instructions.append("turnLeft()")
        elif correct_direction == 3:
            instructions.append("turnRight()")
    elif direction == 3:
        if correct_direction == 0:
            instructions.append("turnRight()")
        elif correct_direction == 1:
            instructions.append("turnRight()")
            instructions.append("turnRight()")
        elif correct_direction == 2:
            instructions.append("turnLeft()")

    return instructions

def generate_ptp_instructions(a, b, direction):
    """Generate point to point instructions for the turtle to follow

    Parameters:
    a (tuple): a tuple representing the starting point
    b (tuple): a tuple representing the ending point
    direction (int): the direction the turtle is facing

    Returns:
    list: a list of instructions for the turtle to follow
    int: the direction the turtle is facing after the instructions are executed
    """
    instructions = []

    # Correct x coordinate first
    # face right direction

    if a[0] < b[0]:
        # face east
        instructions.extend(generate_direction_instruction(direction, 1))
        direction = 1
    elif a[0] > b[0]:
        # face west
        instructions.extend(generate_direction_instruction(direction, 3))
        direction = 3

    # move to correct x coordinate
    for i in range(abs(a[0] - b[0])):
        instructions.append("forward()")

    # Correct y coordinate
    # face right direction

    if a[1] < b[1]:
        # face south
        instructions.extend(generate_direction_instruction(direction, 2))
        direction = 2
    elif a[1] > b[1]:
        # face north
        instructions.extend(generate_direction_instruction(direction, 0))
        direction = 0

    # move to correct y coordinate
    for i in range(abs(a[1] - b[1])):
        instructions.append("forward()")

    return instructions, direction

def path_to_instructions(path, layer, direction, items, slot):
    """Generates a list of instructions for the turtle to follow to build the path

    The path generated will take into account the amount of items the turtle has,
    and will return to (-1, 0, 0) to collectItems when it runs out of items

    Parameters:
    path (list): a list of tuples representing the path the turtle will take
    layer (int): the layer the turtle is currently on
    direction (int): the direction the turtle is facing
    items (int): the amount of items the turtle has
    slot (int): the slot the turtle is currently selected on

    Returns:
    list: a list of instructions for the turtle to follow
    int: the direction the turtle is facing after the instructions are executed
    int: the amount of items the turtle has left
    int: the updated slot the turtle is selected on
    """

    instructions = []

    for i in range(1, len(path)):

        # go to the next coordinate
        new_instructions, direction = generate_ptp_instructions(path[i - 1], path[i], direction)
        instructions.extend(new_instructions)

        # if the turtle is at (-1, 0), generate instructions to refuel
        if path[i] == (-1, 0):
            instructions.extend(generate_refuel_instructions(direction, layer))
            direction = 0
        else:
            instructions.append("placeDown()")
            items -= 1

        if items == 0:
            if slot == 16:
                instructions.extend(generate_item_collection_instructions(path[i], direction, layer))
                slot = 1
            else:
                instructions.append("turtle.select(" + str(slot + 1) + ")")
                slot += 1
            items = 64

    return instructions, direction, items, slot

def generate_item_collection_instructions(current_pos, current_direction, layer):
    instructions = []

    # go to (-1, 0)
    go_back, direction = generate_ptp_instructions(current_pos, (-1, 0), current_direction)
    instructions.extend(go_back)
    # face east at (-1, 0)
    instructions.extend(generate_direction_instruction(direction, 1))

    for i in range(layer + 2):
        instructions.append("down()")

    instructions.append("turnRight()")
    instructions.append("collectItems()")
    instructions.append("turnLeft()")

    for i in range(layer + 2):
        instructions.append("up()")

    go_back, direction = generate_ptp_instructions((-1, 0), current_pos, 1)
    instructions.extend(go_back)
    instructions.extend(generate_direction_instruction(direction, current_direction))

    return instructions

def generate_refuel_instructions(direction, layer):
    """Generates a list of instructions for the turtle to follow to refuel

    Assumes a starting position of (-1, 0, layer)
    Creates an ending position of (-1, 0, layer), facing north (0)

    Parameters:
    direction (int): the direction the turtle is facing
    layer (int): the layer the turtle is currently on

    Returns:
    list: a list of instructions for the turtle to follow
    """
    instructions = []
    instructions.extend(generate_direction_instruction(direction, 0))
    for i in range(layer + 2):
        instructions.append("down()")
    instructions.append("refuel()")
    for i in range(layer + 2):
        instructions.append("up()")
    return instructions

def paths_to_instructions(paths):
    """Given a list of paths, generate a list of instructions for the turtle to follow

    Parameters:
    paths (list): a list of paths, where each path is a list of tuples representing coordinates

    Returns:
    list: a list of instructions for the turtle to follow
    """

    print("Generating instructions...")

    instructions = []

    # starting values for turtle
    direction = 1
    itemCount = 64
    slot = 1

    # generate instructions for each layer's path
    for i in range(len(paths)):
        new_instructions, direction, itemCount, slot = path_to_instructions(paths[i], i, direction, itemCount, slot)
        instructions.extend(new_instructions)

        # if there is another layer, go up
        if i != len(paths) - 1:
            instructions.append("up()")

    # go to starting x, z
    go_back, direction = generate_ptp_instructions(paths[-1][-1], (-1, 0), 1)
    instructions.extend(go_back)

    # face north
    instructions.extend(generate_direction_instruction(direction, 0))

    # go to starting y
    for i in range(len(paths) + 2):
        instructions.append("down()")

    return instructions

if __name__ == "__main__":

    path = [(-1, 0), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (3, 1), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (4, 3), (3, 3), (2, 3), (1, 3), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]
    path2 = [(4, 4), (4, 4), (3, 3), (2, 3), (1, 3), (1, 2), (2, 2), (3, 2), (3, 1), (2, 1), (1, 1)]

    instructions = paths_to_instructions([path, path2])
    print(instructions)

    exit()
    import turtle

    layer = 2

    turtle.up()
    turtle.goto(-300, 300)
    turtle.down()
    turtle.color("brown")
    turtle.dot(30) # refuel
    turtle.up()
    turtle.goto(-300, 200)
    turtle.color("red") # -1, 0
    turtle.down()
    turtle.dot(30)
    turtle.up()
    turtle.goto(-300, 100)
    turtle.color("brown") # chest
    turtle.down()
    turtle.dot(30)
    turtle.up()
    turtle.goto(-200, 200)

    for i in range(5):
        for j in range(5):
            turtle.color("gray")
            turtle.down()
            turtle.dot(30)
            turtle.up()
            turtle.forward(100)
        turtle.back(500)
        turtle.right(90)
        turtle.forward(100)
        turtle.left(90)

    turtle.goto(-200, 200)

    turtle.speed(1)

    for i in range(len(instructions)):
        print(turtle.position())
        if instructions[i] == "forward()":
            turtle.forward(100)
        elif instructions[i] == "back()":
            turtle.back(100)
        elif instructions[i] == "turnLeft()":
            turtle.left(90)
        elif instructions[i] == "turnRight()":
            turtle.right(90)
        elif instructions[i] == "up()":
            layer += 1
            print(layer)
        elif instructions[i] == "down()":
            layer -= 1
            print(layer)
        elif instructions[i] == "placeDown()":
            turtle.color("red")
            turtle.down()
            turtle.dot(30)
            turtle.up()
        elif instructions[i] == "refuel()":
            turtle.color("green")
            turtle.down()
            turtle.dot(30)
            turtle.up()

    turtle.exitonclick()

    print(instructions)