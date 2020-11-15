# CambiumKit

## Cambium Router Attack Kit

CambiumKit is an attack kit for Cambium ePMP routers. Right now it just does a dictionary password attack using default credentials. Eventually it'll be able to exploit vulnerabilities and pop a shell on vulnerable routers.

### Usage
`$ python3 ck2.py [-fvth] <ip>
-f <file> - file containing list of IPs. One IP per line.
-v - verbose
-t <int> - number of threads for brute forcing
-h <ip> - ip of target`

### Todo
**Todo:**
* Integrate command line arguments
* Add support for automatically detecting and exploiting vulnerabilities in the Cambium ePMP software.
* Add loader to get a bind shell running on the target after successful exploitation.
