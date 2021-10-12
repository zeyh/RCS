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
import re

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
        tfGPUdata= []
        locator = soup.find(id="gpu").find_next("table")

        rows = locator.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            tfGPUdata.append([ele for ele in cols if ele]) # Get rid of empty values
        
        # rows = locator.findAll(lambda tag: tag.name=='tr')
        # in each row: Version, Python version, Compiler, Build tools, cuDNN,CUDA
        print(tfGPUdata, ver, pos)
        return filterVer(tfGPUdata, ver, pos)
    
    def scrapURL_cuDnn(self):
        #https://docs.nvidia.com/deeplearning/cudnn/support-matrix/index.html
        #given cuda version, find all cuDnn 
        localURL = "https://docs.nvidia.com/deeplearning/cudnn/support-matrix/index.html"
        page = requests.get(localURL)
        soup = BeautifulSoup(page.content, "html.parser")
        # a dictionary
        dict = {}
        # find all cudnn versions documented in  <a name="#cudnn-versions*" >
        a_tags = soup.findAll("a",{"name": re.compile(r'cudnn-versions.*')} ) #
        
        #extract the numbers and valid versions 
        cudnnVerSet = []
        cudnnQueryNames = []
        for i in a_tags:
            if(i.has_attr("name")):
                currStr = i["name"]
                if "cudnn-versions-" in currStr:
                    regFilter = re.compile(r'cudnn-versions-\d+')
                    cudnnQueryNames.append(i["name"])
                    if regFilter.match(currStr):
                        cudnnVerSet.append(currStr.partition("cudnn-versions-")[2])
        #arrange the list 
        cudnnVerSet = sorted(list(set(cudnnVerSet)), reverse=True)
        cudnnQueryNames = list(set(cudnnVerSet))
        
        #query all table within div with name attribute within cudnnQueryNames
        div_tags = soup.findAll("div",{"id": re.compile(r'cudnn-versions.*')} ) 
        tableContents = {}
        for i in div_tags:
            tableData = []
            table = i.find('table')
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                tableData.append([ele for ele in cols if ele]) # Get rid of empty values
            tableContents[i["id"].partition("cudnn-versions-")[2]] = tableData
        
        print(tableContents)
        # [['NVIDIA Ampere GPU architecture\nTuring\nVolta\nPascal\nMaxwell\nKepler', '11.41', 'SM 3.5 and later', 'r470'], 
        #  ['11.3', 'r465'], 
        #  ['11.2', 'r460, r455, r450'], 
        #  ['11.1', 'r450, r455'], 
        #  ['11.0', 'r450'], 
        #  ['Turing\nVolta\nXavier\nPascal\nMaxwell\nKepler', '10.2', 'SM 3.0 and later', 'r440']]
        
        
         
    def scrapURL_cuDnn_conda(self):
        #https://anaconda.org/conda-forge/cudnn/files
        #given cudnn, check if exists a version in conda-forge
        localURL = "https://anaconda.org/conda-forge/cudnn/files"
        page = requests.get(localURL)
        soup = BeautifulSoup(page.content, "html.parser")
        tableData = []
        table = soup.find('table')
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            tableData.append([ele for ele in cols if ele]) # Get rid of empty values
        
        #get only the third column
        versions_raw = [x[2] for x in tableData]
        versions = []
        verNums = []
        for ver in versions_raw:
            if "linux-" in ver:
                versions.append("linux-"+ver.split("linux-")[-1])
                m = re.search('.*cudnn-(.+?).tar.bz2.*', ver)
                if m:
                    found = m.group(1)
                    verNums.append(found)
        print(verNums)
        # ['8.0.5.39-h69e801d_3', '8.2.1.32-h86fa8c9_0', '8.2.1.32-h2c0ae14_0', '8.0.5.39-h69e801d_2', '8.2.0.53-h86fa8c9_0', '8.2.0.53-h2c0ae14_0', '8.1.0.77-h90431f1_0', '8.1.0.77-h469e712_0', '8.0.5.39-ha5ca753_1', '8.0.5.39-h01f27c4_1', '8.0.5.39-hc0a50b0_1', '8.0.5.39-ha5ca753_0', '8.0.5.39-h01f27c4_0', '8.0.5.39-hc0a50b0_0', '7.6.5.32-h01f27c4_1', '7.6.5.32-hc0a50b0_1', '7.6.5.32-h5754881_1', '7.6.5.32-ha8d7eb6_1', '7.6.5.32-hc0a50b0_0', '7.6.5.32-h01f27c4_0', '7.6.5.32-ha8d7eb6_0', '7.6.5.32-h5754881_0']

        
        
    
    def scrapURL_cudatoolkit(self):
        #https://docs.nvidia.com/deploy/cuda-compatibility/
        pass

    def scrapURL_cudatoolkit_conda(self):
        #https://anaconda.org/conda-forge/cudatoolkit/files
        #given cudatoolkit version, check if exists a version in conda-forge
        pass   
    
    def changeChannels(self):
        #besides conda-forge, also search for conda/nvidia/other channel
        pass
         
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
    print("------------------------")
    scrapper.scrapURL_cuDnn()
    print("------------------------")
    scrapper.scrapURL_cuDnn_conda()
    
    # some testing functions
    print("\nFinished Testing in scrapping.py")
    
    print("Done running scrapping.py")
    