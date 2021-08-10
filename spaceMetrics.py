# -*- coding: utf-8 -*-

"""Scratch Space TBD
a command line tool for specific data queries e.g userid, space occupied, 
"""
# -----------------------------------------------------------------------------
# REFERENCES:
# (for formatting) https://gist.github.com/jfrfonseca/5be28aef4e44d544f36e
# -----------------------------------------------------------------------------
'''
USAGE ----------------------------------------------------------------

$ python spaceMetrics.py -h 
#find out all available arguments

$ python spaceMetrics.py --dir data --uid user1 -desc -median
# get all files within a folder named data, 
# find out the usage specifically for a netID of user1
# print the output in a descending order
# also print out the median


TODO ----------------------------------------------------------------
* Input user netid → return users space change through out the month 
* add duration flag → discrete dates to days (resolved in uidQuery)
* input space number → return user netid with space above + dates 
* input frequency number → return user netid with frequencies (resolved in spaceQuery)
! rank user based on their average usage
* input dates → return stats: mean, median 
? Add labels/legends to the plot
? Zoom in - query only specific begin & end dates / single day
? Single user - how many days above certain thresh
? add monthly bars - deletion days 

? ways for identifying 90 days perid [deletion policies]
? minimun occupied for x days [sort by that]

20th 28th  
file deleted on the 1st - 2nd [4th] (transition time)


OPTIONS ----------------------------------------------------------------
A description of each option that can be passed to this script
-h, --help            show this help message and exit
--dir DIR             input directory name
--prefix PREFIX       input files common prefix
--uid UID             user id
--spaceThresh SPACETHRESH
                      a number indicating the lowerbound of the space you d like to query
-desc, --desc         output in a descending order

* no longer necessary👇 ----------
-mean, --mean         print the mean
-std, --std           print the standard deviation
-median, --median     print the median
  
ARGUMENTS -------------------------------------------------------------
A description of each argument that can or must be passed to this script
--dir ../../artspace_reports/daily/scratch
'''

import argparse
import glob
import datetime
from multiprocessing import Pool
from collections import OrderedDict
import statistics
from itertools import chain

