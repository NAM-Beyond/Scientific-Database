import requests
from bs4 import BeautifulSoup
import time

Database_SecondaryList = []

for n in range(0, 100):
    Database_URL = "https://scholar.google.com/scholar?start=" + str(n) + "0&q=%22schizophrenia%22+AND+(%22social+media%22OR+%22internet%22)+AND+(%22medical%22+OR+%22health%22)+AND+%22information%22&hl=fr&as_sdt=0,5&as_ylo=2006&as_yhi=2019"
    Database_Response = requests.get(Database_URL)
    Database_Page = BeautifulSoup(Database_Response.text, "html.parser")
    Database_PrimaryList = Database_Page.body.find_all("h3")
    print(len(Database_PrimaryList))
    for o in range (0, len(Database_PrimaryList)):
        Database_SecondaryList.append(Database_PrimaryList[o].a.encode_contents().decode("UTF-8"))
    time.sleep(1)

Database_file = open("Database.txt", "w+")
for p in range(0, len(Database_SecondaryList)):
    Database_file.write(str(Database_SecondaryList[p]) + "\n")
