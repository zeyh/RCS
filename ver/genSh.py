# -*- coding: utf-8 -*-
'''
generating .sh based on the scrapped results
'''
'''
post-processing of scrapping.py
generating the corresponding sh file

ARGUMENTS:
--envName name of the conda environment (if none then will be randomly assigned)
--shName name of the .sh output file (if none then will be randomly assigned)


testing the sh file with 
$ sh run.sh

TODO:=====================================================
add README
bash script error handling: duplicated environment name?
test running on quest
same thing for the pyTorch Site
'''
#! /usr/bin/env python

import argparse
import string
import random
from pathlib import Path
from scrapping import Scrapper
from tqdm import tqdm
import inspect
import glob


TESTING_DIR = "results/"
class Logger:
    def __init__(self):
        parser = argparse.ArgumentParser(description='description tbd...')
        parser.add_argument('--shName', default="", help='Optional: specify an output name prefix (may include a potential directory)')
        parser.add_argument('--envName',default="", help='Optional: specify a conda environment name prefix')
        parser.add_argument('--envPath', default="",help='Optional: specify a conda create path')
        parser.add_argument('-ow','--ow', action='store_false',  help='Optional: name collision handling')
        parser.add_argument('--cudaVer', default="10.1", help='Optional: return this Cuda version and above (by default 10.1)')
        
        # TODO --printing/silent instuction differences between anaconda and tf  -ideal instructions
        # TODO  --warning cuda version mismatch conda toolkit - conda instruction requires install a cuda toolkit that out cuda version is incompatible
        
        self.args = parser.parse_args()
        # if self.args.shName != "" and '.sh' not in self.args.shName:
        #     self.args.shName += ".sh"
            
        self.scrapper = Scrapper("https://www.tensorflow.org/install/source#gpu") #TODO: torch
        
    def randomNameGen(self):
        '''
        generate random 4 chars
        '''
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(4)) 
    
    def printArgs(self):
        print("Current Arguments:" ,self.args)
     
    def getTFver(data):
        '''
        given a 2d data list, find the first column 
        or not really, just use the first column as it is
        '''
        pass
       
    def writeSH(self):
        TFdata = self.scrapper.scrapURL_tf(self.args.cudaVer, "6")
        
        #the case that there's no specification
        print("Now Creating "+str(len(TFdata))+" .sh files...")
        
        counter = 0
        for entry in tqdm(TFdata):
            counter += 1
            envPath = "--prefix "+self.args.envPath if self.args.envPath != "" else ""
            pyVer = entry[1].split("-")[-1] #TODO by default the highest python version, need for all versions'combination
            envName = self.args.envName+entry[0]+"-py-"+pyVer
            cudnnVer = entry[4]
            currFileName = TESTING_DIR+self.args.shName+entry[0]+"-py-"+pyVer+'.sh'
            
            if self.args.ow == False: 
                if Path(currFileName).is_file():
                    # print("WARNING: Output name already exists in the current directory, so the name will be added with _fourRandomCharacters.sh")
                    tmpName = currFileName.rpartition('.sh')[0]
                    currFileName = tmpName+"_"+self.randomNameGen()+".sh"
                    
            with open (currFileName, 'w') as rsh:
                script = f'''\
                #! /bin/bash
                echo "hello!"

                module purge all
                module load python-anaconda3
                conda create -n {envName} {envPath} -c conda-forge -c anaconda python={pyVer} cudnn={cudnnVer} --yes
                source activate {envName}
                pip3 install tensorflow

                echo "finished install!"
                ''' 
                # source(conda) activate #tensorflow==version 
                #! channels? 
                # # cudnn/cuda version conflict ? go up a version
                #? conda search for what anaconda has compares with tf and torch wants 
                # https://anaconda.org/anaconda/cudnn/files
                # https://anaconda.org/conda-forge/cudnn
                # conda serach closest matching version on anaconda compared with tf and torch
                # 1. does anaconda has the cuda version and cudnn library that tf has on its own page?
                # 2. anaconda doesnot have the right cuda and cudnn combination - what cuda version we have on our GPU
                # # cuda version 11.4 now
                
                
                script = inspect.cleandoc(script)
                rsh.write(script) 
                
            print(str(counter) + "/" + str(len(TFdata)) + " finished writing "+ currFileName)
            
        #write a install all script
        shNames = self.getAllLocalSh(TESTING_DIR, "yes | bash ")
        shNames = '\n'.join(map(str, shNames)).lstrip(' ')

        with open ("TEST-INSTALL.sh", 'w') as rsh_sum:
            script =  f'''\
                #! /bin/bash    
                {shNames}
                '''
            script = inspect.cleandoc(script)
            rsh_sum.write(script)
  
    def getAllLocalSh(self, dir, prefix):
        '''
        read all local file end with .sh
        attach a prefix to each filename
        return a list of prefix+filename
        '''
        names = []
        for filename in glob.glob(dir + "*.sh"): 
            names.append(prefix+filename)
        return names
     
    def crossSearch_cudnn(self):
        pass
    
if __name__ == '__main__':
    logger = Logger()
    logger.printArgs()
    logger.writeSH()
    
    print("Done running genSh.py")