#!/usr/bin/env python3
# -*- coding utf-8 -*-

from argparse import ArgumentParser
from PIL import Image
import math

#shapecatcher <3
shapes = {
    "1111" : "█",
    "1010" : "▌",
    "0101" : "▐",
    "1100" : "▀",
    "0011" : "▄",
    "1001" : "▚",
    "0110" : "▞",
    "0010" : "▖",
    "0001" : "▗",
    "1000" : "▘",
    "0100" : "▝",
    "1011" : "▙",
    "1110" : "▛",
    "1101" : "▜",
    "0111" : "▟",
    "0000" : " "
}


def get_shape_part(r, g, b, threshold):
    if r+g+b < threshold:
        return "1"
    else:
        return "0"

def print_color_image(image, threshold):
    #image.save("output.png", "PNG")
    width, height = image.size
    for h in range(0, height, 2):
        out = ""
        for w in range(0, width, 2):
            red = green = blue = 255
            #red = green = blue = 0
            valid_pixels = 0
            active_pixels = [(w, h), (w+1, h), (w, h+1), (w+1, h+1)]
            shape = ""
            for pixels in active_pixels:
                try:
                    r, g, b = image.getpixel(pixels)
                    shape += get_shape_part(r, g, b, threshold)
                    red = int((red*r)/255)
                    green = int((green*g)/255)
                    blue = int((blue*b)/255)
                except IndexError:
                    shape += "0"
            if red+green+blue == 255:
                out += shapes["0000"]
            else:
                out += f"\033[38;2;{red};{green};{blue}m" + shapes[shape] + "\033[0m"
        print(out)

def print_image(image, threshold):
    width, height = image.size

    for h in range(0, height, 2):
        out = ""
        for w in range(0, width, 2):
            shape = ""
            active_pixels = [(w, h), (w+1, h), (w, h+1), (w+1, h+1)]
            for pixels in active_pixels:
                try:
                    shape += get_shape_part(*image.getpixel(pixels), threshold)
                except IndexError:
                    shape += "0"
            out += shapes[shape]
        print(out)

def main():
    parser = ArgumentParser(
                    prog='Fraktur',
                    description='Generates terminal-displayable pixel art from images',
                    epilog='Beebee booboo')
    mode_title = parser.add_argument_group("Mode", "What mode to run Fraktur in")
    mode = mode_title.add_mutually_exclusive_group(required=True)
    mode.add_argument("--single", help="Single color mode", action="store_true")
    mode.add_argument("--multi", help="Multiple color mode", action="store_true")

    parser.add_argument("filename")
    parser.add_argument("-w", "--widen", help="Strech the image to account for font size being slim", action="store_true")
    parser.add_argument("-s", "--scale", help="Scales image to specific width", type=int)
    parser.add_argument("-t", "--threshold", help="Threshold for transparency", default=382, type=int)
    #parser.add_argument("-b", "--background", help="Adds a background color", type=str)
    args = parser.parse_args()

    with Image.open(args.filename) as image:
        if args.scale:
            width, height = image.size
            image = image.resize((args.scale, int((args.scale/width)*height)), reducing_gap=3)
        if args.widen:
            width, height = image.size
            image = image.resize((width*2, height))
        if args.single:
            print_image(image, args.threshold)
        elif args.multi:
            print_color_image(image, args.threshold)
            pass
    

main()
