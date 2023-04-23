# ComputerCraft Turtle Constructor

Generates a Lua script to build a structure given in a `.nbt` format using ComputerCraft turtles.

# Files

### nbt_to_json.py

Uses the `pythonnbt` library to convert an NBT schematic into a JSON format.

### json_to_arrays.py

Converts the JSON of the build into typed nested arrays to be used algorithmically

### arrays_to_path.py

Generates an optimized path for the turtle to take using BFS that takes into account refueling

### path_to_instructions.py

Creates a series of instructions from a path around a 2D surface that instruct the turtle

### instructions_to_lua.py

Writes the instructions along with necessary helper functions to a `.lua` file

### functions.lua

Functions that are shared with each Lua program