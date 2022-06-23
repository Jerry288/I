from genericpath import exists
import os
import shutil



programs_folder = "C:\Program Files"

#functions
def install():
    os.mkdir(f"{programs_folder}\isharp")

#check if program is already installed
if os.path.exists(f"{programs_folder}\isharp"):
    pass

