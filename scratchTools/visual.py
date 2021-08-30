"""Visualization for Scratch Space Data
with matplotlib

ARGUMENTS -------------------------------------------------------------
A description of each argument that can or must be passed to this script
--dir ../../artspace_reports/daily/scratch

(scratchVisual) [zhf3975@quser21 scratch]$ srun --account=a9009 --time=01:00:00 --partition=buyin --mem=1G --pty bash -l
(scratchVisual) [zhf3975@quser21 scratch]$ python visual.py --dir ../../artspace_reports/daily/scratch --spaceThresh 10000
"""

import os
import matplotlib as mpl
mpl.use('Agg')
from spaceMetrics import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import argparse
from tqdm import tqdm

def genMonthlyBars(reader):
    '''
    generate the 1st of every month of a given period, plus the start/ending dates
    :return: a list
    '''
    start = strToDate(reader.earliestDate)
    end = strToDate(reader.latestDate)
    #generate a list of 1st of each month between the beginning and ending dates
    monthly = [datetime.date(m//12, m%12+1, 1) for m in range(start.year*12+start.month-1, end.year*12+end.month)]
    if calDuration(reader.earliestDate, reader.latestDate) < 152: #some arbitrary number for displaying midMonth xstick
        midMonth =  [datetime.date(m//12, m%12+1, 15) for m in range(start.year*12+start.month-1, end.year*12+end.month)]
        monthly += midMonth
        
    #include the endpoints
    if(monthly[0] != start.date()):
        monthly.insert(0, start.date())
    if(monthly[-1] != end.date()):
        monthly.append(end.date())
    return monthly
    
def plotUid(reader):
    '''
    plot the individual's usage throughout the dates
    '''
    #get x and y values for plotting
    result = reader.queryUidInfo(True)
    x_values = [strToDate(d).date() for d in result.keys()]
    
    #set the x-axis date format
    fig, ax = plt.subplots()
    ax.grid(linestyle='dotted')
    ax.set_xticks(
        [x_values[0], x_values[-1]])
    formatter = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)
    
    # locator = mdates.MonthLocator() #Option1: only showing the monthly xstick
    # ax.xaxis.set_major_locator(locator)
    monthlyXstick = genMonthlyBars(reader) #Option2: include both ends for xstick
    ax.set_xticks(monthlyXstick)
    
    #plot values 
    plt.plot(x_values, result.values(), linestyle='--', marker='o', markersize=3)
    fig.autofmt_xdate()
    
    #add labels
    fig.set_size_inches(18.5, 10.5, forward=True)
    plt.suptitle(reader.args.uid+" Usage Report",fontsize=15)
    plt.title(formatDate(strToDate(reader.earliestDate))
              +" - "+formatDate(strToDate(reader.latestDate)),fontsize=12)
    plt.xlabel("Date")
    plt.ylabel("Space Occupied (GB)")
    
    #for easier debugging
    # plt.show()
    # plt.close()
    
    #saving options
    outputName = reader.args.uid+".png"
    if reader.args.out != "":
        outputName = reader.args.out+".png"
    if os.path.isfile(outputName):
        os.remove(outputName)
    plt.savefig(outputName)

def plotGroups(reader):
    '''
    plotGroups plot number of users whose usage is above some thresh
    '''
    #get the data for plotting
    result = reader.querySpaceAbove(True)
    x_values = [strToDate(d).date() for d in result.keys()]
    
    #set the x-axis date format
    fig, ax = plt.subplots()
    ax.grid(linestyle='dotted')
    formatter = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)
    
    monthlyXstick = genMonthlyBars(reader) 
    ax.set_xticks(monthlyXstick)
    
    #plot values 
    plt.bar(x_values,listToFreq(result.values()))
    fig.autofmt_xdate()
    
    #add labels
    fig.set_size_inches(18.5, 10.5, forward=True)
    plt.suptitle("Number of Users Above "+reader.args.spaceThresh+" GB Limit",fontsize=15)
    plt.title(formatDate(strToDate(reader.earliestDate))
              +" - "+formatDate(strToDate(reader.latestDate)),fontsize=12)
    plt.xlabel("Date")
    plt.ylabel("Number of Users Exceeding "+reader.args.spaceThresh+" GB Limit Each Day")
    
    #for easier debugging
    # plt.show()
    # plt.close()
    
    #saving options
    outputName = str(reader.args.spaceThresh)+".png"
    if reader.args.out != "":
        outputName = reader.args.out+"_userNum"+str(reader.args.spaceThresh)+".png"
    if os.path.isfile(outputName):
            os.remove(outputName)
    plt.savefig(outputName)

def plotMultiUid(reader):
    '''
    plot multiple users exceeding certain limit in one figure
    '''
    #get a list of uID
    reader.querySpaceAbove(False)
    userList = reader.rankedUserList
    print("all users waited to be plotted: ", userList)
    fig, ax = plt.subplots()

    #loop through every uid
    for uid in tqdm(userList.keys()):
        
        #get individual x and y values for plotting 
        reader.setUid(uid)
        result = reader.queryUidInfo(False)
        x_values = [strToDate(d).date() for d in result.keys()]
        
        #set the x-axis date format
        ax.grid(linestyle='dotted')
        ax.set_xticks(
            [x_values[0], x_values[-1]])
        formatter = mdates.DateFormatter("%Y-%m-%d")
        ax.xaxis.set_major_formatter(formatter)
        monthlyXstick = genMonthlyBars(reader)
        ax.set_xticks(monthlyXstick) 
        
        #plot values 
        plt.plot(x_values, result.values(), linestyle='--', marker='o', markersize=3, label = uid)
        fig.autofmt_xdate()
       

    
    #add labels & legends
    fig.set_size_inches(18.5, 10.5, forward=True)
    plt.suptitle("Usage Report: All Users Exceeding " + reader.args.spaceThresh+" GB ",fontsize=15)
    plt.title(formatDate(strToDate(reader.earliestDate))
              +" - "+formatDate(strToDate(reader.latestDate)),fontsize=12)
    plt.xlabel("Date")
    plt.ylabel("Space Occupied (GB)")
    lgd = plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')    

    #for easier debugging
    # plt.show()
    # plt.close()
    
    #saving options
    outputName = "multiUser_"+str(reader.args.spaceThresh)+".png"
    if reader.args.out != "":
        outputName = reader.args.out+"_individualUsage"+str(reader.args.spaceThresh)+".png"
    if os.path.isfile(outputName):
        os.remove(outputName)
    plt.savefig(outputName)
    
        
        
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
    
    
    