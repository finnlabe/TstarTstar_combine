import os
import argparse

parser = argparse.ArgumentParser(description="TODO")
parser.add_argument("--doSR", action="store_true", help="Combine signal region?")
parser.add_argument("--doVR", action="store_true", help="Combine validation region?")
parser.add_argument("--doSpin12", action="store_true", help="Combine spin 1/2?")
parser.add_argument("--doSpin32", action="store_true", help="Combine spin 3/2?")
args = parser.parse_args()

years = ["UL16preVFP", "UL16postVFP", "UL17", "UL18"]

pass_along_arguments = ""
if args.doSR: pass_along_arguments += " --doSR"
if args.doVR: pass_along_arguments += " --doVR"
if args.doSpin12: pass_along_arguments += " --doSpin12"
if args.doSpin32: pass_along_arguments += " --doSpin32"

for year in years:
    
    print("Combining channels for {}.".format(year))
    
    os.chdir(year)
    os.system("python combine_channels.py" + pass_along_arguments)
    os.chdir("..")

# to the year combination here
os.system("python combine_years.py" + pass_along_arguments)