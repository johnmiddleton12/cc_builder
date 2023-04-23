def generate_direction_instruction(direction, correct_direction):

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

def generate_instructions(a, b, direction, items=-1):
    # a and b are tuples representing coordinates
    # e.g. (0, 0) and (1, 1)

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

    if b != (-1, 0):
        instructions.append("placeDown()")
        if items != -1:
            items -= 1

    if items == -1:
        return instructions, direction
    else:
        return instructions, direction, items

def path_to_instructions(path, layer, items, slot):

    # path is a list of tuples, each tuple is a coordinate
    # e.g. [(0,0), (1,0), (2,0), (2,1), (2,2), (1,2), (0,2), (0,1), (0,0)]

    instructions = []
    direction = 1

    for i in range(len(path) - 1):

        # if there is a (-1, 0) in the path, it means the turtle has to refuel
        if i != 0 and path[i] == (-1, 0) and path[i - 1] != (-1, 0):
            instructions.extend(generate_refuel_instructions(direction, layer))
            direction = 1

        if items == 0:
            if slot == 16:
                instructions.extend(generate_item_collection_instructions(path[i], direction, layer))
                slot = 1
            else:
                instructions.append("turtle.select(" + str(slot + 1) + ")")
                slot += 1
            items = 64

        #TODO: gross case - this might not be necessary, as the code to generate instructions and place a block is run for
        # duplicate coordinates, but it might be more efficient to just check for duplicates and not run the code
        if path[i] == path[i + 1] and (path[i + 1] != (-1, 0)):
            instructions.append("placeDown()")
            items -= 1
        else:
            new_instructions, direction, items = generate_instructions(path[i], path[i + 1], direction, items)
            instructions.extend(new_instructions)

    # make sure the turtle ends up facing east
    # instructions.append("start of correcting to east")
    instructions.extend(generate_direction_instruction(direction, 1))
    # instructions.append("end of correcting to east")

    return instructions, items, slot

def generate_item_collection_instructions(current_pos, current_direction, layer):
    instructions = []

    # go to (-1, 0)
    go_back, direction = generate_instructions(current_pos, (-1, 0), current_direction)
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

    go_back, direction = generate_instructions((-1, 0), current_pos, 1)
    instructions.extend(go_back)
    instructions.extend(generate_direction_instruction(direction, current_direction))

    return instructions

def generate_refuel_instructions(direction, layer, gainLayer=False):
    instructions = []

    instructions.extend(generate_direction_instruction(direction, 1))

    # accounted for this by setting refuel location to be (-1, 0)
    # instructions.append("back()")

    for i in range(layer + 2):
        instructions.append("down()")

    instructions.append("turnLeft()")
    instructions.append("refuel()")
    instructions.append("turnRight()")

    if gainLayer:
        instructions.append("up()")

    for i in range(layer + 2):
        instructions.append("up()")

    # instructions.append("forward()")

    return instructions

def advance_layer():
    return ["up()"]

def paths_to_instructions(paths):

    print("Generating instructions...")

    refuelEveryLayer = False

    instructions = []

    itemCount = 64
    slot = 1

    for i in range(len(paths)):

        # print(paths[i])

        new_instructions, itemCount, slot = path_to_instructions(paths[i], i, items=itemCount, slot=slot)

        instructions.extend(new_instructions)

        if i != len(paths) - 1:
            # refuel every layer
            if refuelEveryLayer:
                instructions.extend(generate_refuel_instructions(1, i, gainLayer=True))   
            else:
                instructions.extend(advance_layer())

    # go to starting x, z
    go_back, direction = generate_instructions(paths[-1][-1], (-1, 0), 1)
    instructions.extend(go_back)
    instructions.extend(generate_direction_instruction(direction, 0))

    # go to starting y
    for i in range(len(paths) + 2):
        instructions.append("down()")


    # process placeDown() instructions
    # keep track of how many placeDown() instructions there are
    # if there are more than 64, then add a collectItems() instruction
    #TODO: implement

    return instructions

if __name__ == "__main__":

    path = [(0, 0), (1, 1), (2, 1), (3, 1), (3, 2), (2, 2), (1, 2), (1, 3), (2, 3), (3, 3), (0, 0)]
    path2 = [(0, 0), (1, 1), (2, 1), (3, 1), (3, 2), (2, 2), (1, 2), (1, 3), (2, 3), (3, 3), (0, 0)]

    path3 = [(0, 0), (1, 1), (2, 1), (3, 1), (3, 2), (2, 2), (1, 2), (0, 0), (1, 3), (2, 3), (3, 3), (0, 0)]

    # instructions = paths_to_instructions([path, path2])
    instructions = paths_to_instructions([path3])
    print(instructions)

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