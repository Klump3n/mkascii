#!/usr/bin/env python3
"""
Load a picture and turn it into ascii art with aalib.

"""
import sys
import argparse

from modules import window


def parse_args():
    """
    Parse command line arguments.

    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--image", help="image to use", required=True)
    args = parser.parse_args()
    return args

def main():
    """
    Load args and start displaying.

    """
    args = parse_args()
    img_path = args.image

    # start the curses app
    window.Window(img_path)

if __name__ == "__main__":
    main()
