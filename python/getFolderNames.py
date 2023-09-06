import os
import datetime

# define the directory you want to search
directory_path = "path/to/directory/"

# define the file where you want to write the folder names
output_file = "folders.txt"
date_output_file = "folder_dates.txt"

# create a list to store folder names and creation dates
folder_names = []
folder_dates = []

# parse through the directory
for entry in os.scandir(directory_path):
    if entry.is_dir():
        folder_names.append(entry.name)
        creation_time = datetime.datetime.fromtimestamp(os.path.getctime(entry.path))
        folder_dates.append(creation_time.strftime("%d.%m.%Y"))

# write the folder names to a file
with open(output_file, "w") as f:
    for folder in folder_names:
        f.write(f"{folder}\n")

# write the creation dates to a separate file
with open(date_output_file, "w") as f:
    for date in folder_dates:
        f.write(f"{date}\n")
