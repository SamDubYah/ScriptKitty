#! /usr/bin/python3

import subprocess, os, argparse, sys
from datetime import datetime


############# - TO DO LIST - ###############
# - Allow change in verbosity
# - Include logic to support hostfile/single host w/ nmap & masscan
# - Cleanup Function (Collect all data together, zip, delete all other traces)
# - Function to donwload wordlist if needed & desire
# - Parse arguments
# - Parse nmap results, change scan accordingly
# - Finish masscan module
###########################################

#### [Defaults] ####
# Software dictionary to be returned
## Default set 'False', until software found
software = {
"Nmap": False,
"Masscan": False,
"Gobuster": False,
"Cewl": False
}

# global defaults
VERBOSITY = True

# port scan default
HOST="127.0.0.1"
PORTS="1-1000"

# webscan defaults
## Change wordlist to be used for gobuster scan
WORDLIST_GOBUST="/usr/share/seclists/Discovery/Web-Content/common.txt"

#### [END DEFAULTS] ####

#### [CHECK FUNCTIONS] ####
def banner():
    print("TO BE REPLACED WITH BANNER")

def checkRoot():
    
    if 'root' != subprocess.getoutput("whoami"):
        print("[!] Root required for port scans")
        exit(1)

# Checks current installed software
## to use in the audit, or to skip
def checkSoftware():
    # Check for available software
    for softName in software:
        if subprocess.getstatusoutput("which " + softName)[0]:
            software[softName] = True
        else:
            software[softName] = False

    # Prints results of software
    print("[*] Checking for available software")
    for key in software:
        if software[key] == True:
            print('\t', key, ": \tAvailable")
        else:
            print('\t', key, ": \tNot Found")

# Check if wordlist is found
def checkWordlist():
    return true


#### [END CHECK FUNCTIONS] ####


#### [Main Functions] ####


# initiate an Nmap Scan
def nmapScan(host, portRange):
    # Only runs if nmap is available
    if software["Nmap"]:
        #Creates new directory for nmap results
        print("[*] Checking for Nmap working Directory.")
        makeNewDir("nmap")

        #Opens nmap on a new process
        print("[*] Running Nmap with default scripts, and version Enumeration")
        subprocess.call(["nmap -sC -sV -p" + portRange + " " + host +
        " -oA ./nmap/" + getTimeFMT() + host + "_nmapResults"], shell=True, stdout=subprocess.DEVNULL)

# initation a masscan
def masscanScan(hostFile, portRange):
    # Only runs if masscan is available
    if software["Masscan"]:
        #Creates new directory for masscan
        print("[*] Checking for Masscan working Directory.")
        makeNewDir("masscan")

        #Open masscan on a new process
        print("[*] Running masscan with the given file, sending open hosts to nmap for further enum")


        
# initiate a gobusterScan
def gobusterScan(host, wordlist):
    # Only run if Gobuster is available
    if software["Gobuster"]:
        #Creates new dir for gobuster results
        print("[*] Creating working directory for Gobuster scan.")
        makeNewDir("gobuster")

        #Opens gobuster on a new process
        print("[*] Running gobuster on " + host + " using wordlist:\n\t" 
                + wordlist)
        subprocess.call(["gobuster dir -u " + host + " -w " + wordlist +
            " -o ./gobuster/" + getTimeFMT() + host + "_gobusterResults"], shell=True, stdout=subprocess.DEVNULL)

#### [Utility Functions] ####

# get the arguments from user prints help if no arguments given
def parseArgs(argv=None):
    parser = argparse.ArgumentParser(prog='ScriptKitty', description="""A simpled python script to be run at the start of enumeration. 
            Useful during the initial enumeration to provide automation of scans and logging""")
    
    parser.add_argument("-t", "--target", nargs="?", help = "Single Target to initiate the enumeration")
    parser.add_argument("-p", "--portRange", nargs="?", default=PORTS, help = """Port range to be used during initial scans with nmap/masscan 
            Default Port Range (1-1000)""")

    parser.add_argument("-f", "--target_file", nargs="?", action="store_true", help = "File containing line seperated ip addresses")
    parser.add_argument("-wG","--gobust_wl", nargs="?", default=WORDLIST_GOBUST, help = "Wordlist to use for gobuster scan. Default wordlist {}".format(WORDLIST_GOBUST))
    parser.add_argument("--version", action="version", version="0.0.1", help=argparse.SUPPRESS)
    results = parser.parse_args(argv)
    
    if results.target == results.target_file == None:
        parser.print_help()
        sys.exit(0)

    return results


# check if directory exists, if not create it
def makeNewDir(folder):
    #Check if directory exists, if no create new directory
    dir = os.path.join(os.getcwd(), folder)
    if not os.path.exists(dir):
        print("[*] Creating working directory for " + folder)
        os.mkdir(dir)
    else:
        print("[!] " + folder + " directory already exists, Skipping creation")

# gets current date/time to use as nameing schema
def getTimeFMT():
    return datetime.now().strftime("%Y-%b-%d_%H:%M_")

# test case function to test functional of script
def testCase(): 
    #nmapScan(args.target, args.port)
    #gobusterScan(args.target, WORDLIST_GOBUST)

    print("Target: {}".format(args.target))
    print("Port Range: {}".format(args.portRange))
    print("Word List: {}".format(args.gobust_wl))
    print("Host file: {}".format(args.target_file))

if __name__ == "__main__" :
    args = parseArgs(sys.argv[1:])

    banner()
    checkRoot()
    checkSoftware()

    testCase() 

