import archivebuild

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
archCompress = archivebuild.buildArchiveObject(archivename, archive.tell(), input("Archive folder-> "))
archive.close()

#print("writing archive info object @ "+hex(archive.tell()))
