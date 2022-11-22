#!/usr/bin/env python

"""
Bagfile player utility to play ROS1 bagfiles inside a top level path
@Author: Mayank Joneja
@Date: 22-Nov-2022
"""

import pathlib
import subprocess
import shlex
import sys


def print_usage():
    """
    Print how to use the script
    """
    print("Usage: python3 bagfile_player.py <path_to_top_level_folder>")


def play_bagfiles(bagfile_list):
    """
    Plays bagfiles sequentially from a list of paths using `rosbag play` command

    :param bagfile_list: list of Pathlib paths for bagfiles

    """
    if len(bagfile_list) == 0:
        print("Bagfile list empty!")
        return

    for bag_file in bagfile_list:
        cmd = "rosbag play " + str(bag_file.resolve())
        print(f"Executing: {cmd}")
        cmd = shlex.split(cmd)
        subprocess.call(cmd)
        print("---")


def main():
    """
    Main method to play bags recursively inside path given from cmdline
    """

    num_args = len(sys.argv)
    if num_args != 2:
        print_usage()
        return

    bagfile_root_path = sys.argv[1]

    if pathlib.Path(bagfile_root_path).exists() is False:
        print("Bagfile root path doesn't exist!")
        print_usage()
        return

    print(f"Playing back bagfiles recursively inside: {bagfile_root_path}")
    bagfile_paths = pathlib.Path(bagfile_root_path).glob('**/*.bag')
    bagfile_list = list(bagfile_paths)

    if len(bagfile_list) == 0:
        print("No bagfiles found!")
        return

    resolved_path_list = [str(x.resolve()) for x in bagfile_list]

    print("===")
    print(f"Found bags: {resolved_path_list}")
    print("===")

    try:
        play_bagfiles(bagfile_list)
    except KeyboardInterrupt:
        print("\n\nExiting...")
        return


if __name__ == '__main__':
    main()
