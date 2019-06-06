from selenium import webdriver
from bs4 import BeautifulSoup as soup
import re
import os


googleURL = 'https://www.google.com/maps/dir/'
driver = webdriver.PhantomJS()            

origins = ["IJsselstein"]
destinations = ["Bellingwedde","Vlagtwedde","Hoogezand-Sappemeer","Slochteren","Menterwolde",
"het Bildt","Franekeradeel","Menameradiel","Littenseradiel","Leeuwarderadeel","Rijnwaarden",
"Sudwest Fryslan","Schijndel", "Sint-Oedenrode", "Veghel"]

distances = [["" for x in range(len(destinations))] for y in range(len(origins))]
count = 0
cityIndex = 0
## If the file does not exist
if not os.path.isfile("distances16.csv"):
    # create it and write the headers
    file = open("distances16.csv", "w")
    file.write(";")
    file.write(";".join(destinations))
    file.write("\n")
    file.close()
# now we get down to it
for i in range(len(origins)):
    # open the file in appending mode
    file = open("distances16.csv", "a")
    # reset the count
    count = 0
    # get the origin city
    origin = origins[i]
    # write the origin city in the excel file
    file.write(origin + ";")
    # convert the origin city name to a URL friendly name
    originURL = "+".join(origin.split(" "))
    # for all cities
    for j in range(len(destinations)):
        # start with a high distance
        distance = 999999.0
        # find the destination
        destination = destinations[j]
        # make the destination name URL friendly
        destinationURL = "+".join(destination.split(" "))
        # Write the origin and destination pairing
        print(origin + " : " + destination)
        # if distance has not been found
        if not distances[i][j]:
            # if the origin = destination
            if origin == destination:
                # there is no distance
                distances[i][j] = "0"
                print("They're the same city")
                # write that to the file
                file.write(distances[i][j] + ";")
            # otherwise
            else:
                # compile the URL
                url = googleURL + originURL + "/" + destinationURL
                # access the webpage
                webpage = driver.get(url)
                # parse the webpage data
                data = soup(driver.page_source, "html.parser")
                # find all potential routes
                potential = data.find_all("div", {"class":"section-listbox"})
                # how many routes are there
                numberPotentials = len(potential)
                # if we could find a route
                if numberPotentials > 0:
                    # list all possible routes
                    possibles = potential[numberPotentials-1].find_all("div", recursive=False)
                    # find the minimum distance
                    for possibility in possibles:
                        dummyDistanceFull = re.search('(\d+,?\d+\skm)', possibility.text)
                        if dummyDistanceFull:
                            dummyDistanceNumber = re.search('(\d+,?\d+)', dummyDistanceFull.group(0))
                            if dummyDistanceNumber:
                                print(dummyDistanceNumber.group(0))
                                number = float(dummyDistanceNumber.group(0).replace(",","."))
                                if number < distance :
                                    distance = number
                    distance = (str(distance)).replace(".",",")
                    # if we didn't reach it
                    if (distance == "999999,0"):
                        distance = "unreachable"
                    distances[i][j] = distance
                    file.write(distance + ";")
                # otherwise we didn't find a route
                else:
                    distance = "unreachable"
                    file.write("unreachable;")
            count = count + 1
            print(str(distance) + " km")
            print("City index = " + str(j))
            print("Count = " + str(count))
        else:
            print("We didn't have to look for it!")
            file.write(distances[i][j] + ";")
    file.write("\n")
    file.close()

# at the end, close everything off properly
driver.quit()
logFile = "ghostdriver.log"
if os.path.isfile(logFile):
    os.remove(logFile)
