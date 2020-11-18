#!/usr/bin/env python3
# Find Cambium ePMP routers using google dorking

from selenium import webdriver
import sys
import re

HEADLESS = False

def verifyTarget(string):
    # Check that string is a domain name or IP address
    match = re.fullmatch("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", string)
    if match != None:
        return True

    match = re.fullmatch("[a-zA-Z0-9\-]?\.?[a-zA-Z0-9\-]?\.?[a-zA-Z0-9\-]?\.?[a-zA-Z0-9\-]+\.{1}[a-zA-Z0-9\-]+", string)
    if match != None:
        return True
    
    # If we've made it to this point then the string isn't a domain or ip
    return False

##### Main ######
#######################
# Initialize selenium

if HEADLESS:
    browserOptions = webdriver.FirefoxOptions()
    browserOptions.set_headless()
    browser = webdriver.Firefox(browserOptions)
else:    
    browser = webdriver.Firefox()

# Search using the google dork
browser.get("https://www.google.com/search?source=hp&ei=cXa1X5nXIImWsAW1-7T4Aw&q=intitle%3AePMP+1000+intext%3ALog+In+-site%3A*.com+-site%3Acom.*&oq=intitle%3AePMP+1000+intext%3ALog+In+-site%3A*.com+-site%3Acom.*&gs_lcp=CgZwc3ktYWIQA1CPxxxYj8ccYK_JHGgAcAB4AIABAIgBAJIBAJgBAKABAqABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwjZ07e06oztAhUJC6wKHbU9DT8Q4dUDCAg&uact=5")

pageNumber = 1
while True:
    # Check for captcha
    if "/sorry" in browser.current_url:
        print("reCAPTCHA detected!")
        while True:
            print("To continue, solve the reCAPTCHA and then press 'c'")
            print("To exit, enter e")
            response = input("(e)xit / (c)ontinue: ").strip().lower()
            if response == "c":
                if "/sorry" in browser.current_url:
                    continue
                else:
                    break
            elif response == "e":
                sys.exit()

    # Grab the IPs/URLs from the results
    for result in browser.find_elements_by_tag_name("cite"):
        if len(result.text) > 0 and verifyTarget(result.text) == True:
            print(result.text)
    
    # Go to next page of results
    pageNumber += 1
    
    try:
        nextButton = browser.find_element_by_id("pnnext")
    except NoSuchElementException:
        print("End of results. Exiting...")
        sys.exit()

    nextPageLink = nextButton.get_attribute("href")
    browser.get(nextPageLink)
    #for result in browser.find_elements_by_id("pnnext"):
        #if result.get_attribute("aria-label") == "Page {pageNumber}":
            #print("clicking on", result, result.get_attribute("aria-label"))
            #result.click()
            #nextPageLink = result.get_attribute("href")
            #print(nextPageLink)
            #browser.get(nextPageLink)
            #break
        #else:
            #print("error! couldn't find next page link!")
            #sys.exit()
