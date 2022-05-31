# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
##Imports
import hashlib
import os
import requests
from bs4 import BeautifulSoup 
import pandas as pd
import pprint
import subprocess
from PyPDF2 import PdfFileReader, PdfFileMerger


# %%
def getmd5sum(filename):

    md5_hash = hashlib.md5()
    a_file = open(filename, "rb")
    content = a_file.read()
    md5_hash.update(content)
    digest = md5_hash.hexdigest()
    return digest


# %%
def getdatafrommd5(md5):
    url ='https://www.libgen.is/book/index.php?md5=' +md5
    page = requests.get(url) 
    contents = page.content 
    soup = BeautifulSoup(contents, 'html.parser')
    a=soup.body.table.tbody
    #a = soup.find(id='bibtext')
    print(a)
    return #[title, author, publisher, series, year]


# %%
def getdatafrommd5v2(md5):
    url ='https://www.libgen.is/book/index.php?md5=' +md5
    print(url)
    r = requests.get(url)
    if(r.text == "No record with such MD5 hash has been found</body></html>"):
        return  [-1, -1, -1, -1, -1]
    df_list = pd.read_html(r.text) # this parses all the tables in webpages to a list
    table = df_list[0]
    title = table.loc[table[1] == 'Title:',2].tolist()[0]
    author = table.loc[table[1] == 'Author(s):',2].tolist()[0]
    publisher = table.loc[table[1] == 'Publisher:',2].tolist()[0]
    series = table.loc[table[1] == 'Series:',2].tolist()[0]
    year = table.loc[table[1] == 'Year:',2].tolist()[0]
    return  [title, author, publisher, series, year]


# %%
def setpdfmetadataOLD(file,title, author, publisher, series, year):
    newfname='new_'+file
    file_in = open(file, 'rb')
    pdf_reader = PdfFileReader(file_in)
    metadata = pdf_reader.getDocumentInfo()
    pprint.pprint(metadata)

    pdf_merger = PdfFileMerger()
    pdf_merger.append(file_in)
    pdf_merger.addMetadata({
        u'/Author': author,
        u'/Title': title,
        u'/Publisher':str(publisher),
        u'/Series':str(series),
        u'/Year':str(year)
    })
    file_out = open(newfname, 'wb')
    pdf_merger.write(file_out)
    file_in.close()
    file_out.close()
  #  with open(file) as f:
   #     f.fileinfo = {'title': title,'author':author,'publisher':publisher,'series':series,'year':year}



# %%
#For file
#get md5
#get metadata 
#set metadata


# %%
#exiftool -Title="This is the Title" -Author="Happy Man" -Year="1999" -Publisher="me" -SeriesName="wow" a.djvu
def setmetadata(fname,title, author, publisher, series, year):
    command = "exiftool -Title=\"{}\" -Author=\"{}\" -Year=\"{}\" -Publisher=\"{}\" -SeriesName=\"{}\" -overwrite_original \"{}\" ".format(title,author,year,publisher,series,fname)
    print("doing: "+command)
    subprocess.call(command, shell=True)


# %%
def setCalibremetadata(fname,title, author, publisher, series, year):
    command = f"ebook-meta \"{fname}\" -t \"{title}\" -a \"{author}\"  -p \"{publisher}\"  -d \"{year}\"  -s \"{series}\" "
    print("doing: "+command)
    subprocess.call(command, shell=True)


# %%
#def setdjvumetadata(fname,title, author, publisher, series, year):
    


# %%
def doIt(fname):
    md5 = getmd5sum(fname)
    [title, author, publisher, series, year] = getdatafrommd5v2(md5)
    if(title != -1):
        setCalibremetadata(fname,title, author, publisher, series, year)
        # move fname from input dir to output dir
        os.rename(fname, fname.replace('input', 'output'))
        
    else:
        print("nothing found for "+fname)


# %%
for file in os.listdir('input'):
    if not file.endswith(".pdf"):
        continue
    doIt('input/'+file)