class LogReader:
    def __init__(self):
        """
        __init__ initialize the class with either input arguments, or default arguments
        fill self.args with values
        """
        parser = argparse.ArgumentParser(description='description tbd...')
        parser.add_argument('--dir', default='', help='input directory name')
        parser.add_argument('--prefix', default='b1042_scratch',
                            help='input files common prefix')
        parser.add_argument('--uid', default='',
                            help='user id')
        parser.add_argument('--spaceThresh', default='',
                            help='a number indicating the lowerbound of the space you d like to query')
        # parser.add_argument('--desc', default=True,type=str2bool, nargs='?',
        #                     help='output in a descending order?')
        parser.add_argument('-desc','--desc', action='store_true', help='output in a descending order')
        parser.add_argument('-mean', '--mean', action='store_true', help='print the mean')
        parser.add_argument('-std','--std', action='store_true',  help='print the standard deviation')
        parser.add_argument('-median', '--median', action='store_true',  help='print the median')
        
        self.args = parser.parse_args()
        if self.args.dir and self.args.dir[-1] != "/":
            self.args.dir += "/"
            

    def setArgs(self, arg):
        """
        setting keyword for query
        """
        self.args = arg
        
    def setUid(self, id):
        """
        setting keyword for query
        """
        self.args.uid = id
        
    def setSpaceThresh(self, thresh):
        """
        setting keyword for query
        """
        self.args.spaceThresh = thresh
    
    def printArgs(self):
        print(self.args)

    def queryUidInfo(self):
        """
        uidQuery get the occupacy data 
        Assuming that data is formatted as "uid allocationNumber spaceOccupied"
        Assuming that one uid would appear in each date once

        :param: uid a string of a user's netID
        :return: 2d list in the form of[[dates, space],]
        """
        print("Reading all files under", self.args.dir if self.args.dir else "current directory", ", starting with", self.args.prefix)
        print("Querying all info matching netID", self.args.uid)
        spaceList = [] # collect the output
        pool = Pool()
        params = [] # feed in one element from list of params for each thread
        for filename in glob.glob(self.args.dir + self.args.prefix + "*"):
            params.append(filename+" "+self.args.uid) 
        spaceList = pool.map(uidReadFiles, params)
        spaceList = list(filter(None, spaceList)) # filter out the None values in the list
        if spaceList != []:
            finalDict = sortDict(mergeDict(spaceList), self.args.desc) #return one single dictionary rather than a list
            # if printing:
            #     printStats(finalDict)
            #     printDuration(finalDict)
            return finalDict
        else:
            print("ERROR: netID not found. Please run with -h for help.")
            return 


        
        
    def querySpaceAbove(self):
        """
        spaceQuery return all uid above 

        :param: filenamewithId a string of "filename uid"
        :return: 1d list matching given uid and dates
        """
        try:
            print("Reading all files under", self.args.dir if self.args.dir else "current directory", ", starting with", self.args.prefix)
            print("Querying all user id with", self.args.spaceThresh, "GB occupied and above")
            threshold = float(self.args.spaceThresh)
            if threshold < 0:
                print("ERROR: please enter a valid space lowerbound number")
                return 
        except:
            print("ERROR: please enter a valid space lowerbound number")
            return
        spaceList = [] # collect the output
        pool = Pool()
        params = [] # feed in one element from list of params for each thread
        for filename in glob.glob(self.args.dir + self.args.prefix + "*"):
            params.append(filename+" "+str(self.args.spaceThresh))
        spaceList = pool.map(spaceReadFiles, params) 
        spaceList = list(filter(None, spaceList)) # filter out the None values in the list
        if spaceList != []:
            finalDict = sortDict(mergeDict(spaceList), self.args.desc) #return one single dictionary rather than a list
            userList = printUniqueUserCount(finalDict)
            print(userList)
            # self.rankUsers(userList)
            printDuration(finalDict)
            return finalDict
        else:
            print("ERROR: no user not found above this thresh. Please run with -h for help.")
            return 
        
    def rankUsers(self, users):
        '''
        TODO
        '''
        d = {}
        for u in users:
            self.setUid(u)
            uInfo = self.queryUidInfo(False)
            mean = findMean(uInfo)
            d[u] = mean
        print(sorted(d, key=d.get, reverse=True))
        
    def readLocalDir(self):
        """
        TESTING - NOT USED
        """
        print(self.args.dir + self.args.prefix)
        print(glob.glob(self.args.dir + self.args.prefix + "*"))
        for filename in glob.glob(self.args.dir + self.args.prefix + "*"):
            print(filename)
            date = filename[-6:]
            print(date)
        print("done reading logs")


# * =====================================
# * Parallelization functions 
# * =====================================

def uidReadFiles(filenamewithId):
    """
    uidReadFiles get all occupacy data given a user id

    :param: filenamewithId a string of "filename uid"
    :return: 1d list matching given uid and dates
    """
    filename, uid = filenamewithId.split()
    try: 
        currFile = open(filename, 'r')
    except FileNotFoundError:
        print("ERROR: Wrong file or file path. Please run with -h for help.")
        return
    
    tmplist = {getDate(filename):""}
    for line in currFile:
        currLine = line.strip().split()
        try:
            if currLine[0] == uid:
                tmplist[getDate(filename)] = float(currLine[2])
                currFile.close()
                return tmplist
        except IndexError:
            continue
    return None
        
def spaceReadFiles(filenameWithThresh):   
    """
    spaceReadFiles get all occupacy data given a threshold number

    :param: filenameWithThresh a string of "filename threshold"
    :return: 1d list of dates and uid matching and above given thresh
    """
    filename, thresh = filenameWithThresh.split()
    try: 
        currFile = open(filename, 'r')
    except FileNotFoundError:
        print("ERROR: Wrong file or file path. Please run with -h for help.")
        return
    
    tmplist = {getDate(filename):[]}
    for line in currFile:
        currLine = line.strip().split()
        try:
            if float(currLine[2]) >= float(thresh):
                tmplist[getDate(filename)].append(currLine[0])
        except (ValueError, IndexError): #ingore other commenting lines
            continue
    currFile.close()       
    return tmplist

