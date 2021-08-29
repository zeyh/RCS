"""Visualization for Scratch Space Data
with matplotlib

ARGUMENTS -------------------------------------------------------------
A description of each argument that can or must be passed to this script
--dir ../../artspace_reports/daily/scratch

(scratchVisual) [zhf3975@quser21 scratch]$ srun --account=a9009 --time=01:00:00 --partition=buyin --mem=1G --pty bash -l
(scratchVisual) [zhf3975@quser21 scratch]$ python visual.py --dir ../../artspace_reports/daily/scratch --spaceThresh 10000
"""

import matplotlib as mpl
mpl.use('Agg')
from spaceMetrics import *
import matplotlib.pyplot as plt
import argparse
from tqdm import tqdm

def genMonthlyBars(reader):
    start = reader.args.start
    end = reader.args.end
    # split the 1st of each month
    # handle the case - what if it's not there [not being collected]
    
def plotUid(reader):
    '''
    plot the individual's usage throughout the dates
    ? lay different user on top of each other
    ? zoom in for shorten days
    '''
    result = reader.queryUidInfo(True)
       
    plt.plot(result.keys(), result.values())
    print(result.keys())
    plt.vlines('060821',0,100,linestyles='dashed')
    plt.legend("Space", "Date")
    # plt.show()
    if reader.args.out == "":
        plt.savefig(reader.args.uid+".png")
    else:
        plt.savefig(reader.args.out+".png")

def plotGroups(reader):
    '''
    plotGroups plot number of users whose usage is above some thresh
    '''
    result = reader.querySpaceAbove(True)
    plt.bar(result.keys(),listToFreq(result.values()))
    # plt.show()
    if reader.args.out == "":
        plt.savefig(str(reader.args.spaceThresh)+".png")
    else:
        plt.savefig(reader.args.out+"_frequencies"+str(reader.args.spaceThresh)+".png")

def plotMultiUid(reader):
    reader.querySpaceAbove(False)
    userList = reader.rankedUserList
    for uid in tqdm(userList.keys()):
        reader.setUid(uid)
        result = reader.queryUidInfo(False)
        plt.plot(result.keys(), result.values(), label = uid)
    print("all users waited to be plotted: ", userList)
    plt.legend()
    # plt.show()
    # plt.set_size_inches(18.5, 10.5, forward=True)
    
    if reader.args.out == "":
        plt.savefig("multiple_"+changeDateFormat(reader.args.start)+"_"+changeDateFormat(reader.args.end)+".png", dpi=100)
    else:
        plt.savefig(reader.args.out+"_users"+str(reader.args.spaceThresh)+".png")
        
        
def changeDateFormat(date1):
    if("/" in date1):
        dateSplited = date1.split("/")
        date1 = ''.join(str(e) for e in dateSplited) 
    return date1
    
    
def listToFreq(values):
    '''
    only count the length of each subarray
    :param values: 2d list
    :return: 1d list - consisting of each inner list's length
    '''
    return [len(i) for i in values]

    
def addArgs():
    """
    get either input arguments, or default arguments
    fill args with values
    """
    parser = argparse.ArgumentParser(description='description tbd...')
    parser.add_argument('--dir', default='', help='input directory name')
    parser.add_argument('--prefix', default='b1042_scratch',
                        help='input files common prefix')
    parser.add_argument('--uid', default='',
                        help='user id')
    parser.add_argument('--spaceThresh', default='',
                        help='a number indicating the lowerbound of the space you d like to query')
    
    parser.add_argument('--start', default='02/01/21',
                        help='a starting date')
    parser.add_argument('--end', default='08/01/21',
                        help='an ending date')
    parser.add_argument('-o','--out', default='',
            help='define the name of output plotted figure')
    
    # parser.add_argument('--desc', default=True,type=str2bool, nargs='?',
    #                     help='output in a descending order?')
    parser.add_argument('-desc','--desc', action='store_true', help='output in a descending order')
    parser.add_argument('-mean', '--mean', action='store_true', help='print the mean')
    parser.add_argument('-std','--std', action='store_true',  help='print the standard deviation')
    parser.add_argument('-median', '--median', action='store_true',  help='print the median')
    
    
    args = parser.parse_args()
    if args.dir and args.dir[-1] != "/":
        args.dir += "/"
    if args.dir and args.dir[-1] != "/":
        args.dir += "/"
    if args.start == "":
        args.start = "01/01/2000"
    if args.end == "":
        args.end = formatDate(date.today())    
    return args


            
if __name__ == '__main__':
    reader = LogReader()
    args = addArgs()
    reader.setArgs(args)
    
    if args.uid != "":
        plotUid(reader) #save the plot here

    if args.spaceThresh != "":
        print("start ploting frequency bars")
        plotGroups(reader) #save the plot here
        
        print("start ploting multiple user IDs")
        plotMultiUid(reader) #plot multiple users

    print("\nFinished Plotting.")
    
    
    