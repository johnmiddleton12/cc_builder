-- every layer refuel, or every movement check fuel level,
-- and if it is too low to be able to return, refuel???

-- can just precompute everything and then just move and place, no need to check fuel level
-- if the path taken is already less than what's needed to return, then it's fine

-- Save the starting position
local start_x, start_y, start_z = 0, 0, 0 -- x is east(+)/west(-), y is up/down, z is north/south
local start_facing = 0 -- 0 = north, 1 = east, 2 = south, 3 = west

-- Save the position
local x, y, z = start_x, start_y, start_z
local facing = start_facing

-- The turtle will start facing the fuel chest - the program assumes infinite fuel in it
-- The item chest will be behind the turtle.
-- The turtle will start with an empty inventory.

function refuel()

    turtle.select(1)
    turtle.suck()

    local level = turtle.getFuelLevel()
    if new_level == "unlimited" then error("Turtle does not need fuel", 0) end

    local ok, err = turtle.refuel()
    if ok then
    local new_level = turtle.getFuelLevel()
    print(("Refuelled %d, current level is %d"):format(new_level - level, new_level))
    else
    printError(err)
    end

end

function collectItems()
    turtle.select(2)
    -- Collect items from the chest until turtle is full or chest is empty
    while turtle.suck() do
        -- Do nothing
    end
end

-- Safe movement functions
function forward()
    local success = turtle.forward()
    if success then
        if facing == 0 then
            z = z - 1
        elseif facing == 1 then
            x = x + 1
        elseif facing == 2 then
            z = z + 1
        elseif facing == 3 then
            x = x - 1
        end
    end
    return success
end

function back()
    local success = turtle.back()
    if success then
        if facing == 0 then
            z = z + 1
        elseif facing == 1 then
            x = x - 1
        elseif facing == 2 then
            z = z - 1
        elseif facing == 3 then
            x = x + 1
        end
    end
    return success
end

function up()
    local success = turtle.up()
    if success then
        y = y + 1
    end
    return success
end

function down()
    local success = turtle.down()
    if success then
        y = y - 1
    end
    return success
end

function turnLeft()
    local success = turtle.turnLeft()
    if success then
        facing = (facing - 1) % 4
    end
    return success
end

function turnRight()
    local success = turtle.turnRight()
    if success then
        facing = (facing + 1) % 4
    end
    return success
end

-- Safe place functions
function placeDown()
    local success = turtle.placeDown()
    if success then
        turtle.select(2)
    end
    return success
end

-- To print
-- 3d array of blocks
local blocks = {}
for i = 1, 3 do
    blocks[i] = {}
    for j = 1, 3 do
        blocks[i][j] = {}
        for k = 1, 3 do
            blocks[i][j][k] = 0
        end
    end
end

blocks[1][1][1] = 1
blocks[1][1][2] = 1
blocks[1][1][3] = 1
blocks[1][2][1] = 1
blocks[1][2][2] = 1
blocks[1][2][3] = 1
blocks[1][3][1] = 1
blocks[1][3][2] = 1
blocks[1][3][3] = 1

blocks[2][2][2] = 1
blocks[2][2][3] = 1
blocks[2][3][2] = 1
blocks[2][3][3] = 1

blocks[3][3][3] = 1

-- Step 1: Refuel

refuel()

-- Step 2: Turn to the item chest and collect items

turnLeft()
turnLeft()
collectItems()

-- Step 3: Return to the starting position

turnLeft()
turnLeft()

-- Step 4: Print the blocks

function returnToStart()
    -- Go to starting position

    -- Turn to the starting facing
    if facing == 1 then
        turnLeft()
    elseif facing == 2 then
        turnLeft()
        turnLeft()
    elseif facing == 3 then
        turnRight()
    end

    -- Now facing north, positive z
    -- correct z
    if z < start_z then
        while z < start_z do
            back()
        end
    elseif z > start_z then
        while z > start_z do
            forward()
        end
    end

    turnRight()

    -- Now facing east, positive x
    -- correct x
    if x < start_x then
        while x < start_x do
            forward()
        end
    elseif x > start_x then
        while x > start_x do
            back()
        end
    end

    turnLeft()

    -- Go down to 0
    while y > 0 do
        down()
    end

end

local layer = 1

while layer <= 3 do

    -- Move to the next layer from the starting position
    up()
    up()
    for i = 1, layer - 1 do
        up()
    end

    turnRight()
    forward()

    -- Print the layer
    for i = 1, 3 do
        for j = 1, 3 do
            if blocks[layer][i][j] == 1 then
                placeDown()
            end
            if j < 3 then
                forward()
            end
        end
        if i < 3 then
            if i % 2 == 0 then
                turnLeft()
                forward()
                turnLeft()
            else
                turnRight()
                forward()
                turnRight()
            end
        end
    end

    layer = layer + 1

    -- Go to starting position
    returnToStart()

end