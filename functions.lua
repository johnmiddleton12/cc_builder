function maxRefuel()
    while refuel() do
    end

    for i = 1, 16 do
        turtle.select(i)
        turtle.drop()
    end

end

function refuel()

    if turtle.getFuelLevel() == 100000 then return false end

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

    return ok

end

function collectItems()

    for i = 1, 16 do
        turtle.select(i)
        turtle.suck()
    end

    turtle.select(1)

end

-- Safe movement functions
function forward()
    local success = turtle.forward()
    return success
end

function back()
    local success = turtle.back()
    return success
end

function up()
    local success = turtle.up()
    return success
end

function down()
    local success = turtle.down()
    return success
end

function turnLeft()
    local success = turtle.turnLeft()
    return success
end

function turnRight()
    local success = turtle.turnRight()
    return success
end

-- Safe place functions
function placeDown()
    local success = turtle.placeDown()
    return success
end