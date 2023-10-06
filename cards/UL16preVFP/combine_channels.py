import os
import argparse

parser = argparse.ArgumentParser(description="TODO")
parser.add_argument("--doSR", action="store_true", help="Combine signal region?")
parser.add_argument("--doVR", action="store_true", help="Combine validation region?")
parser.add_argument("--doSpin12", action="store_true", help="Combine spin 1/2?")
parser.add_argument("--doSpin32", action="store_true", help="Combine spin 3/2?")
args = parser.parse_args()

masspoints = [700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2250, 2500, 2750, 3000]

for masspoint in masspoints:
    
    print("Combining {}".format(masspoint))
    
    if (args.doSR and args.doSpin12):
        os.system(
            "combineCards.py mu={0}_pt_ST_mu_SR.dat ele={0}_pt_ST_ele_SR.dat > {0}_pt_ST_total_SR.dat".format(masspoint)
        )
    
    if (args.doVR and args.doSpin12):
        os.system(
            "combineCards.py mu={0}_pt_ST_mu_VR.dat ele={0}_pt_ST_ele_SR.dat > {0}_pt_ST_total_VR.dat".format(masspoint)
        )
        
    if (args.doSR and args.doSpin32):
        os.system(
            "combineCards.py mu={0}_pt_ST_mu_SR_Spin32.dat ele={0}_pt_ST_ele_SR_Spin32.dat > {0}_pt_ST_total_SR_Spin32.dat".format(masspoint)
        )
    
    if (args.doVR and args.doSpin32):
        os.system(
            "combineCards.py mu={0}_pt_ST_mu_VR_Spin32.dat ele={0}_pt_ST_ele_SR_Spin32.dat > {0}_pt_ST_total_VR_Spin32.dat".format(masspoint)
        )