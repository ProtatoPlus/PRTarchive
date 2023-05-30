import os
import binascii
import lz4.frame
import base64

from cryptography.fernet import Fernet

nfileoffset = 0
archpath = input("Path to archive: ")
archive = open(archpath, "rb")
fstat = os.stat(archpath)
outfolder = input("Output folder: ")
if (input("Encryption (y/n) ") == "y"):
    crypto = True
    key = base64.b64encode(input('Key-> ').encode('ascii'))
    fernet = Fernet(key)
else:
    crypto = False

if os.path.exists(outfolder) != True:
    print("Output folder does not exist!")
    exit()

def b2h(bytesIn):
    return bytesIn.hex()

testsig = archive.read(7)
archive.seek(0)
if testsig != b'protato':
    print("Selected file is not a compatible archive")
else:
    archive.seek(7)
    archive.seek(archive.tell() + 4)
    fcount = int.from_bytes(archive.read(4), "big")
    archive.seek(archive.tell() + 1)
    asize = b2h(archive.read(4))
    archive.seek(archive.tell() + 1)
    afirstfile = b2h(archive.read(4))
    print("Archive file count: " + str(fcount) + "\nArchive size: " + str(int(asize, 16)) + " bytes \nOffset of first file: " + str(int(afirstfile)))
    
    print("Begin archive read...")

    for i in range(fcount):
        if i == 0:
            pos = int(afirstfile)
            archive.seek(archive.tell() + pos - 1)
        else:
            pos = nfileoffset
            archive.seek(pos)
        nsize = archive.read(4)
        fname = str(archive.read(int.from_bytes(nsize, "big")), 'utf-8')
        fsize = int.from_bytes(archive.read(4), "big")
        print("FOUND FILE///" + "\n\nNAME: "+fname+"\nSIZE: "+str(fsize)+"\n\n")
        
        nfileoffset = int(b2h(archive.read(4)), 16)

        outputdat = archive.read(fsize)
        f = open(os.path.join(outfolder + fname), 'x')
        f.close()
        outfile = open(os.path.join(outfolder + fname), 'r+b')
        if (crypto):
            outputdat = fernet.decrypt(outputdat)
        b64_dec = base64.b64decode(outputdat)
        outfile.write(b64_dec)
        outfile.close()


