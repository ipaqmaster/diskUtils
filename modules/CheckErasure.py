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
        self.parser = argparse.ArgumentParser(description="A script for checking disk erasure progress for easy resumption.")

        self.parser.add_argument(
                '-d',
                '--device',
                required=True,
                help='The target device or file.'
                )

        self.parser.add_argument(
                '-s',
                '--slices',
                default=100,
                type=int,
                help='How many slices we should check sequentially when looking for wiped space.'
                )


        self.args, self.unknownargs = self.parser.parse_known_args()

        self.deviceType = 'Device'

        if os.path.isfile(self.args.device):
            self.deviceType = 'File'


    def main(self):
        if self.args.device in [None,'']:
            print('Please specify a valid --device')
            self.parser.print_help()
            exit(1)

        self.deviceTotalBytes = diskUtils.getTotalBytes(self.args.device)
        self.deviceSliceSize  = int(self.deviceTotalBytes / self.args.slices)

        self.deviceBlockSize = diskUtils.getBlockSize(self.args.device)
        print('%s block size is %s' % (self.deviceType,str(self.deviceBlockSize)))

        # Add an extra slice if byte count not perfectly divisible by the desired slice count.
        #if not self.deviceTotalBytes % self.args.slices == 0:
        #    self.deviceTotalSlices = self.deviceTotalSlices + 1
        print("Checking %s slices of %s %s to determine if wiped." % (self.args.slices, self.deviceType, self.args.device))
        sliceProgress = 0
        while sliceProgress <= self.args.slices:
            targetOffset = self.deviceSliceSize * sliceProgress
            progressPercentage = round(sliceProgress / self.args.slices * 100)
            read = diskUtils.readFromOffset(self.args.device, targetOffset)
            if set(read) != {0}:
                print('[%s%%] Block not empty: %s' % (str(progressPercentage),targetOffset))

            print('[%s%%] [%s/%s] scanned.' % (str(progressPercentage),sliceProgress,self.args.slices), end='\r')
            sliceProgress = sliceProgress + 1

        print() # Final newline

if __name__ == "__main__":
    checkErasure = CheckErasure()
    checkErasure.main()
