
def writer(folderName, numberOfStripsPerSide):
    # Parameters
    numberOfStrips = 2 * numberOfStripsPerSide
    peakVoltage = 25000 #Volts
    voltageDifference = peakVoltage / (numberOfStrips / 2 + 1)

    # Opens or creates files
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

    # Writes the material and equation properties for all the bodies
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

    # Write template 2
    sif.write(templateSifText)
    print("template 2 copied")

    # Calculate Potentials
    potential = []
    for x in range(int(numberOfStrips/2) + 2):
        potential.append(x*voltageDifference)

    # Find number of boundaries
    lines = boundary.readlines() # The mesh.boundary files contains a list of mesh points and what boundary
    # number they are associated with. It is not organized by boundary number, so we have to comb through it to find
    # the largest boundary number
    numberOfBoundaries = 0
    for line in lines:
        split = line.split(" ")
        if int(split[1]) > numberOfBoundaries:
            numberOfBoundaries = int(split[1])

    # Calculate the strip boundary numbers
        # This section is finding the boundary number associated with each strip, so that they can be listed as having a
    # particular boundary condition. All the numbers that appear here a severely hard coded!! Any changes to the
    # geometry of the field cage that are not done through the parameters of geoBox.py may affect these calculations!
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

    # Write the BCs
    BC1 = "Boundary Condition 1\n  Target Boundaries(2) = " + str(boundaryIndex - 2) + " 17\n  Name = \"0\"\n  Potential = 0\nEnd\n\n"
    sif.write(BC1)

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
    boundary.close()


def main(args):
    writer(args.outFolderName, int(args.StripNumber))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Create ND LAr geometry and export mesh')
    parser.add_argument('outFolderName',
                        help='The folder which contains the mesh files')
    parser.add_argument('StripNumber',
                        help='Set the number of strips (on one side of the box)')

    args = parser.parse_args()

    main(args)
