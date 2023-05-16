import os
import binascii
import lz4.frame
import codecs

files = {}
encoding_list = []
totalsize = 0

def get_all_file_encodings(filename):
    global encoding_list
    encoding_list = []
    encodings = ('utf_8', 'utf_16', 'utf_16_le', 'utf_16_be', 
                 'utf_32', 'utf_32_be', 'utf_32_le',
                 'cp850' , 'cp437', 'cp852', 'cp1252', 'cp1250' , 'ascii',
                 'utf_8_sig', 'big5', 'big5hkscs', 'cp037', 'cp424', 'cp500',
                 'cp720', 'cp737', 'cp775', 'cp855', 'cp856', 'cp857',
                 'cp858', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864',
                 'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932',
                 'cp949', 'cp950', 'cp1006', 'cp1026', 'cp1140', 'cp1251',
                 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 
                 'cp1258', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
                 'euc_kr', 'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp',
                 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004',
                 'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr', 'latin_1',
                 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5',
                 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9',
                 'iso8859_10', 'iso8859_13', 'iso8859_14', 'iso8859_15',
                 'iso8859_16', 'johab', 'koi8_r', 'koi8_u', 'mac_cyrillic',
                 'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman',
                 'mac_turkish', 'ptcp154', 'shift_jis', 'shift_jis_2004',
                 'shift_jisx0213'
                 )  
    for e in encodings:
        try:
            fh = codecs.open(filename, 'r', encoding=e)
            fh.readlines()
        except UnicodeDecodeError:
            fh.close()
        except UnicodeError:
            fh.close()
        else:
            encoding_list.append([e])

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