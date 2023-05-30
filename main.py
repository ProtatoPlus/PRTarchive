import archivebuild
import base64
import keygen

print("Protato archive tool")
archivename = input("name of archive: ") + ".prt"
encoding = "utf-8"
f = open(archivename, "x")
f.close()
archive = open(archivename, "r+b")
archive.seek(0)
print("Adding signature")
archive.write(bytes("protato", encoding))
archive.write(bytes(4))
if (input("Encryption (y/n) ") == "y"):
    keyder = keygen.getKeyFromStr(input('Key-> '))
    print("Your private key is: " + keyder)
    key = base64.b64encode(keyder.encode('ascii'))
else:
    key = None
archCompress = archivebuild.buildArchiveObject(archivename, archive.tell(), input("Archive folder-> "), key)
print("Operation Completed")
archive.close()

#print("writing archive info object @ "+hex(archive.tell()))
