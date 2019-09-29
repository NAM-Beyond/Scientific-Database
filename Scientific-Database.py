from selenium import webdriver
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

Database_PrimaryList = []

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
    element = WebDriverWait(browser, 240).until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    for i in browser.find_elements_by_tag_name("h3"):
        Database_PrimaryList.append(i.text)
    browser.find_element_by_xpath("//*[@id=\"gs_n\"]/center/table/tbody/tr/td[12]/a").click()
    time.sleep(10)
print(Database_PrimaryList)
with open("scholar.txt", "w+") as f:
    for i in Database_PrimaryList:
        if re.search("^\[[a-zA-Z]*\] ", i):
            f.write(re.sub("^\[[a-zA-Z]*\] ", "", i))
        else:
            f.write(i)

# PubMed Central results can be stored on a "Summary (Text)" file but need to be modified in order to have only the title on each line
#with open("pmc_result.txt", "r") as f:
#    lines = f.readlines()
#with open("pmc.txt", "w+") as f:
#    for line in lines:
#        if re.search("^\d+: ", line):
#            f.write(re.sub("^\d+:  ", "", line))

# PubMed results stored locally in a "Summary (Text)" format and treated in order to only display the title
#with open("pubmed_result.txt", "r") as f:
#    lines = f.readlines()
#with open("pubmed.txt", "w+") as f:
#    for line in lines:
#        if re.search("TI  - ", line):
#            f.write(re.sub("TI  - ", "", line))