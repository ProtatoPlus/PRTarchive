My own VERY bad and basic archive format

header\
7 bytes| signature | 70 72 6F 74 61 74 6F\
4 bytes| padding

archive info\
4 bytes| file count\
1 bytes| padding\
4 bytes| total archive size\
1 bytes| padding\
4 bytes| offset to first file

file format\
4 bytes| file name length\
ANY bytes| fname\
4 bytes| file size\
4 bytes| end of file\
ANY bytes| file (lz4)
