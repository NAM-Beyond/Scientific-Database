from bs4 import BeautifulSoup
import re

Database_SecondaryList = []

for n in range(1, 11):
    Database_Page = BeautifulSoup(open("Database_File" + str(n) + ".html"), "html.parser")
    Database_PrimaryList = Database_Page.body.find_all("h3")
    for o in range(0, len(Database_PrimaryList)):
        Database_PrimaryList[o] = Database_PrimaryList[o].find("a")
        Database_SecondaryList.append(Database_PrimaryList[o].encode_contents().decode("UTF-8"))

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