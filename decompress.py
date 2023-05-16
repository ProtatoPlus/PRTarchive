import os
import binascii
import lz4.frame

archpath = input("Path to archive: ")
archive = open(archpath, "rb")
fstat = os.stat(archpath)

def b2h(bytesIn):
    return bytesIn.hex()

testsig = archive.read(7)
archive.seek(0)
if testsig != b'protato':
    print("Selected file is not a compatible archive")
else:
    archive.seek(7)
    archive.seek(archive.tell() + 4)
    fcount = b2h(archive.read(4))
    archive.seek(archive.tell() + 1)
    asize = b2h(archive.read(4))
    archive.seek(archive.tell() + 1)
    afirstfile = b2h(archive.read(4))
    print("Archive file count: " + str(int(fcount)) + "\nArchive size: " + str(int(asize, 16)) + " bytes \nOffset of first file: " + str(int(afirstfile)))
    
    print("i forgor")
    archive.seek(archive.tell() + int(afirstfile) + 4)
    fsize = archive.read(4)
    print(fsize)
    print(str(int(fsize, 16)))
