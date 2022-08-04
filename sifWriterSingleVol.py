import numpy as np


def writer(folderName, numberOfStrips, resistance):
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

    # Body setup
    LArBody = "\nBody 1\n  Target Bodies(1) = 1\n  Name = \"Body 1\"\n  Equation = 1\n  Material = 3\nEnd\n\n"
    sif.write(LArBody)
    for y in range(1):
        boardBody = "Body " + str(y + 2) + "\n  Target Bodies(1) = " + str(y + 2) + "\n  Name = \"Body " + str(
            y + 2) + "\"\n  Equation = 1\n  Material = 2\nEnd\n\n"
        sif.write(boardBody)
    for x in range(numberOfStrips + 2):
        stripBody = "Body " + str(x + 3) + "\n  Target Bodies(1) = " + str(x + 3) + "\n  Name = \"Body " + str(
            x + 3) + "\"\n  Equation = 1\n  Material = 1\nEnd\n\n"
        sif.write(stripBody)

    # Copy template 2
    templateSifText = templateSif2.read()
    print("template 2 read")

    # Write the template
    sif.write(templateSifText)
    print("template 2 copied")

    # Calculate Potentials
    potential = []
    for x in range(numberOfStrips + 2):
        if x == 0 or x == numberOfStrips + 1 or not resistance:
            potential.append(x * voltageDifference)
        else:
            potential.append(current * resistances[x] + potential[x - 1])

    # Find number of boundaries
    lines = boundary.readlines()
    numberOfBoundaries = 0
    for line in lines:
        split = line.split(" ")
        if int(split[1]) > numberOfBoundaries:
            numberOfBoundaries = int(split[1])

    # Calculate the boundary numbers
    boundaryIndex = numberOfBoundaries - numberOfStrips + 1
    side1 = boundaryIndex - 3 * numberOfStrips
    side2 = boundaryIndex - 2 * numberOfStrips
    side3 = boundaryIndex - numberOfStrips
    side4 = boundaryIndex
    boundariesSide1, boundariesSide2, boundariesSide3, boundariesSide4 = [], [], [], []

    for y in range(numberOfStrips):
        boundariesSide1.append(side1 + y)
        boundariesSide2.append(side2 + y)
        boundariesSide3.append(side3 + y)
        boundariesSide4.append(side4 + y)

    # Write BC
    BC1 = "\nBoundary Condition 1\n  Target Boundaries(1) = 8\n  Name = \"0\"\n  Potential = 0\nEnd\n\n"
    sif.write(BC1)

    for boundary in range(numberOfStrips):
        BC = "Boundary Condition " + str(boundary + 2) + "\n  Target Boundaries(4) = " + str(boundariesSide1[boundary]) +\
             " " + str(boundariesSide2[boundary]) + " " + str(boundariesSide3[boundary]) + " " +\
             str(boundariesSide4[boundary]) + " " + "\n  Name = \"" + str(potential[boundary + 1]) + "\"\n  Potential = " +\
             str(potential[boundary + 1]) + "\nEnd\n\n"
        sif.write(BC)

    BCLast = "Boundary Condition " + str(numberOfStrips + 2) + "\n  Target Boundaries(1) = " + str(side1 - 3) +\
             "\n  Name = \"" + str(potential[numberOfStrips + 1]) + "\"\n  Potential = " +\
             str(potential[numberOfStrips + 1]) + "\nEnd\n"
    sif.write(BCLast)

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

    args = parser.parse_args()

    main(args)

