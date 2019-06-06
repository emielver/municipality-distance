file = open("distances.csv", "r")
lines = file.readlines()
info = [["" for x in range(395)] for y in range(395)]
file.close()
# populate the data matrix
for i in range(len(lines)):
    parts = lines[i].split(";")
    for j in range(len(parts)):
        info[i][j] = parts[j]

# make the matrix symmetric
for i in range(len(lines)):
    for j in range(i, len(lines)):
        info[i][j] = info[j][i]

# write the matrix to a file
file = open("distancesNEW.csv", "w+")
for i in range(len(lines)):
    for j in range(len(lines)):
        file.write(info[i][j])
        file.write(";")
    file.write("\n")
file.close()
