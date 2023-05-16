header:
7 bytes| signature | 70 72 6F 74 61 74 6F \n
4 bytes| padding \n \n

archive info: \n
4 bytes| file count \n
1 bytes| padding \n
4 bytes| total archive size \n
1 bytes| padding \n
4 bytes| offset to first file \n \n

file format: \n
4 bytes| file size \n
4 bytes| next file offset \n
ANY bytes| file (lz4) \n
