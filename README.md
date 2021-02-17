# OnDemand

## Table of Contents

- [OnDemand](#ondemand)
  - [Table of Contents](#table-of-contents)
  - [Overview <a name = "overview"></a>](#overview-)
  - [Accessing OnDemand  <a name = "accessing_ondemand"></a>](#accessing-ondemand--)
    - [Browser Requirements](#browser-requirements)
  - [File Management  <a name = "file_management"></a>](#file-management--)
  - [Job Management <a name = "job_management"></a>](#job-management-)
  - [Accessing Command-line Shell <a name = "accessing_shell"></a>](#accessing-command-line-shell-)
  - [References](#references)
  
## Overview <a name = "overview"></a>

[OnDemand](https://qondemand.ci.northwestern.edu/) provides web access for the university's high performance computing(HPC) systems [QUEST](https://www.it.northwestern.edu/research/user-services/quest/index.html). By opening a web browser, OnDemand users have the oppotunity to:

- Manage files on Quest: upload, download, view, edit files and folders
- Compose and monitor jobs on Quest: create, edit, submit jobs with templates and script editors
- Access command-line shell

## Accessing OnDemand  <a name = "accessing_ondemand"></a>
Please make sure you have a valid Quest account, otherwise, computational time on the Quest cluster can be requested [here](https://www.it.northwestern.edu/secure/forms/research/allocation-request.html).
To connect to OnDemand, open a browser and visit https://qondemand.ci.northwestern.edu/. For unmanaged university computers or home computers, please make sure you are connected to a [Northwestern VPN](https://www.it.northwestern.edu/offcampus/). A popup window would ask for your username and password.\
**Hostname** : qondemand.ci.northwestern.edu\
**Username** : your Northwestern NetID (all lowercase letters)\
**Password** : your Northwestern NetID password

![Sign In Popup Window](images/signin.png)

### Browser Requirements

Google Chrome, Mozilla Firefox or Microsoft Edge. Please note that IE11 is not supported. 

Also, please make sure that your browser's pop-up blocker isn't preventing the sign in window from being displayed. To configure the pop-up settings in your browser, please visit [this page](https://kb.northwestern.edu/page.php?id=77182).


---

## File Management  <a name = "file_management"></a>

Once you've logged into OnDemand, by clicking "Files" &#8594; "Home Directory" in the main menu, you will be directed to the file explorer page. By default, you will be viewing your home directory on Quest: ```/home/<NetID>```. The home directory has 80GB of storage and is backed up nightly. Backups are kept for two weeks.

![File Explorer](images/file_navigation.png)
![all options](images/allOptions.png)

**Navigating**

The file explorer provides many options to go to your files and file management. You can navigate the folders similarly to a desktop GUI. Your **current directory** is located on the near top of the browsing window.

![Current Directory](images/current_directory.png)

**Switching folders:**

- Double click the folder name in the main section
- Single click the folder name in the left tree view
- Click the button named "GO TO..." and enter your folder directory
![go to](images/goto.png)

**Backtracting the path:**

- Single click the filename marked as blue in your current directory
- Double click the ".." which is the first entry on top of your files in the main section
![backtract](images/back.png)


**Uploading files**

Go to your destination folder, and then

- Drag files from your local file navigator to your OnDemand browser window
- Click "Upload" button located on the top-right corner of your browser and click "Choose Files" button to choose files in your local computer
![upload](images/upload.png)

**Downloading files**

- Click the file or multiselect with "control+click" the files first. Then click the "Download" button. Please note that if a folder is selected, it will be automatically zipped when downloading.
![download](images/download.png)

**Viewing or Editing files**

- OnDemand offers built-in file editors with syntax highlight which will automatically be opened in a new tab of your browser. To view or edit a file, select the file name you would like to view or edit, then click the "View" or "Edit" button to direct to the new tab.
![edit a file](images/edit.png)

- Then single click the refreshing icon located on the left of current directory to let new changes appearing on the screen
![refresh](images/refresh.png)

**Changing viewing options**

- To show all dotfiles such as *.bash_profile*, please select the checkbox named "Show Dotfiles" on the upper-right corner of the webpage.

- To view file owner or mode, please select the checkbox named "Show Owner/Mode" on the upper-right corner of the webpage.

![viewing options](images/viewing_options.png)

--- 

## Job Management <a name = "job_management"></a>

OnDemand provides graphical user interface so that you can create new Quest jobs as well as manage and view existing jobs all in one browser. To navigate to job management page, please select "Jobs" in dashboard's main menu, and choose either "Active Jobs" to view existing jobs or "Job Composer" to create a new job.

![Job Management](images/job_navigation.png)

TODO: 👇
**Creating a new Quest job**
Begin by creating a new job from an existing template, from any arbitrary path on the file system, or by copying a job you have already created through the Job Composer......

**Creating templates for job submissions**
[script.sh templates here](https://kb.northwestern.edu/page.php?id=69247)

**Editing a job**
Select a job and click xx to open the path in the file explorer so you can edit the job's files.....

**Submiting a job**
[Error message page](https://kb.northwestern.edu/page.php?id=91392)
Submit the job and monitor the progress from the "Job Composer" index page.

**Monitoring existing jobs**
[Job status page](https://kb.northwestern.edu/page.php?id=70711)

--- 

## Accessing Command-line Shell <a name = "accessing_shell"></a>

Without openning a terminal window, you can open  Quest S shell via OnDemand, which is equivalent to [connecting with an SSH terminal](https://kb.northwestern.edu/quest-login) with the following ways.

- Navigate to "Clusters"  &#8594; "_Quest S Shell Access" on the main menu in dashboard
![Shell](images/shell.png)
- Under Job Composer page (qondemand.ci.northwestern.edu/pun/sys/myjobs), click "Open Terminal" button. Please note that in the terminal page, your default working location would be your job script location.
- ![Shell in Jobs Page](images/shell_jobs.png)
- Under File Explorer page (qondemand.ci.northwestern.edu/pun/sys/files/fs/home/NetID/), click "Open in Terminal" button. Please note that in the terminal page, your default working location would be whatever is your current viewing directory on OnDemand.
![Shell in File Explorer](images/shell_fileExplorer.png)
  - To print your current working directory in shell, please type ```pwd```.
  - [Command line introduction](https://workshops.rcs.northwestern.edu/workshop/command_line/)
  - [Quest Quick Start](https://kb.northwestern.edu/quest-quickstart)
  - [Commonly used commands](https://kb.northwestern.edu/page.php?id=70710)

---



## References

https://openondemand.org/
https://www.osc.edu/resources/online_portals/ondemand
https://kb.northwestern.edu/page.php?id=70716
