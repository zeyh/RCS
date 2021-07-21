# -*- coding: utf-8 -*-

"""Scratch Space TBD
some description
"""
# -----------------------------------------------------------------------------
# REFERENCES:
# https://gist.github.com/jfrfonseca/5be28aef4e44d544f36e
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
* 1. Input user netid → return users space change through out the month 
2. input frequency number → return user netid with frequencies + dates
* 3. input space number → return user netid with space above + dates 
4. add duration flag → discrete dates to days
* 5. input dates → return stats: mean, median 

OPTIONS ----------------------------------------------------------------
A description of each option that can be passed to this script
ARGUMENTS -------------------------------------------------------------
A description of each argument that can or must be passed to this script
'''

import argparse
import glob
import datetime
from multiprocessing import Pool
from itertools import product
from collections import OrderedDict
import statistics

def addArguments():
    """
    addArguments description...

    :return: args...
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
    
    args = parser.parse_args()
    if args.dir and args.dir[-1] != "/":
        args.dir += "/"
    return args

def calDuration(date1, date2):
    """
    calDuration calcualte the duration between two input dates
    Assuming the dates are the last 6 digits in the format of MM/DD/YY
    Assuming all dates are before the year of 2000

    :param: two string of 6 digits in the format of MM/DD/YY
    :return: integer in days indicating duration between two input dates
    """
    duration = strToDate(date1)-strToDate(date2)
    return duration.days


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


def strToDate(date1):
    return datetime.datetime(
        2000+int(date1[-2:]), int(date1[0:2]), int(date1[2:4]))


def uidQuery(uid):
    """
    uidQuery get the occupacy data 
    Assuming that data is formatted as "uid allocationNumber spaceOccupied"
    Assuming that one uid would appear in each date once

    :param: uid a string of a user's netID
    :return: 2d list in the form of[[dates, space],]
    """
    spaceList = [] # collect the output
    pool = Pool()
    params = [] # feed in one element from list of params for each thread
    for filename in glob.glob(args.dir + args.prefix + "*"):
        params.append(filename+" "+uid) 
    spaceList = pool.map(uidReadFiles, params)
    spaceList = list(filter(None, spaceList)) # filter out the None values in the list
    if spaceList != []:
        return sortDict(mergeDict(spaceList), args.desc) #return one single dictionary rather than a list
    else:
        print("ERROR: netID not found")
        return 


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
        print("ERROR: Wrong file or file path")
        return
    
    tmplist = {getDate(filename):""}
    for line in currFile:
        currLine = line.strip().split()
        if currLine[0] == uid:
            tmplist[getDate(filename)] = float(currLine[2])
            currFile.close()
            return tmplist
    return None


def spaceQuery(threshold):
    """
    spaceQuery return all uid above 

    :param: filenamewithId a string of "filename uid"
    :return: 1d list matching given uid and dates
    """
    try:
        threshold = float(threshold)
    except:
        print("ERROR: please enter a valid space lowerbound number")
        return
    if threshold < 0:
        print("ERROR: please enter a valid space lowerbound number")
        return 
    spaceList = [] # collect the output
    pool = Pool()
    params = [] # feed in one element from list of params for each thread
    for filename in glob.glob(args.dir + args.prefix + "*"):
        params.append(filename+" "+str(threshold))
    spaceList = pool.map(spaceReadFiles, params) 
    spaceList = list(filter(None, spaceList)) # filter out the None values in the list
    if spaceList != []:
        return sortDict(mergeDict(spaceList), args.desc) #return one single dictionary rather than a list
    else:
        print("ERROR: no user not found above the thresh")
        return 
    
    
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
        print("ERROR: Wrong file or file path")
        return
    
    tmplist = {getDate(filename):[]}
    for line in currFile:
        currLine = line.strip().split()
        if float(currLine[2]) >= float(thresh):
            tmplist[getDate(filename)].append(currLine[0])
    currFile.close()       
    return tmplist


def findMean(dict):
    return statistics.mean(dict.values())


def findMedian(dict):
    return statistics.median(dict.values())


def findStdev(dict):
    return statistics.stdev(dict.values())


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


def readLogs():
    """
    TESTING - NOT USED
    """
    print(args.dir + args.prefix)
    print(glob.glob(args.dir + args.prefix + "*"))
    for filename in glob.glob(args.dir + args.prefix + "*"):
        print(filename)
        date = filename[-6:]
        print(date)
    print("done reading logs")



if __name__ == '__main__':
    global args
    args = addArguments()
    
    # TESTING ======================
    # readLogs()
    # calDuration("071221", "063021")
    testDictionary = {'120722': 90.0, '050821': 100.0, '060821': 10.0}
    sortDict(testDictionary, True)
    # ==============================
    
    if args.uid != "":
        result1 = uidQuery(args.uid)
        print("uid", result1)
        if args.mean == True:
            print("Average: %.1f" % findMean(result1))
        if args.median == True:
            print("Median:  %.1f" % findMedian(result1))
        if args.std == True:
            print("Standard Deviation:  %.1f" % findStdev(result1))
            
    if args.spaceThresh != "":
        result2 = spaceQuery(args.spaceThresh)
        print("a space limit number", result2)
    
    
    print("done")


