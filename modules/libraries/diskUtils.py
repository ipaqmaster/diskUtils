import os

def getTotalBytes(path):
    "Get the total bytes of a device or file."
    fd= os.open(path, os.O_RDONLY)
    try:
        return os.lseek(fd, 0, os.SEEK_END)
    finally:
        os.close(fd)
