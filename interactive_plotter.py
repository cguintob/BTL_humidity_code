import sys

# This script continuously calls NEW_READER.py with continously updating data.
 
if (len(sys.argv) == 1):
    print("Use the following format: python interactive_plotter.py [datafile1].txt [datafile2].txt [datafile3].txt ...")
    print("Can also be used like this: python interactive_plotter.py path_to_datafiles/[filename]*")
    sys.exit(1)
else:
    while True:
        exec(open("NEW_READER.py").read())
