import sys
import os
import shutil
import datetime
import re

# if data (files and directories) exist in the given directory "src" copy them to a backup directory and delete them from the given directory
# the name of the backup directory is structured as follows: YYYY-MM-DD_HH-MM-SS
# if the backup directory already exists, the name is extended by a number
# directories with name structure YYYY-MM-DD_HH-MM-SS or YYYY-MM-DD_HH-MM-SS_i are excluded from copy process
# the backup directory is created in the given directory
# sys.stdout is logged into a logfile, no output on console, data is appended to logfile
# therefore a custom print function is created

# Compile the regular expressions for directories to exclude with name structure YYYY-MM-DD_HH-MM-SS or YYYY-MM-DD_HH-MM-SS_i
exclude_pattern1 = re.compile(r'^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$')
exclude_pattern2 = re.compile(r'^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_i$')

#####################################################
# user input / configuration
#####################################################
# source directory is in the same directory as the script
src = "nameOfDirectory"
# name of logfile, gets stored in the same directroy as the script
logfile = "copyDataToBackup_logfile.log"

class LogWriter:
    def __init__(self, filename):
        self.filename = filename

    def write(self, message):
        with open(self.filename, 'a') as file:
            file.write(message)

    def flush(self):
        pass

def log_print(*args, **kwargs):
    output = ' '.join(map(str, args)) + '\n'
    sys.stdout.write(output)

def custom_print(*args, **kwargs):
    log_print(*args, **kwargs)

def copyData(src):
    # check if source directory exists
    if not os.path.exists(src):
        print("Source directory does not exist!")
        return None
    
    # check if data exists in source directory
    if not os.listdir(src):
        print("No data found in source directory!")
        return None
    # check if data exists in source directory excluding directories with name structure YYYY-MM-DD_HH-MM-SS or YYYY-MM-DD_HH-MM-SS_i
    if not [item for item in os.listdir(src) if not (exclude_pattern1.match(item) or exclude_pattern2.match(item))]:
        print("Only backup directories in source directory!")
        return None

    # get current date and time
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d_%H-%M-%S")

    # create backup directory
    backup_dir = src + '\\' + now_str
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    else:
        i = 1
        while os.path.exists(backup_dir + '_' + str(i)):
            i += 1
        backup_dir = backup_dir + '_' + str(i)
        os.makedirs(backup_dir)

    # copy data from source directory to backup directory including subdirectories and files with the same name
    # Loop through all files and directories in the source directory
    # after copy process delete data
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(backup_dir, item)

        if os.path.isdir(s) and (exclude_pattern1.match(item) or exclude_pattern2.match(item)):
            print("directory excluded from copy process: {}".format(s))
            continue

        # If item is a directory, copy it recursively
        # Otherwise, just copy the file
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
            print("Directory copied from {} to {}".format(s, d))
            shutil.rmtree(s)
            print("Source directory deleted: {}".format(s))
        else:
            shutil.copy2(s, d)
            print("File copied from {} to {}".format(s, d))
            os.remove(s)
            print("Source file deleted: {}".format(s))

    return backup_dir

# main function
if __name__ == "__main__":
    # prefix the actual directory for logfile
    logfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), logfile)
    log_writer = LogWriter(logfile)
    sys.stdout = log_writer

    print = custom_print

    print("##########################################################################################")
    print("Python script called at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # prefix the actual directory for source directory
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), src)
    print("using source directory: " + src)

    # copy data
    backup_dir = copyData(src)

    # print backup directory
    if backup_dir:
        print("\n*** Backup directory: " + backup_dir + " ***\n")
    else:
        print("\n*** No backup directory created! ***\n")
