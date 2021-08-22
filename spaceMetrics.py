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
* shell & environmnet & code structure
* Input user netid → return users space change through out the month 
* add duration flag → discrete dates to days (resolved in uidQuery)
* input space number → return user netid with space above + dates 
* input frequency number → return user netid with frequencies (resolved in spaceQuery)
! rank user based on their average usage
* input dates → return stats: mean, median 
! zoom in - query only specific begin & end dates
! plot multiuser on a single img
? ❗️ add monthly bars 
? Add more labels/legends to the plot 
? Example commands on readME

===============================================
# ? more on error handling on input dates sanity check 
? unifying date vs datetime vs string input format
# ?Optimize Memory usage + running performance 

? Single user - how many days above certain thresh
? single date/ bars on deletion days 

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
../../projects/a9009/artspace_reports/daily/scratch
'''

import argparse
import glob
import datetime
from datetime import date
from multiprocessing import Pool
from collections import OrderedDict
import statistics
from itertools import chain

class LogReader:
    def __init__(self):
        """
        initialize the class with either input arguments, or default arguments
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
       
        parser.add_argument('-start','--start', default='',
                    help='a starting date in the format of MM/DD/YY')
        parser.add_argument('-end','--end', default='',
                            help='an ending date in the format of MM/DD/YY')
       
       
        # parser.add_argument('--desc', default=True,type=str2bool, nargs='?',
        #                     help='output in a descending order?')
        parser.add_argument('-desc','--desc', action='store_true', help='output in a descending order')
        parser.add_argument('-mean', '--mean', action='store_true', help='print the mean')
        parser.add_argument('-std','--std', action='store_true',  help='print the standard deviation')
        parser.add_argument('-median', '--median', action='store_true',  help='print the median')
        
        self.args = parser.parse_args()
        self.rankedUserList = {}
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

    def queryUidInfo(self, printing):
        """
        get the occupacy data of each uID
        Assuming that data is formatted as "uid allocationNumber spaceOccupied"
        Assuming that one uid would appear in each date once
        :param uid:  string - a user's netID
        :return: 2d list - in the form of[[dates, space],]
        """
        if self.args.start != "" and self.args.end != "":  # check input dates
            if not checkDate(self.args.start) or not checkDate(self.args.end):
                print("ERROR IN DATES 1")
                return
            # try:
            #     if not checkDate(self.args.start) or not checkDate(self.args.end):
            #         print("ERROR IN DATES 1")
            #         return
            # except:
            #     print("ERROR IN DATES 2 - ALL ERROR CATCHED")
            #     return
            
        if printing:
            print("Reading all files under", self.args.dir if self.args.dir else "current directory", ", starting with", self.args.prefix)
            print("Querying all info matching netID", self.args.uid)
        spaceList = [] # collect the output
        pool = Pool()
        params = [] # feed in one element from list of params for each thread
        for filename in glob.glob(self.args.dir + self.args.prefix + "*"): #TODO change params format for feeding in
            params.append(filename+" "+self.args.uid+" "+self.args.start+" "+self.args.end)
        spaceList = pool.map(uidReadFiles, params)
        spaceList = list(filter(None, spaceList)) # filter out the None values in the list
        if spaceList != []:
            finalDict = sortDict(mergeDict(spaceList), self.args.desc) #return one single dictionary rather than a list
            if printing:
                printStats(finalDict)
                printDuration(finalDict)
            return finalDict
        else:
            print("ERROR: netID not found. Please run with -h for help.")
            return 

        
    def querySpaceAbove(self):
        """
        return all uid above args.spaceThresh
        :param filenamewithId: string - in the form of "filename uid"
        :return: 1d list - matching given uid and dates
        """
        if self.args.start != "" and self.args.end != "":  # check input dates
            if not checkDate(self.args.start) or not checkDate(self.args.end):
                print("ERROR IN DATES 1")
                return
            # try:
            #     if not checkDate(self.args.start) or not checkDate(self.args.end):
            #         print("ERROR IN DATES 1")
            #         return
            # except:
            #     print("ERROR IN DATES 2 - ALL ERROR CATCHED")
            #     return
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
        for filename in glob.glob(self.args.dir + self.args.prefix + "*"): #TODO change params format for feeding in
            params.append(filename+" "+str(self.args.spaceThresh)+" "+self.args.start+" "+self.args.end)
        spaceList = pool.map(spaceReadFiles, params) 
        spaceList = list(filter(None, spaceList)) # filter out the None values in the list
        if spaceList != []:
            finalDict = sortDict(mergeDict(spaceList), self.args.desc) #return one single dictionary rather than a list
            userList = printUniqueUserCount(finalDict)
            ranked_result = self.rankUsers(userList)
            self.rankedUserList = ranked_result
            printDuration(finalDict)
            return finalDict
        else:
            print("ERROR: no user not found above this thresh. Please run with -h for help.")
            return 
        
    def rankUsers(self, users):
        '''
        rank a list of user based on their mean/std/median space
        :param users: 1d list - unsorted uids
        TODO:param comp: string - keyword for deciding the comparision method: mean, median, std
        :return: a dictionary of ranked user and their corresponding space value
        '''
        d = {}
        for u in users:
            self.setUid(u)
            uInfo = self.queryUidInfo(False)
            val = findMean(uInfo) #TODO easier change to std
            d[u] = round(val,2)
        result =  OrderedDict(d).items()
        print(">> Ranked", result)
        return dict(result)
        
    def readLocalDir(self):
        """
        TESTING - NOT USED
        """
        print(self.args.dir + self.args.prefix)
        print(glob.glob(self.args.dir + self.args.prefix + "*"))
        for filename in glob.glob(self.args.dir + self.args.prefix + "*"):
            print(filename)
            date1 = filename[-6:]
            print(date1)
        print("done reading logs")


# * =====================================
# * Parallelization functions 
# * =====================================

def uidReadFiles(filenamewithId):
    """
    get all occupacy data given a user id
    :param filenamewithId: string - in the form of "filename uid"
    :return: 1d list - matching given uid and dates
    """
    filename, uid, start, end = filenamewithId.split()
    try: 
        currFile = open(filename, 'r')
    except FileNotFoundError:
        print("ERROR: Wrong file or file path. Please run with -h for help.")
        return
    if not start or not end or not checkDateBoundary(getDate(filename), start, end):
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
    get all occupacy data given a threshold number
    :param filenameWithThresh: string - in the form of "filename threshold"
    :return: 1d list - dates and uid matching and above given thresh
    """
    filename, thresh, start, end = filenameWithThresh.split()
    try: 
        currFile = open(filename, 'r')
    except FileNotFoundError:
        print("ERROR: Wrong file or file path. Please run with -h for help.")
        return
    if not start or not end or not checkDateBoundary(getDate(filename), start, end):
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

def checkDate(date1):
    '''
    with input format MM/DD/YY
    TODO handling different formats, different format errors
    '''
    if date1 == "":
        print("ERROR: please enter a valid begin/end date in MM/DD/YY")
        return
    date1 = date1.split("/")
    if len(date1) != 3:
        print("ERROR: please enter a valid begin/end date in MM/DD/YY")
        return
    date_final = ""
    for i in date1:
        date_final += i
    return strToDate(date_final) if checkDateBoundary(date_final, "", "") else None
    
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
    associated with function queryUidInfo
    print the stats given a user id
    '''
    if(len(dict) > 1):
        print("Mean: %.1f" % findMean(dict))
        print("Median:  %.1f" % findMedian(dict))
        print("Standard Deviation:  %.1f" % findStdev(dict))
    else:
        print("Only contains one data point")
        
