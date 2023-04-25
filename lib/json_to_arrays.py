import json
from PIL import Image

def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

class BlockArray:
    def __init__(self, size_x, size_y, size_z):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.blocks = [[[Block("minecraft:air", 0) for z in range(size_z)] for x in range(size_x)] for y in range(size_y)]
        self.matrix = [[[0 for z in range(size_z)] for x in range(size_x)] for y in range(size_y)]
    
    def get_matrix(self):
        return self.matrix

    def get_block(self, x, y, z):
        return self.blocks[y][x][z]
    
    def set_block(self, x, y, z, block):
        self.blocks[y][x][z] = block
        if block.block_type != "air":
            self.matrix[y][x][z] = 1

    def pretty_print_layer(self, y):
        # concatenate all the images in the layer
        for z in range(self.size_z):
            for x in range(self.size_x):
                if x == 0:
                    row = self.get_block(x, y, z).get_image()
                else:
                    row = get_concat_h(row, self.get_block(x, y, z).get_image())
            if z == 0:
                layer = row
            else:
                layer = get_concat_v(layer, row)
        layer.show()

class Block:
    def __init__(self, block_type, block_data):
        self.block_type = block_type.replace("minecraft:", "")
        self.block_data = block_data

    def get_image(self):
        return Image.open("blockImages/" + "Images/" + self.block_type + ".png")

def json_to_arrays(json_path): 
    """This function converts a JSON file to a 3D array of blocks.

    The JSON file will have been converted form a Minecraft NBT file using the nbt_to_json.py script.
    That NBT file was created using the Litematica mod, converted from a schematic file on some kind.

    Parameters:
    json_path (str): The path to the JSON file.

    Returns:
    BlockArray: A 3D array of blocks.
    """

    ### Step 0 - Load the JSON file

    try:
        json_file = open(json_path, 'r')
    except IOError:
        print("Error: Could not open JSON file.")
        return None
    
    try:
        json_file = json.load(json_file)
    except ValueError:
        print("Error: Could not load JSON file.")
        return None
    
    ### Step 1 - Get the block palette

    block_palette = json_file["palette"]
    for i in range(len(block_palette)):
        if "Properties" in block_palette[i]:
            block_palette[i] = Block(block_palette[i]["Name"], block_palette[i]["Properties"])
        else:
            block_palette[i] = Block(block_palette[i]["Name"], 0)

    ### Step 2 - Get the size of the build and construct the 3D array of blocks
    
    [size_x, size_y, size_z] = json_file["size"]
    print("Size of build: " + str(size_x) + "x" + str(size_y) + "x" + str(size_z))

    print("Creating 3D array of blocks...")
    blocks = BlockArray(size_x, size_y, size_z)

    ### Step 3 - Fill the 3D array of blocks

    print("Filling 3D array of blocks...")
    for block in json_file["blocks"]:
        [x, y, z] = block["pos"]
        blocks.set_block(x, y, z, block_palette[block["state"]])

    return blocks

if __name__ == "__main__":

    blocks = json_to_arrays("buildVanilla.json")

    blocks.pretty_print_layer(8)