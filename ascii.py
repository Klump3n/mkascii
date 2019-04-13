#!/usr/bin/env python3
"""
Load a picture and turn it into ascii art with aalib.

"""
import aalib
import curses
import argparse


def parse_args():
    """
    Parse command line arguments.

    """
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("-i", "--image", help="Use this image.", required=True)

    args = parser.parse_args()
    return args

def main():
    """
    Load args and start displaying.

    """
    args = parse_args()

if __name__ == "__main__":
    main()