# * =====================================
# * Helper functions
# * =====================================

def printUniqueUserCount(dict):
    '''
    find out unique values in a dict
    '''
    users = set(list(chain.from_iterable(dict.values())))
    num = len(users)
    print("Total:", num, "users")
    return users

def printStats(dict):
    '''
    associated with queryUidInfo()
    print the stats given a user id
    '''
    print("Mean: %.1f" % findMean(dict))
    print("Median:  %.1f" % findMedian(dict))
    print("Standard Deviation:  %.1f" % findStdev(dict))

def printDuration(dict):
    days = list(dict.keys())
    print("Begin from: ", formatDate(strToDate(days[0])), "to", formatDate(strToDate(days[-1])), "-", calDuration(days[0], days[-1]), "days")
    print(len(days), "days collected")
    
def mergeDict(myList):
    """
    mergeDict return a single dictionary rather than a list of dictionaries

    :param: dict - a list of dictionary  
    :return: one dictionary
    """
    result = {}
    for d in myList:
        result.update(d)
    return result

def sortDict(dict, descending):
    """
    sortDict return a sorted dictionary
    Assuming the dates are the last 6 digits in the format of MM/DD/YY
    Assuming all dates are before the year of 2000

    :param: dict - a dictionary to be sorted by date, isAscending - a bool indicating the sorting order
    :return: a sorted dictionary
    """
    compare = lambda key1, key2: key1 if (strToDate(key1) > strToDate(key2)) else key2
    result = OrderedDict(sorted(dict.items(), key=lambda x:strToDate(x[0]),reverse=descending)) # "key=..." equals to the compare function above
    return result

def findMean(dict):
    return statistics.mean(dict.values())

def findMedian(dict):
    return statistics.median(dict.values())

def findStdev(dict):
    return statistics.stdev(dict.values())

def strToDate(date1):
    return datetime.datetime(
        2000+int(date1[-2:]), int(date1[0:2]), int(date1[2:4]))

def formatDate(date):
    return date.strftime("%m/%d/%Y")

def str2bool(v):
    """
    NOT USED
    see https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def calDuration(date1, date2):
    """
    calDuration calcualte the duration between two input dates
    Assuming the dates are the last 6 digits in the format of MM/DD/YY
    Assuming all dates are before the year of 2000

    :param: two string of 6 digits in the format of MM/DD/YY
    :return: integer in days indicating duration between two input dates
    """
    duration = strToDate(date1)-strToDate(date2)
    return abs(duration.days) + 1 #calcuated both end dates #TODO
  
def getDate(filename):
    """
    getDate get the date from input filename
    Assuming the dates are the last 6 digits in the format of MM/DD/YY
    Assuming all dates are before the year of 2000

    :param: one string of filename consisting of the date
    :return: a string of date in the formate of MM/DD/YY
    """
    date1 = filename[-6:]
    return date1


if __name__ == '__main__':
    # * INIT ======================
    logReader = LogReader()
    
    if logReader.args.uid != "":
        result1 = logReader.queryUidInfo()
        print("Result: ", result1)
        if logReader.args.mean == True:
            print("Mean: %.1f" % findMean(result1))
        if logReader.args.median == True:
            print("Median:  %.1f" % findMedian(result1))
        if logReader.args.std == True:
            print("Standard Deviation:  %.1f" % findStdev(result1))
            
    if logReader.args.spaceThresh != "":
        result2 = logReader.querySpaceAbove()
        print("Result: ", result2)
    # * =============================
    
    # * TESTING ======================
    # calDuration("071221", "063021")
    # testDictionary = {'120722': 90.0, '050821': 100.0, '060821': 10.0}
    # sortDict(testDictionary, True)
    print("\nFinished Running.")
    # * =============================
    
    


