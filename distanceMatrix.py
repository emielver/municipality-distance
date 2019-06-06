from selenium import webdriver
from bs4 import BeautifulSoup as soup
import re
import os


googleURL = 'https://www.google.com/maps/dir/'
driver = webdriver.PhantomJS()            



file = open("gemeenten.txt","r")
cities = file.readlines()
for i in range(len(cities)):
    cities[i] = cities[i].strip()
file.close()
distances = [["" for x in range(len(cities))] for y in range(len(cities))]
count = 0
cityIndex = 0
## If the file does not exist
if not os.path.isfile("distances.csv"):
    # create it and write the headers
    file = open("distances.csv", "w")
    file.write(";")
    file.write(";".join(cities))
    file.write("\n")
    file.close()
else :
    file = open("distances.csv", "r")
    lineList = file.readlines()
    # fill the distance matrix for however far its already filled
    for i in range(1, len(lineList)):
        line = lineList[i].split(";")
        for j in range(1, len(line)):
            try :
                distances[i-1][j-1] = line[j]
                distances[j-1][i-1] = line[j]
            except IndexError:
                print("i = " + str(i))
                print("j = " + str(j))
    # check what the last city that was check is
    lastParts = lineList[len(lineList) - 1].split(";")
    city = lastParts[0]
    # if it exists
    if city:
        # find the index of the city and store it
        for i in range(len(cities)):
            if cities[i] == city:
                cityIndex = i+1;
                break
    # otherwise look in the line above
    else:
        lastParts = lineList[len(lineList) - 2].split(";")
        city = lastParts[0]
        # if the city exists
        if city:
            # find the index of the city and store it
            for i in range(len(cities)):
                if cities[i] == city:
                    cityIndex = i+1;
                    break
        # if you can't find anything, start at the first city
        else:
            cityIndex = 0
# now we get down to it
for i in range(cityIndex, len(cities)):
    # reset the webdriver every 50 origins
    if (i%50 == 1):
        driver = webdriver.PhantomJS()
    # open the file in appending mode
    file = open("distances.csv", "a")
    # reset the count
    count = 0
    # get the origin city
    origin = cities[i]
    # write the origin city in the excel file
    file.write(origin + ";")
    # convert the origin city name to a URL friendly name
    originURL = "+".join(origin.split(" "))
    # for all cities
    for j in range(len(cities)):
        # start with a high distance
        distance = 999999.0
        # find the destination
        destination = cities[j]
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
                    distances[j][i] = distance
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
    if (i%50 == 0) :
        driver.quit()
        logFile = "ghostdriver.log"
        if os.path.isfile(logFile):
            os.remove(logFile)

# at the end, close everything off properly
driver.quit()
logFile = "ghostdriver.log"
if os.path.isfile(logFile):
    os.remove(logFile)
