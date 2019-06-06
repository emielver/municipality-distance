from bs4 import BeautifulSoup
htmlFile = open("ArbeidsmarkregiosGemeenten.htm", "r")
soup = BeautifulSoup(htmlFile, "html.parser")

regionBox = soup.find("div", {"class":"indeling-regios-overzicht"})

regions = regionBox.find_all("div", {"class":"toggle regio"}, recursive=False)

file = open("regios.csv", "w+")

file.write("Regio;Werkplein;;Gemeenten;\n")

for region in regions:
    regionName = region.h3.text
    regionWerkplein = region.div.dl.dd.text
    file.write(regionName)
    file.write(";")
    file.write(regionWerkplein)
    file.write(";;")
    rawMunicipalities = region.find_all("li")
    for municipality in rawMunicipalities:
        file.write(municipality.text)
        file.write(";")
    file.write("\n")
print("HTML file analysed")
file.close()
    
    
    
