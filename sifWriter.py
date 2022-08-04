import numpy as np


def wrtiter(folderName, numberOfStripsPerSide, resistance):
    # Parameters
    numberOfStrips = 2 * numberOfStripsPerSide
    peakVoltage = -25000
    voltageDifference = peakVoltage / (numberOfStripsPerSide + 1)

    resistances = (1 + np.random.normal(size=int(numberOfStripsPerSide) + 1) / 100) * 150*10**6  # 150 M Ohm resistors
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
    LArBody = "Body 1\n  Target Bodies(1) = 1\n  Name = \"Body 1\"\n  Equation = 1\n  Material = 3\nEnd\n\n"
    sif.write(LArBody)
    for y in range(5):
        boardBody = "Body " + str(y + 2) + "\n  Target Bodies(1) = " + str(y + 2) + "\n  Name = \"Body " + str(y + 2) + "\"\n  Equation = 1\n  Material = 2\nEnd\n\n"
        sif.write(boardBody)
    for x in range(numberOfStrips+4):
        stripBody = "Body " + str(x + 7) + "\n  Target Bodies(1) = " + str(x + 7) + "\n  Name = \"Body " + str(x + 7) + "\"\n  Equation = 1\n  Material = 1\nEnd\n\n"
        sif.write(stripBody)

    # Copy template 2
    templateSifText = templateSif2.read()
    print("template 2 read")

    # Write the template
    sif.write(templateSifText)
    print("template 2 copied")

    # Calculate Potentials
    potential = []
    for x in range(int(numberOfStripsPerSide) + 2):
        if x == 0 or x == int(numberOfStripsPerSide) + 1 or not resistance:
            potential.append(x * voltageDifference)
        else:
            potential.append(current * resistances[x] + potential[x-1])

    # Find number of boundaries
    lines = boundary.readlines()
    numberOfBoundaries = 0
    for line in lines:
        split = line.split(" ")
        if int(split[1]) > numberOfBoundaries:
            numberOfBoundaries = int(split[1])

    # Calculate the boundary numbers
    boundaryIndex = numberOfBoundaries - 16 - 4*numberOfStrips
    side1 = boundaryIndex
    side2 = boundaryIndex + numberOfStrips + 5
    side3 = boundaryIndex + 2*numberOfStrips + 10
    side4 = boundaryIndex + 3*numberOfStrips + 14
    boundaries1Side1, boundaries1Side2, boundaries1Side3, boundaries1Side4 = [], [], [], []
    boundaries2Side1, boundaries2Side2, boundaries2Side3, boundaries2Side4 = [], [], [], []

    for y in range(int(numberOfStrips/2)):
        boundaries1Side1.append(side1 + y)
        boundaries2Side1.append(numberOfBoundaries - 15 - 3*numberOfStrips - y)
        boundaries1Side2.append(side2 + y)
        boundaries2Side2.append(numberOfBoundaries - 10 - 2*numberOfStrips - y)
        boundaries1Side3.append(side3 + y)
        boundaries2Side3.append(numberOfBoundaries - 5 - numberOfStrips - y)
        boundaries1Side4.append(side4 + y)
        boundaries2Side4.append(numberOfBoundaries - 1 - y)

    # Write BC
    BC0 = "Boundary Condition 1\n  Target Boundaries(2) = " + str(boundaryIndex - 2) + " 17\n  Name = \"0\"\n  Potential = 0\nEnd\n\n"
    sif.write(BC0)

    for boundary in range(int(numberOfStrips/2)):
        BC = "Boundary Condition " + str(boundary + 2) + "\n  Target Boundaries(8) = " + str(boundaries1Side1[boundary]) +\
             " " + str(boundaries1Side2[boundary]) + " " + str(boundaries1Side3[boundary]) + " " +\
             str(boundaries1Side4[boundary]) + " " + str(boundaries2Side1[boundary]) +\
             " " + str(boundaries2Side2[boundary]) + " " + str(boundaries2Side3[boundary]) + " " +\
             str(boundaries2Side4[boundary]) + " " + "\n  Name = \"" + str(potential[boundary + 1]) + "\"\n  Potential = " +\
             str(potential[boundary + 1]) + "\nEnd\n\n"
        sif.write(BC)

    last = boundaryIndex - 4*numberOfStrips - (numberOfStrips + 3)
    BCLast = "Boundary Condition " + str(int(numberOfStrips/2) + 2) + "\n  Target Boundaries(2) = " + str(last) + " " + str(last - 11) + "\n  Name = \"" + str(potential[int(numberOfStrips/2) + 1]) + "\"\n  Potential = " +\
             str(potential[int(numberOfStrips/2) + 1]) + "\nEnd\n"
    sif.write(BCLast)

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
