
# Scratch Space Data Querying


## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Example Running Commands](#running)
- [Example Results](#results)


## 🧐 About <a name = "about"></a>
Given user id, dates, and corresponding space occupied, query and visualize the data. Assuming that data is given in the following format:
**within a directory:**
    a list of documents with name "somePrefix_MMDDYY" (i.e. "b1000_scratch_073021") assuming that all dates are between 01/01/2000 and the current running date.
**within each document:**
```bat
user1 b1000 8
user3 b1000 22
user6 b1000 0
```
in the format of "userID allocationNumber spaceOccupied"

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

```bat
conda install -c conda-forge matplotlib
conda install tqdm
```
or
```bat
conda env create --file env.yml
```

## 🎈 Usage <a name="usage"></a>

#### 1. find all available options
```bat
-h 
```
#### 2. Query 1

**Option 1:** 
**Option 2:** 

####3. Query 2
**Option 1:** 
**Option 2:** 

## 🚀 Example Running Commands <a name = "running"></a>

1. Create an interactive job session
```bat
[xx@quser21 scratch]$ srun --account=XXXXX --time=00:20:00 --partition=buyin --mem=64G  --pty bash -l
```

2. Active conda environment
```bat
[xx@quser21 scratch]$ conda activate scratchVis
```

3. Run the script
```bat
(scratchVis) [xx@quser21 scratch]$ python visual.py --dir ../../artspace_reports/daily/scratch --spaceThresh 10000
```

## 🎆 Example Results <a name = "results"></a>

IMG1, 2,3