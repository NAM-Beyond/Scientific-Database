from selenium import webdriver
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

Database_PrimaryList = []
Database_SecondaryList = []
Database_TempList = []

# Preparing Brave as Chrome, because using chromedriver
options = webdriver.chrome.options.Options()
options.binary_location = "/usr/bin/brave-browser"
browser = webdriver.Chrome(chrome_options = options)

# Lots of time.sleeps in order to avoid being flaged as a robot by Google
browser.get("https://scholar.google.com")
time.sleep(3)
# Finding the input field for research and entering the desired keywords
browser.find_element_by_name("q").send_keys("\"schizophrenia\" AND (\"social media\" OR \"internet\") AND (\"medical\" OR \"health\") AND \"information\"")
time.sleep(3)
# Clicking the search button
browser.find_element_by_id("gs_hdr_tsb").click()
if browser.find_elements_by_xpath("//*[contains(@id,\"captcha\")]") != []: 
    element = WebDriverWait(browser, 240).until(EC.presence_of_element_located((By.ID, "gs_res_sb_yyc")))
time.sleep(3)
# Clicking on selecting a specific range of dates
browser.find_element_by_id("gs_res_sb_yyc").click()
time.sleep(3)
browser.find_element_by_id("gs_as_ylo").send_keys("2006")
time.sleep(3)
browser.find_element_by_xpath("//*[@id=\"gs_res_sb_yyf\"]/div[1]/div[2]/input").send_keys("2019")
time.sleep(3)
browser.find_element_by_xpath("//*[@id=\"gs_res_sb_yyf\"]/div[2]/button").click()
time.sleep(3)
for n in range(0, 99):
    if browser.find_elements_by_xpath("//*[contains(@id,\"captcha\")]") != []:
        element = WebDriverWait(browser, 240).until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    if  browser.find_elements_by_xpath("//*[contains(@id,\"captcha\")]") == [] and browser.find_element_by_xpath("//*[@id=\"gs_n\"]/center/table/tbody/tr/td[12]/a") == "" :
        break
    for i in browser.find_elements_by_tag_name("h3"):
        Database_PrimaryList.append(i.text)
    browser.find_element_by_xpath("//*[@id=\"gs_n\"]/center/table/tbody/tr/td[12]/a").click()
    time.sleep(10)
Database_PrimaryList.sort()
with open("scholar.txt", "w+") as f:
    for i in Database_PrimaryList:
        if re.search("^\[[a-zA-Z]*\] ", i):
            f.write(re.sub("^\[[a-zA-Z]*\] ", "", i) + "\n")
        else:
            f.write(i + "\n")

# PubMed Central results can be stored on a "Summary (Text)" file but need to be modified in order to have only the title on each line
with open("pmc_result.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        if re.search("^\d+: ", line):
            Database_TempList.append(re.sub("^\d+:  ", "", line))
    Database_TempList.sort()
with open("pmc.txt", "w+") as f:
    for i in Database_TempList:
        f.write(i)

# PubMed results stored locally in a "Summary (Text)" format and treated in order to only display the title
with open("pubmed_result.txt", "r") as g:
    lines = g.readlines()
    lines.sort()
with open("pubmed.txt", "w+") as g:
    for line in lines:
        if re.search("TI  - ", line):
            g.write(re.sub("TI  - ", "", line))

# Gathering all results in one main file, with remove of duplicates
def AddLines(textfile):
    with open(textfile, "r") as h:
        lines = h.readlines()
        for line in lines:
            templine = line.split()
            for i in range(0, len(templine)):
                templine[i] = templine[i].capitalize()
            line = ""
            for i in range(0, len(templine)):
                line += templine[i] + " "
            Database_SecondaryList.append(line)
AddLines("pubmed.txt")
AddLines("pmc.txt")
AddLines("scholar.txt")
Database_SecondaryList.sort()
n = 0
for i in range(0, len(Database_SecondaryList) - 1):
    if Database_SecondaryList[n] == Database_SecondaryList[n + 1]:
        del Database_SecondaryList[n + 1]
        n -= 1
    else:
        n += 1
with open("database.txt", "w+") as k:
    for i in Database_SecondaryList:
        k.write(i + "\n")
