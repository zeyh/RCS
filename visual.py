"""Visualization for Scratch Space Data
with matplotlib

ARGUMENTS -------------------------------------------------------------
A description of each argument that can or must be passed to this script
--dir ../../artspace_reports/daily/scratch

"""
from spaceMetrics import *
import matplotlib.pyplot as plt
import argparse

def plotUid(reader):
    '''
    plotUid plot the individual's usage throughout the dates
    ? lay different user on top of each other
    ? identify people 
    ? zoom in for shorten days
    '''
    result = reader.queryUidInfo()
       
    plt.plot(result.keys(), result.values())
    # plt.legend("Space", "Date")
    # plt.show()
    plt.savefig(reader.args.uid+".png")

def plotGroups(reader):
    '''
    plotGroups plot number of users whose usage is above some thresh
    '''
    result = reader.querySpaceAbove()
    plt.bar(result.keys(),listToFreq(result.values()))
    # plt.show()
    plt.savefig(str(reader.args.spaceThresh)+".png")
 
def listToFreq(values):
    '''
    listToFreq only count the length of each subarray
    
    :param: a 2d list
    :return: 1d list consisting of each inner list's length
    '''
    return [len(i) for i in values]
    
def addArgs():
    """
    addArgs get either input arguments, or default arguments
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


            
if __name__ == '__main__':
    reader = LogReader()
    args = addArgs()
    reader.setArgs(args)
    
    if args.uid != "":
        plotUid(reader) #save the plot here

    if args.spaceThresh != "":
        plotGroups(reader) #save the plot here

        

    print("\nFinished Plotting.")
    
    
    