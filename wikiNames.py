from bs4 import BeautifulSoup as soup
import requests as req

municipalities = []

url = "https://nl.wikipedia.org/wiki/Lijst_van_Nederlandse_gemeenten"
webpage = req.get(url, {"user-agent":"mozilla/5.0"})
content = webpage.content
data = soup(content, "html.parser")

sections = data.find_all("div", {"class":"editmode"})

for section in sections:
    entries = section.find_all("li")
    for entry in entries:
        municipalities.append(entry.text)

file = open("gemeenten.txt", "w")
for municipality in municipalities:
    file.write(municipality)
    file.write("\n")
file.close()
print(len(municipalities))
