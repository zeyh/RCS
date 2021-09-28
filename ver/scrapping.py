# -*- coding: utf-8 -*-

"""Scratch Space TBD
a command line tool for specific data queries e.g userid, space occupied
"""
# -----------------------------------------------------------------------------
# CODE REFERENCES:
# (for formatting) https://gist.github.com/jfrfonseca/5be28aef4e44d544f36e
# web scrapping: https://realpython.com/beautiful-soup-web-scraper-python/

# -----------------------------------------------------------------------------
'''
USAGE ----------------------------------------------------------------
# Install
conda install -c anaconda beautifulsoup4
pip install requests
conda activate verScrapping

# run
python scraping.py

DONE ----------------------------------------------------------------

TODO -------------------------------------------------------


OPTIONS ----------------------------------------------------------------
A description of each option that can be passed to this script
TBD
-h, --help            show this help message and exit
 

ARGUMENTS -------------------------------------------------------------
A description of each argument that can or must be passed to this script
TBD

ASSUMING URLs are fixed👇
links: 
https://pytorch.org/get-started/previous-versions/
https://www.tensorflow.org/install/source#gpu

ref: 
https://discuss.pytorch.org/t/is-there-a-table-which-shows-the-supported-cuda-version-for-every-pytorch-version/105846/2
https://discuss.pytorch.org/t/pytorch-with-cuda-11-compatibility/89254/2
https://pytorch.org/get-started/locally/
https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/rel_19-03.html

'''

import requests
from bs4 import BeautifulSoup

class Scrapper:
    def __init__(self, url):
        '''
        now has to be a specific url, not generic at all
        '''
        if url == "":
            self.url = "https://www.tensorflow.org/install/source#gpu"
        else:
            self.url = url
            
    def setURL(self, link):
        self.url = link
        
    def scrapURL_tf(self, ver, pos):
        '''
        return in the format [Version, Python version, Compiler, Build tools, cuDNN, CUDA]
        '''
        if ver == "":
            ver = "10.1"
        
        #try to convert string to float/int, o.w. 10.1, 6 by default
        try:
            ver = float(ver)
            pos = int(pos)
        except ValueError:
            print("WARNING: something wrong w/ customized input, now to the detault 10.1 and the 6th column")
            ver = 10.1
            pos = 6
            
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        # print(soup.prettify())
        
        # * for TF site --------------------------
        #Grab all div w/ class = "devsite-table-wrapper" and after h4 id = "gpu"
        # ref: table = soup.find(lambda tag: tag.name=='table' )  #and tag.has_attr('id') and tag['id']=="Table1"
        #Find the gpu table in the format of a list
        #TODO: find the gpu id under h4 linux
        tfGPUdata= []
        locator = soup.find(id="gpu").find_next("table")

        rows = locator.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            tfGPUdata.append([ele for ele in cols if ele]) # Get rid of empty values
        
        # rows = locator.findAll(lambda tag: tag.name=='tr')
        # in each row: Version, Python version, Compiler, Build tools, cuDNN,CUDA
        return filterVer(tfGPUdata, ver, pos)
        
        
def filterVer(data, ver, pos):
    '''
    return the filtered "data" where only the "ver" number in the "pos" column (start from 1) is greater
    param: data - 2d string list, column seperated by comma [["a","b"],["c","d"]...]
            ver - float
            pos - int (assume it's counted from 1)
    '''
    out = []
    for row in data:
        if row != []:
            if len(row) > pos:
                return "ERROR: please enter a valid column number"
            try:
                if float(row[pos-1]) >= ver:
                    out.append(row)
            except ValueError:
                print("ERROR: something wrong with the web scrapping, or the column number - the column value is not a float")
    return out
            
    

if __name__ == '__main__':
    scrapper = Scrapper("https://www.tensorflow.org/install/source#gpu")
    scrapper.scrapURL_tf("","")
    # some testing functions
    print("\nFinished Testing in scrapping.py")
    
    print("Done running scrapping.py")
    