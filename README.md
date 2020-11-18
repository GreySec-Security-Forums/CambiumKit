# CambiumKit

## Cambium Router Attack Kit

CambiumKit is an attack kit for Cambium ePMP routers. Right now it just does a dictionary password attack using default credentials. Eventually it'll be able to exploit vulnerabilities and pop a shell on vulnerable routers.

### Usage
`$ python3 ck2.py [-fvth] <ip>
-f <file> - file containing list of IPs. One IP per line.
-v - verbose
-t <int> - number of threads for brute forcing
-h <ip> - ip of target`

### ckHunter
ckHunter is a (hacked-together) script to google dork for ePMP routers. The only thing I can guarantee is that it should work (probably). Just run like this: `python3 ckHunter.py`
If it encounters a reCAPTCHA (and isn't in headless mode), it'll prompt you to solve the captcha. If it is in headless mode, it just exits since you can't solve the captcha and it can't solve it.

### Todo
**Todo:**
* Integrate command line arguments
* Add support for automatically detecting and exploiting vulnerabilities in the Cambium ePMP software.
* Add loader to get a bind shell running on the target after successful exploitation.
