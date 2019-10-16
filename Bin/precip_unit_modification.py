
#importing libraries and dependencies
import sys

#Declaring variables
precippath = sys.argv[1]
print "Opening file: " + precippath 
basinfile = open(precippath, 'r')
lines = basinfile.readlines()
header = lines[0] + lines[1] + lines[2] + lines[3] + lines[4] + "NODATA_value  -9999.00\n"
line = lines[0].split()
ncols = int(line[1])
line = lines[1].split()
nrows = int(line[1])

precipgrid = [[0 for x in xrange(ncols)] for y in xrange(nrows)]

for i in xrange(nrows):
    element = lines[i+5].split()
    for j in xrange(ncols):
        precipgrid[i][j] = float(element[j])/10.0

data=header
for x in range(0, nrows):
    for y in range(0, ncols):
        data = data + " " + "{0:.2f}".format(precipgrid[x][y])
    data = data + "\n"

with open(precippath, 'w') as txt:
    txt.write("{}\n".format(data))
print "Precipitation unit changed successfully."

