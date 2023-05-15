#!/usr/bin/python3
# Author: TheonlyTazz
# Documentation & improvements: R3GEN
# Corporate author: Feed The Beast Ltd
# Date: April 28th, 2023
# Github paste: https://gist.github.com/TheonlyTazz/c4bec488e5f3c83da1838d4fbe0d39a9
#
# Description:
# NBTPaletteChanger replaces all occurrences of the specified (input) term in the block palette of a Minecraft Java structure file (.nbt) with the new (output) term.
#
# Usage:
# NBTPaletteChanger.py [--exact]
#
# Arguments:
# --exact: If specified, the input term and output term of the block palette need to match each other.


import nbtlib
from nbtlib.tag import *
import os
import sys

def main():
    # Check for arguments
    exact_matching = False
    if len(sys.argv) >= 2:
        argument2 = sys.argv[1]
        if argument2 == '--exact':
            exact_matching = True
            print('\nExact matching mode only replaces materials whose fully match the string to find')

    input_folder = input('Input folder: \n')
    input_string = input('String to find: \n')
    output_string = input('String to replace to: \n')

    # Walk all files from the input folder
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith('.nbt'):
                nbt_file = nbtlib.load(os.path.join(root, filename), gzipped=True)

                # Get the palette compound NBT
                try:
                    palette = nbt_file['palette']
                except KeyError:
                    print(f"\nFilename> Unable to open \"{os.path.join(root, filename)}\" because it is corrupted")
                    continue

                printfilename = True

                # For each material change the block palette if applicable
                for material in palette:
                    name = ''
                    name = material.get('Name')

                    if exact_matching:
                        if input_string == name:
                            if printfilename:
                                print(f"\nFilename> {os.path.join(root, filename)}")
                                printfilename = False

                            material.update({'Name': String(output_string)})
                            print(f"    - Changed: {material.get('Name')}")
                    else:
                        if input_string in name:
                            if printfilename:
                                print(f"\nFilename> {os.path.join(root, filename)}")
                                printfilename = False

                            material.update({'Name': String(name.replace(input_string, output_string))})
                            print(f"    - Changed: {material.get('Name')}")

                nbt_file.save(os.path.join(root, filename))          
            
if __name__ == '__main__':
    main()