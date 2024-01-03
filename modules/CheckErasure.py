#!/usr/bin/env python
import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'libraries'))
#import modules.libraries.diskUtils
#import _scriptRoot.libraries.diskUtils
import diskUtils

class CheckErasure:
    def __init__(self):
        parser = argparse.ArgumentParser(description="A script for checking disk erasure progress for easy resumption.")

        parser.add_argument(
                '-d',
                '--device',
                help='The target device or file.'
                )

        parser.add_argument(
                '-s',
                '--slices',
                default=100,
                type=int,
                help='How many slices we should check sequentially when looking for wiped space.'
                )


        self.args, self.unknownargs = parser.parse_known_args()

    def main(self):
        if   self.args.device == None:
            print('Please specify a --device')

        print(diskUtils.getTotalBytes(self.args.device))

if __name__ == "__main__":
    checkErasure = CheckErasure()
    checkErasure.main()
