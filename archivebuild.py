import os
import binascii
import lz4.frame
import codecs
import base64

from cryptography.fernet import Fernet

files = {}
totalsize = 0

def buildArchiveObject(archname, curpos, archivefolder, b64enckey):
    global files
    global totalsize
    totalsize = 0
    if (b64enckey != None):
        crypto = True
    else:
        crypto = False

    print("Getting archive files")
    for filename in os.listdir(archivefolder):
        f = os.path.join(archivefolder, filename)
        if os.path.isfile(f):
            print("Adding file " + filename)
            fstat =  os.stat(f)
            tfile = open(f, "r+b")
            fdat = tfile.read(fstat.st_size)
            print("Compressing: " + filename)
            #ucdat = lz4.frame.compress(fdat)
            ucdat = fdat

            base64_bytes = base64.b64encode(ucdat)

            if (crypto):
                fernet = Fernet(b64enckey)
                print("Encrypting "+filename)
                finalBytes = fernet.encrypt(base64_bytes)
            else:
                finalBytes = base64_bytes

            files[f] = {"fnamelen": len(filename),"name": filename, "size": len(finalBytes), "data": finalBytes}
            totalsize += fstat.st_size
    archinfo = {"metadata": {"amt": len(files), "size": totalsize}, "data": files}
    print("Archive data built")
    archive = open(archname, "r+b")
    archive.seek(curpos)
    archive.write(archinfo['metadata']['amt'].to_bytes(4, byteorder = 'big'))
    archive.write(bytes(1))
    archive.write(archinfo['metadata']['size'].to_bytes(4, byteorder = 'big'))
    archive.write(bytes(1))
    archive.write((archive.tell() + 50).to_bytes(4, byteorder = 'big'))
    archive.seek(archive.tell() + 50 - 4)
    for fdat in archinfo['data']:
        archparent = archinfo['data'][fdat]
        archive.write(archparent['fnamelen'].to_bytes(4, byteorder='big'))
        archive.write(bytes(archparent['name'], 'utf-8'))
        archive.write(archparent['size'].to_bytes(4, byteorder = 'big'))
        cacheloc = archive.tell()
        archive.write(bytes(4))
        archive.write(archparent['data'])
        endloc = archive.tell()
        archive.seek(cacheloc)
        archive.write(endloc.to_bytes(4, 'big'))
        archive.seek(endloc)
        print("Wrote file: "+archparent['name']+" to archive")
