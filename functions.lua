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

    turtle.select(2)

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