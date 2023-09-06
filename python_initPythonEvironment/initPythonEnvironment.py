import importlib
import subprocess
import os

version = "1.0.0"

def status_print(error, message):
    if error:
        print(os.path.basename(__file__) + ": [error]\t" + message)
    else:
        print(os.path.basename(__file__) + ": [status]\t" + message)

status_print(False, "Version: " + version)
status_print(False, "Checking for missing modules / dependencies . . .")

# List of required modules
required_modules = ['argparse', 'logging', 'paramiko']

# Check if all required modules are installed
missing_modules = []
for module in required_modules:
    try:
        importlib.import_module(module)
    except ImportError:
        missing_modules.append(module)

# Print missing modules
if missing_modules:
    status_print(True, f"The following modules are missing: {', '.join(missing_modules)}")
    status_print(False, "Starting installation of missing modules . . .")
    for module in missing_modules:
        subprocess.check_call(['pip', 'install', module])
    status_print(False, "Missing modules have been installed")
else:
    status_print(False, "All required modules are installed.")