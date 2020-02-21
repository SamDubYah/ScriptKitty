#! /usr/bin/python3

import subprocess, os
from datetime import datetime


#### [Defaults] ####
# Software dictionary to be returned
## Default set 'False', until software found
software = {
"Nmap": False,
"Masscan": False,
"Gobuster": False,
"Cewl": False
}

# port scan default
HOST="127.0.0.1"
PORT="1-1000"

# webscan defaults
WORDLIST_DIR="/usr/share/wordlists/SecLists/"

#### [END DEFAULTS] ####

def banner():
    print("TO BE REPLACED WITH BANNER")

def checkRoot():
    # waterwizard added for dev on mac
    if 'root' != subprocess.getoutput("whoami"):
        print("[!] Root required for port scans")
        exit(1)

# Checks current installed software
## to use in the audit, or to skip
def checkSoftware():
    # Check for available software
    for key in software:
        if subprocess.getstatusoutput("which " + key)[0]:
            software[key] = False
        else:
            software[key] = True

    # Prints results of found Software
    print("[*] Checking for available software")
    for key in software:
        if software[key] == True:
            print('\t', key, ": \tAvailable")
        else:
            print('\t', key, ": \tNot Found")

#### [Main Functions] ####


# initiate an Nmap Scan
def nmapScan(host, portRange):
    # Only runs if nmap is available
    if software["Nmap"]:
        #Creates new directory for nmap results
        print("[*] Creating working directory for Nmap scan.")
        makeNewDir("nmap")

        #Opens nmap on a new process
        proc = subprocess.call(["nmap -sC -sV "+ host+
        " -oA ./nmap/"+ getTimeFMT()+ "nmapResults"], shell=True)

# initiate a gobusterScan
def gobusterScan(host, wordlist):
    # Only run if Gobuster is available
    if software["Gobuster"]:
        #Creates new dir for gobuster results
        print("[*] Creating working directory for Gobuster scan.")
        makeNewDir("gobuster")

        #Opens gobuster on a new process
        subprocess.Popen("gobuster dir -u " + host + " -w " + wordlist +
        " -O ./gobuster/ " + getTimeFMT() + host + "_gobuster")


#### [Utility Functions] ####
def readData(fileLocation):
    print("helloworld")

def makeNewDir(folder):
    #Check if directory exists, if no create new directory
    dir = os.path.join(os.getcwd(), folder)
    if not os.path.exists(dir):
        os.mkdir(dir)
    else:
        print("[!]" + "\'" + folder +
        "\'" + "directory already exists, Skipping creation")

# gets current date/time to use as nameing schema
def getTimeFMT():
    return datetime.now().strftime("%Y-%b-%d_%H:%M_")


if __name__ == "__main__" :
    banner()
    #checkRoot()
    checkSoftware()


    #testing
    nmapScan(HOST, PORT)
