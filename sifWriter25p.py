import numpy as np


def wrtiter(folderName, numberOfStrips, resistance):
    # Parameters
    peakVoltage = -25000
    voltageDifference = peakVoltage / (numberOfStrips + 1)

    resistances = (1 + np.random.normal(size=numberOfStrips + 1) / 100) * 150 * 10 ** 6  # 150 M Ohm resistors
    totalRes = 0
    for res in resistances:
        totalRes += res
    current = peakVoltage / totalRes

    # Open files
    sif = open('./' + folderName + '/case.sif', 'w')
    templateSif1 = open('./sif1.txt', 'r')
    templateSif2 = open('./sif2.txt', 'r')
    boundary = open('./' + folderName + '/mesh.boundary', 'r')

    # Copy template 1
    templateSifText = templateSif1.read()
    print("template 1 read")

    # Write the template
    sif.write(templateSifText)
    print("template 1 copied")

    # Calculate Potentials
    potential = []
    for x in range(numberOfStrips + 2):
        if x == 0 or x == numberOfStrips + 1 or not resistance:
            potential.append(x * voltageDifference)
        else:
            potential.append(current * resistances[x] + potential[x - 1])

    # Find number of boundaries
    lines = boundary.readlines()
    totalNumberOfBoundaries = 0
    for line in lines:
        split = line.split(" ")
        if int(split[1]) > totalNumberOfBoundaries:
            totalNumberOfBoundaries = int(split[1])

    # Body setup
    bodyCount = 1
    LArBody = "Body " + str(bodyCount) +\
              "\n  Target Bodies(1) = 1\n  Name = \"LAr\"\n  Equation = 1\n  Material = 3\nEnd\n\n"
    sif.write(LArBody)
    bodyCount += 1

    for y in range(1):
        boardBody = "Body " + str(y + bodyCount) + "\n  Target Bodies(1) = " + str(
            y + bodyCount) + "\n  Name = \"Body " + str(
            y + bodyCount) + "\"\n  Equation = 1\n  Material = 2\nEnd\n\n"
        sif.write(boardBody)
    bodyCount += 1
    for y in range(1):
        lightBody = "Body " + str(y + bodyCount) + "\n  Target Bodies(1) = " + str(
            y + bodyCount) + "\n  Name = \"Body " + str(
            y + bodyCount) + "\"\n  Equation = 1\n  Material = 4\nEnd\n\n"
        sif.write(lightBody)
    bodyCount += 1
    for x in range(numberOfStrips + 2):
        stripBody = "Body " + str(x + bodyCount) + "\n  Target Bodies(1) = " + str(
            x + bodyCount) + "\n  Name = \"Body " + str(
            x + bodyCount) + "\"\n  Equation = 1\n  Material = 1\nEnd\n\n"
        sif.write(stripBody)
    bodyCount += 2 * numberOfStrips + 4

    # Copy template 2
    templateSifText = templateSif2.read()
    print("template 2 read")

    # Write the template
    sif.write(templateSifText)
    print("template 2 copied")

    # Calculate the boundary numbers
    boundaryCount = 1
    boundaryIndex = totalNumberOfBoundaries

    boundaries2Side2, boundaries2Side3, boundaries2Side4 = [], [], []
    for y in range(numberOfStrips):
        boundaries2Side2.append(boundaryIndex - 6 - 2 * numberOfStrips - y)
        boundaries2Side3.append(boundaryIndex - 3 - numberOfStrips - y)
        boundaries2Side4.append(boundaryIndex - 1 - y)
    # Write BC
    BC0 = "Boundary Condition " + str(boundaryCount) + "\n  Target Boundaries(1) = " + \
          str(boundaryIndex - 4 - 2 * numberOfStrips) + "\n  Name = \"0\"\n  Potential = 0\nEnd\n\n"
    sif.write(BC0)
    boundaryCount += 1

    for boundary in range(numberOfStrips):
        BC = "Boundary Condition " + str(boundaryCount) + "\n  Target Boundaries(3) = " +\
             str(boundaries2Side2[boundary]) + " " + str(boundaries2Side3[boundary]) + " " + \
             str(boundaries2Side4[boundary]) + "\n  Name = \"" + str(
            potential[boundary + 1]) + "\"\n  Potential = " + \
             str(potential[boundary + 1]) + "\nEnd\n\n"
        sif.write(BC)
        boundaryCount += 1

    BCLast = "Boundary Condition " + str(boundaryCount) + "\n  Target Boundaries(1) = " +\
             str(boundaryIndex - 7 - 3 * numberOfStrips) + "\n  Name = \"" + str(potential[numberOfStrips + 1]) +\
             "\"\n  Potential = " + str(potential[numberOfStrips + 1]) + "\nEnd\n"
    sif.write(BCLast)
    
    boundaryCount += 1

    BCflux = "\nBoundary Condition " + str(boundaryCount) + \
             "\n  Target Boundaries(1) = 6\n  Name = \"flux\"\n  Periodic BC = 1\n  Electric Flux = 0\nEnd\n"
    sif.write(BCflux)

    print("BC written")

    # Close files
    sif.close()
    templateSif1.close()
    templateSif2.close()


def main(args):
    wrtiter(args.outFolderName, int(args.StripNumber), bool(args.Resistance))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Create ND LAr geometry and export mesh')
    parser.add_argument('outFolderName',
                        help='output folder name (default: LArBox)')
    parser.add_argument('StripNumber',
                        help='Set the number of strips')
    parser.add_argument('Resistance',
                        help='Boolean for accurate resistance')

    args = parser.parse_args()

    main(args)