def printDuration(dict):
    days = list(dict.keys())
    print("Begin from: ", formatDate(strToDate(days[0])), "to", formatDate(strToDate(days[-1])), "-", calDuration(days[0], days[-1]), "days")
    print(len(days), "days collected")
    
def mergeDict(myList):
    """
    return a single dictionary rather than a list of dictionaries
    :param myList: 1d list - a list of dictionary  
    :return: one dictionary
    """
    result = {}
    for d in myList:
        result.update(d)
    return result

def sortDict(dict, descending):
    """
    sort the dictionary
    Assuming the dates are the last 6 digits in the format of MM/DD/YY
    Assuming all dates are before the year of 2000

    :param dict: dictionary - to be sorted by date, isAscending - a bool indicating the sorting order
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
    if "/" in date1:
        dateSplited = date1.split("/")
        date1 = ''.join(str(e) for e in dateSplited)
    return datetime.datetime(
        2000+int(date1[-2:]), int(date1[0:2]), int(date1[2:4]))

def formatDate(d):
    return d.strftime("%m/%d/%Y")

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
    calcualte the duration between two input dates
    Assuming the dates are the last 6 digits in the format of MM/DD/YY
    Assuming all dates are before the year of 2000

    :param date1/date2: string - of 6 digits in the format of MM/DD/YY
    :return: integer - in days indicating duration between two input dates
    """
    duration = strToDate(date1)-strToDate(date2)
    return abs(duration.days) + 1 #calcuated both end dates #TODO
  
def getDate(filename):
    """
    get the date from input filename
    Assuming the dates are the last 6 digits in the format of MM/DD/YY
    Assuming all dates are before the year of 2000

    :param filename: string - filename consisting of the date
    :return: string - date in the formate of MM/DD/YY
    """
    date1 = filename[-6:]
    return date1

def checkDateBoundary(d, lower, upper):
    '''
    check if its a valid date period for query
    '''
    if lower == "":
        lower = "012621"
    if upper == "":
        upper = date.today()
    earliest = strToDate(lower)
    if not isinstance(upper, datetime.date):
        upper = strToDate(upper).date()
    latest = upper
    if earliest.date() < strToDate(d).date() < latest:
        return True
    return False
    

if __name__ == '__main__':
    # * TESTING ======================
    # print(checkDateBoundary("05/20/21", "01/01/2021",  date.today()))
    # print(checkDateBoundary("05/20/21", "01/01/2021",  "11/01/2021"))
    # calDuration("071221", "063021")
    # testDictionary = {'120722': 90.0, '050821': 100.0, '060821': 10.0}
    # sortDict(testDictionary, True)
    print("\nFinished Testing.")
    # * =============================
    
    # * INIT ======================
    logReader = LogReader()
    
    if logReader.args.uid != "":
        result1 = logReader.queryUidInfo(True)
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
    

    
