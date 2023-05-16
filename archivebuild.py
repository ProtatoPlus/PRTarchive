import os
import binascii
import lz4.frame
import codecs

files = {}
totalsize = 0

def buildArchiveObject(archname, curpos, archivefolder):
    global files
    global totalsize
    totalsize = 0
    print("Getting archive files")
    for filename in os.listdir(archivefolder):
        f = os.path.join(archivefolder, filename)
        if os.path.isfile(f):
            print("Adding file " + filename)
            fstat =  os.stat(f)
            tfile = open(f, "r+b")
            fdat = tfile.read(fstat.st_size)
            print("Compressing: " + filename)
            ucdat = lz4.frame.compress(fdat)

            files[f] = {"size": fstat.st_size, "data": ucdat}
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
    archive.seek(archive.tell() + 50)
    for fdat in archinfo['data']:
        archparent = archinfo['data'][fdat]
        archive.write(archparent['size'].to_bytes(4, byteorder = 'big'))
        archive.write((archive.tell() + 4 + archparent['size']).to_bytes(4, byteorder = 'big'))
        archive.write(archparent['data'])
