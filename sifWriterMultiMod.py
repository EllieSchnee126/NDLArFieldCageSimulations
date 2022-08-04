import numpy as np


def writer(folderName, numberOfStrips, numberOfModules, resistance):
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

    for i in range(numberOfModules):
        for y in range(5):
            boardBody = "Body " + str(y + bodyCount) + "\n  Target Bodies(1) = " + str(
                y + bodyCount) + "\n  Name = \"Body " + str(
                y + bodyCount) + "\"\n  Equation = 1\n  Material = 2\nEnd\n\n"
            sif.write(boardBody)
        bodyCount += 5
        for y in range(4):
            lightBody = "Body " + str(y + bodyCount) + "\n  Target Bodies(1) = " + str(
                y + bodyCount) + "\n  Name = \"Body " + str(
                y + bodyCount) + "\"\n  Equation = 1\n  Material = 4\nEnd\n\n"
            sif.write(lightBody)
        bodyCount += 4
        for x in range(2 * numberOfStrips + 4):
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

    for i in range(numberOfModules):
        boundaries1Side1, boundaries1Side2, boundaries1Side3, boundaries1Side4 = [], [], [], []
        boundaries2Side1, boundaries2Side2, boundaries2Side3, boundaries2Side4 = [], [], [], []

        for y in range(numberOfStrips):
            boundaries1Side1.append(boundaryIndex - 18 - 8 * numberOfStrips + y)
            boundaries2Side1.append(boundaryIndex - 9 - 3 * numberOfStrips - y)
            boundaries1Side2.append(boundaryIndex - 16 - 7 * numberOfStrips + y)
            boundaries2Side2.append(boundaryIndex - 7 - 2 * numberOfStrips - y)
            boundaries1Side3.append(boundaryIndex - 13 - 6 * numberOfStrips + y)
            boundaries2Side3.append(boundaryIndex - 4 - numberOfStrips - y)
            boundaries1Side4.append(boundaryIndex - 10 - 5 * numberOfStrips + y)
            boundaries2Side4.append(boundaryIndex - 1 - y)

        # Write BC
        BC0 = "Boundary Condition " + str(boundaryCount) + "\n  Target Boundaries(2) = " +\
              str(boundaryIndex - 12 - 5 * numberOfStrips) + " " +\
              str(boundaryIndex - 5 - 2 * numberOfStrips) +\
              "\n  Name = \"0\"\n  Potential = 0\nEnd\n\n"
        sif.write(BC0)
        boundaryCount += 1

        for boundary in range(numberOfStrips):
            BC = "Boundary Condition " + str(boundaryCount) + "\n  Target Boundaries(8) = " + str(
                boundaries1Side1[boundary]) + \
                 " " + str(boundaries1Side2[boundary]) + " " + str(boundaries1Side3[boundary]) + " " + \
                 str(boundaries1Side4[boundary]) + " " + str(boundaries2Side1[boundary]) + \
                 " " + str(boundaries2Side2[boundary]) + " " + str(boundaries2Side3[boundary]) + " " + \
                 str(boundaries2Side4[boundary]) + " " + "\n  Name = \"" + str(
                potential[boundary + 1]) + "\"\n  Potential = " + \
                 str(potential[boundary + 1]) + "\nEnd\n\n"
            sif.write(BC)
            boundaryCount += 1

        BCLast = "Boundary Condition " + str(boundaryCount) + "\n  Target Boundaries(2) = " + str(
            boundaryIndex - 15 - 6 * numberOfStrips) + " " + str(
            boundaryIndex - 2 - numberOfStrips) + "\n  Name = \"" + str(
            potential[numberOfStrips + 1]) + "\"\n  Potential = " + str(potential[numberOfStrips + 1]) + "\nEnd\n"
        sif.write(BCLast)
        boundaryCount += 1
        boundaryIndex = boundaryIndex - 8 * numberOfStrips - 20

    print("BC written")

    # Close files
    sif.close()
    templateSif1.close()
    templateSif2.close()


def main(args):
    res = True
    if args.Resistance == "False":
        res = False
    writer(args.outFolderName, int(args.StripNumber), res)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Create ND LAr geometry and export mesh')
    parser.add_argument('outFolderName',
                        help='output folder name (default: LArBox)')
    parser.add_argument('StripNumber',
                        help='Set the number of strips')
    parser.add_argument('Resistance',
                        help='Boolean for accurate resistance')
    parser.add_argument('moduleNumber',
                        help='Set the number of modules')

    args = parser.parse_args()

    main(args)
