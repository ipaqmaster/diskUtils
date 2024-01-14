import fcntl
import os
import struct

# As per linux/include/uapi/linux/fs.h
# 0x80000000 is FS_XFLAG_HASATTR
ioctl = {
        "FS_XFLAG_EXTSZINHERIT": {
            "code": 0x00001000,
            "BLKSSZGET": { # Get block device sector size
                "code": 0x00000268,
                "decodeBuffer": b' ' * 4,
                "decodeFormat": 'i'
                },
            },
        "code": 0x80080000,
        "FS_XFLAG_HASATTR": {
            "BLKGETSIZE64": { #Get device size in bytes (u64 *arg)
                "code": 0x1272,
                "decodeBuffer": b' ' * 8,
                "decodeFormat": 'L' 
                }
            }
        }

def getTotalBytes(path):
    "Get the total bytes of a device or file."
    fd = os.open(path, os.O_RDONLY)
    try:
        return os.lseek(fd, 0, os.SEEK_END)
    finally:
        os.close(fd)

def readFromOffset(path,offset,quantity=1048576,debug=False):
    "Read content from a path starting from an offset."
    if debug: print('Reading %s worth of data from offset %s from path %s' % (quantity,offset,path))
    fd = os.open(path, os.O_RDONLY)
    try:
        # Seek to the offset
        os.lseek(fd, offset, os.SEEK_SET)
        # Read out quantity bytes from the offset
        read = os.read(fd, quantity)
    finally:
        os.close(fd)

    return(read)


def getBlockSize(path,debug=False): # Returns the blocksize querying with ioctl (Like fdisk and Co. would)
    "Query ioctl to try and read the blocksize of a device or use another method for files"
    if os.path.isfile(path):
        fileStat = os.stat(path)
        return(round(fileStat.st_size / fileStat.st_blocks))

    ioctlFlag  = "FS_XFLAG_EXTSZINHERIT"
    ioctlFunct = "BLKSSZGET" # Read device block size

    # 'Bitwise OR' the flag and function to get the desired full hex code to poke.
    fullCode = ioctl[ioctlFlag]['code'] | ioctl[ioctlFlag][ioctlFunct]['code']
    if debug: print("Poking ioctl %s (%s)" % (ioctlFunct,hex(fullCode)))

    with open(path) as dev:
        buf = fcntl.ioctl(dev.fileno(), fullCode, ioctl[ioctlFlag][ioctlFunct]['decodeBuffer'])

    bytes = struct.unpack(ioctl[ioctlFlag][ioctlFunct]['decodeFormat'],buf)[0]
    return(bytes)
