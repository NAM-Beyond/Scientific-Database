from bs4 import BeautifulSoup
import re
import requests
import time

Database_SecondaryList = []

for n in range(1, 100):
    print("Page :" + str(n))
    Database_URL = "https://scholar.google.com/scholar?start=" + str(n) + "0&q=%22schizophrenia%22+AND+(%22social+media%22OR+%22internet%22)+AND+(%22medical%22+OR+%22health%22)+AND+%22information%22&hl=fr&as_sdt=0,5&as_ylo=2006&as_yhi=2019"
    Database_Response = requests.get(Database_URL)
    Database_Page = BeautifulSoup(Database_Response.text, "html.parser")
    Database_PrimaryList = Database_Page.body.find_all("h3")
    for o in range(0, len(Database_PrimaryList)):
        if Database_PrimaryList[o].find("a") is None:
            continue
        else:
            Database_PrimaryList[o] = Database_PrimaryList[o].find("a")
            Database_SecondaryList.append(Database_PrimaryList[o].encode_contents().decode("UTF-8"))
    time.sleep(10)

for p in range(0, len(Database_SecondaryList)):
    Database_SecondaryList[p] = re.sub("<b>|</b>", "", Database_SecondaryList[p])
Database_SecondaryList.sort()

Database_file = open("Database.txt", "w+")
for p in range(0, len(Database_SecondaryList)):
    Database_file.write(str(Database_SecondaryList[p]) + "\n")

with open("pmc_result.txt", "r") as f:
    lines = f.readlines()
with open("pmc.txt", "w+") as f:
    for line in lines:
        if re.search("^\d+: ", line):
            f.write(re.sub("^\d+:  ", "", line))

with open("pubmed_result.txt", "r") as f:
    lines = f.readlines()
with open("pubmed.txt", "w+") as f:
    for line in lines:
        if re.search("TI  - ", line):
            f.write(re.sub("TI  - ", "", line))