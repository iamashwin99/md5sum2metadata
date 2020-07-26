import hashlib
import os



def getmd5sum(filename):

    md5_hash = hashlib.md5()
    a_file = open(filename, "rb")
    content = a_file.read()
    md5_hash.update(content)
    digest = md5_hash.hexdigest()
    return digest

def getdatafrommd5(md5):


    return [title, author, publisher, series, year]


ans = getmd5sum('a.djvu')
print(ans)