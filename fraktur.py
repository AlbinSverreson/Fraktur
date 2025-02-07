#!/usr/bin/env python3
# -*- coding utf-8 -*-
"""Fraktur: Render images into terminal-displayable pixel art"""

from argparse import ArgumentParser
import os
from PIL import Image

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


def get_common_colors(pixels, image, threshold):
    """Returns the two most common colors among a group of selected pixels
       in an image, with a threshold for what's considered transparent."""
    colors = {}
    for pixel in pixels:
        try:
            r, g, b = image.getpixel(pixel)
            if r+g+b > threshold:
                colors[(255,255,255)] = colors.get((255, 255, 255), 0) + 1
            else:
                colors[(r,g,b)] = colors.get((r,g,b), 0) + 1
        except IndexError:
            colors[(255,255,255)] = colors.get((255, 255, 255), 0) + 1

    color_list = list(colors.items())
    color_list.sort()
    color_list.reverse()
    fg = color_list[0][0]
    bg = color_list[1][0] if 1 < len(color_list) else (255, 255, 255)
    if fg == (255, 255, 255):
        fg = bg
        bg = (255, 255, 255)
    return (fg, bg)

def print_color_image(image, threshold):
    """Prints a multi colored image to the terminal with a threshold for
       what's considered transparent"""
    width, height = image.size
    for h in range(0, height, 2):
        out = ""
        for w in range(0, width, 2):
            active_pixels = [(w, h), (w+1, h), (w, h+1), (w+1, h+1)]
            fg, bg = get_common_colors(active_pixels, image, threshold)
            shape = ""
            for pixel in active_pixels:
                try:
                    r,g,b = image.getpixel(pixel)
                    if fg == (r,g,b) and fg != (255,255,255):
                        shape += "1" if sum(image.getpixel(pixel)) < threshold else "0"
                    else:
                        shape += "0"
                except IndexError:
                    shape += "0"

            if shape == "0000":
                out+=shapes[shape]
            else:
                out+=f"\033[38;2;{fg[0]};{fg[1]};{fg[2]}m"
                if bg!=(255,255,255):
                    out+=f"\033[48;2;{bg[0]};{bg[1]};{bg[2]}m"
                out+=shapes[shape]
                out+= "\033[0m"
        print(out)

def print_image(image, threshold):
    """Prints a single colored image to the terminal with a threshold for
       what's considered transparent"""
    width, height = image.size

    for h in range(0, height, 2):
        out = ""
        for w in range(0, width, 2):
            shape = ""
            active_pixels = [(w, h), (w+1, h), (w, h+1), (w+1, h+1)]
            for pixel in active_pixels:
                try:
                    shape += "1" if sum(image.getpixel(pixel)) < threshold else "0"
                except IndexError:
                    shape += "0"
            out += shapes[shape]
        print(out)

def main():
    """Parses command line arguments and calls the requested functions"""
    parser = ArgumentParser(
                    prog='Fraktur',
                    description='Generates terminal-displayable pixel art from images',
                    epilog='Beebee booboo')

    mode_title = parser.add_argument_group("Mode", "What mode to run Fraktur in")
    mode = mode_title.add_mutually_exclusive_group(required=True)
    mode.add_argument("--single", help="Single color mode", action="store_true")
    mode.add_argument("--multi", help="Multiple color mode", action="store_true")

    parser.add_argument("filename")
    parser.add_argument("-s", "--scale",
                        help="Scales image to specific width",
                        nargs="?",
                        const=os.get_terminal_size()[0],
                        type=int)
    parser.add_argument("-t", "--threshold",
                        help="Threshold for transparency",
                        default=600,
                        type=int)
    args = parser.parse_args()

    with Image.open(args.filename).convert("RGB") as image:
        if args.scale:
            width, height = image.size
            image = image.resize((args.scale,
                                 int((args.scale/width)*height)),
                                 resample=Image.NEAREST)
        width, height = image.size
        image = image.resize((width*2, height), resample=Image.NEAREST)
        if args.single:
            print_image(image, args.threshold)
        elif args.multi:
            print_color_image(image, args.threshold)

main()
