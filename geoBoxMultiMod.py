from netgen.occ import *
from ngsolve import *

# Geometry Values
values = [
    0.1,  # stripThickness
    6.35,  # boardThickness
    1000,  # boxLength
    3000,  # boxHeight
    10,  # lightPanelThickness
    23.7,  # moduleSideSpacing
    57.89  # moduleAnodeSpacing
]


def buildGeometry(stripWidth, stripSpacing, numberOfStrips, insideCorner):
    print("Starting Geometry")
    # Parameters
    global values
    stripDistance = stripWidth + stripSpacing
    stripThickness = values[0]
    boardThickness = values[1]
    boxLength = values[2]
    boxHeight = values[3]
    lightPanelThickness = values[4]
    boxWidth = stripDistance * numberOfStrips

    # FR4 board for field cage
    outerInsul = Box(Pnt(insideCorner[0], insideCorner[1], insideCorner[2]), Pnt(insideCorner[0] + boxLength,
        insideCorner[1] + 2 * boxWidth + 4 * stripThickness + 3 * boardThickness + 2 * stripSpacing, insideCorner[2] + boxHeight))
    innerInsul = Box(Pnt(insideCorner[0] + boardThickness, insideCorner[1] + boardThickness, insideCorner[2] + boardThickness),
        Pnt(insideCorner[0] + boxLength - boardThickness, insideCorner[1] + 2 * boxWidth + 4 * stripThickness + 2 * boardThickness + 2 * stripSpacing, insideCorner[2] + boxHeight - boardThickness))

    midInsul = Box(Pnt(insideCorner[0] + boardThickness, insideCorner[1] + boardThickness + 2 * stripThickness + boxWidth + stripSpacing, insideCorner[2] + boardThickness),
                   Pnt(insideCorner[0] + boxLength - boardThickness, insideCorner[1] + 2 * boardThickness + 2 * stripThickness + boxWidth + stripSpacing, insideCorner[2] + boxHeight - boardThickness))
    shapeInsul = outerInsul
    shapeInsul -= innerInsul
    shapeInsul += midInsul

    # Cathode in the middle of the field cage
    shapePlateMid1 = Box(Pnt(insideCorner[0] + boardThickness, insideCorner[1] + boardThickness + stripThickness + boxWidth + stripSpacing, insideCorner[2] + boardThickness),
                         Pnt(insideCorner[0] + boxLength - boardThickness, insideCorner[1] + boardThickness + 2 * stripThickness + boxWidth + stripSpacing, insideCorner[2] + boxHeight - boardThickness))
    shapePlateMid2 = Box(Pnt(insideCorner[0] + boardThickness, insideCorner[1] + 2 * boardThickness + 2 * stripThickness + boxWidth + stripSpacing, insideCorner[2] + boardThickness),
                         Pnt(insideCorner[0] + boxLength - boardThickness, insideCorner[1] + 2 * boardThickness + 3 * stripThickness + boxWidth + stripSpacing, insideCorner[2] + boxHeight - boardThickness))

    # Anodes on either end
    shapePlate1 = Box(Pnt(insideCorner[0] + boardThickness, insideCorner[1] + boardThickness, insideCorner[2] + boardThickness),
                      Pnt(insideCorner[0] + boxLength - boardThickness, insideCorner[1] + boardThickness + stripThickness, insideCorner[2] + boxHeight - boardThickness))
    shapePlate2 = Box(Pnt(insideCorner[0] + boardThickness, insideCorner[1] + 2 * boxWidth + 3 * stripThickness + 2 * boardThickness + 2 * stripSpacing, insideCorner[2] + boardThickness),
                      Pnt(insideCorner[0] + boxLength - boardThickness, insideCorner[1] + 2 * boxWidth + 4 * stripThickness + 2 * boardThickness + 2 * stripSpacing, insideCorner[2] + boxHeight - boardThickness))

    shapeInsul -= shapePlateMid1
    shapeInsul -= shapePlateMid2
    shapeInsul -= shapePlate1
    shapeInsul -= shapePlate2

    # Light Collection Panels
    shapeLight1 = Box(
        Pnt(insideCorner[0] + boardThickness + 51 * stripThickness, insideCorner[1] + boardThickness + 76 * stripThickness,
            insideCorner[2] + boardThickness + 51 * stripThickness),
        Pnt(insideCorner[0] + boardThickness + 51 * stripThickness + lightPanelThickness,
            insideCorner[1] + boardThickness + stripSpacing + boxWidth - 74 * stripThickness,
            insideCorner[2] + boxHeight - boardThickness - 51 * stripThickness))

    shapeLight2 = Box(
        Pnt(insideCorner[0] + boardThickness + 51 * stripThickness, insideCorner[1] + 2 * boardThickness + 78 * stripThickness + stripSpacing + boxWidth,
            insideCorner[2] + boardThickness + 51 * stripThickness),
        Pnt(insideCorner[0] + boardThickness + 51 * stripThickness + lightPanelThickness,
            insideCorner[1] + 2 * boardThickness + 2 * stripSpacing + 2 * boxWidth - 72 * stripThickness,
            insideCorner[2] + boxHeight - boardThickness - 51 * stripThickness))

    shapeLight3 = Box(
        Pnt(insideCorner[0] + boxLength - boardThickness - 51 * stripThickness, insideCorner[1] + boardThickness + 76 * stripThickness,
            insideCorner[2] + boardThickness + 51 * stripThickness),
        Pnt(insideCorner[0] + boxLength - boardThickness - 51 * stripThickness - lightPanelThickness,
            insideCorner[1] + boardThickness - 74 * stripThickness + stripSpacing + boxWidth,
            insideCorner[2] + boxHeight - boardThickness - 51 * stripThickness))

    shapeLight4 = Box(
        Pnt(insideCorner[0] + boxLength - boardThickness - 51 * stripThickness,
            insideCorner[1] + 2 * boardThickness + 78 * stripThickness + stripSpacing + boxWidth,
            insideCorner[2] + boardThickness + 51 * stripThickness),
        Pnt(insideCorner[0] + boxLength - boardThickness - 51 * stripThickness - lightPanelThickness,
            insideCorner[1] + 2 * boardThickness - 72 * stripThickness + 2 * stripSpacing + 2 * boxWidth,
            insideCorner[2] + boxHeight - boardThickness - 51 * stripThickness))

    # Strips for one side
    strips1 = []
    for x in range(numberOfStrips):
        outerStripTemp = Box(Pnt(insideCorner[0] + boardThickness,
                                 insideCorner[1] + boardThickness + stripThickness + stripSpacing + x * stripDistance,
                                 insideCorner[2] + boardThickness),
                             Pnt(insideCorner[0] + boxLength - boardThickness, insideCorner[
                                 1] + boardThickness + stripThickness + stripSpacing + stripWidth + x * stripDistance,
                                 insideCorner[2] + boxHeight - boardThickness))
        innerStripTemp = Box(Pnt(insideCorner[0] + boardThickness + stripThickness,
                                 insideCorner[1] + boardThickness + stripThickness + stripSpacing + x * stripDistance,
                                 insideCorner[2] + boardThickness + stripThickness),
                             Pnt(insideCorner[0] + boxLength - boardThickness - stripThickness, insideCorner[
                                 1] + boardThickness + stripThickness + stripSpacing + stripWidth + x * stripDistance,
                                 insideCorner[2] + boxHeight - boardThickness - stripThickness))
        outerStripTemp -= innerStripTemp
        strips1.append(outerStripTemp)


    # Strips for other side
    strips2 = []
    for x in range(numberOfStrips):
        outerStripTemp = Box(Pnt(insideCorner[0] + boardThickness,
                                 insideCorner[1] + 2 * boardThickness + 3 * stripThickness + 2 * stripSpacing + boxWidth + x * stripDistance,
                                 insideCorner[2] + boardThickness),
                             Pnt(insideCorner[0] + boxLength - boardThickness,
                                 insideCorner[1] + 2 * boardThickness + 3 * stripThickness + 2 * stripSpacing + boxWidth + stripWidth + x * stripDistance,
                                 insideCorner[2] + boxHeight - boardThickness))
        innerStripTemp = Box(Pnt(insideCorner[0] + boardThickness + stripThickness,
                                 insideCorner[1] + 2 * boardThickness + 3 * stripThickness + 2 * stripSpacing + boxWidth + x * stripDistance,
                                 insideCorner[2] + boardThickness + stripThickness),
                             Pnt(insideCorner[0] + boxLength - boardThickness - stripThickness,
                                 insideCorner[1] + 2 * boardThickness + 3 * stripThickness + 2 * stripSpacing + boxWidth + stripWidth + x * stripDistance,
                                 insideCorner[2] + boxHeight - boardThickness - stripThickness))
        outerStripTemp -= innerStripTemp
        strips2.append(outerStripTemp)


    # Input for Glue
    shape = []

    shape.append(shapeInsul)
    shape.append(shapeLight1)
    shape.append(shapeLight2)
    shape.append(shapeLight3)
    shape.append(shapeLight4)
    shape.append(shapePlate1)
    shape.append(shapePlate2)
    shape.append(shapePlateMid1)
    shape.append(shapePlateMid2)
    for strip in strips1:
        shape.append(strip)
    for strip in strips2:
        shape.append(strip)

    return shape


def mesh(shape, folderName, meshFineness):
    # Meshing
    geo = OCCGeometry(Glue(shape))
    mesh = Mesh(geo.GenerateMesh(maxh=meshFineness))
    mesh.ngmesh.Export(folderName, "Elmer Format")

    # Make solver file
    solver = open("./" + folderName + "/ELMERSOLVER_STARTINFO", 'w')
    solver.write("case.sif\n1\n")
    solver.close()


def main(args):
    global values
    moduleSideSpacing = values[5]
    moduleAnodeSpacing = values[6]
    stripDistance = float(args.StripWidth) + float(args.StripSpacing)
    anodeToAnode = 3 * values[1] + 4 * values[0] + 2 * stripDistance * int(args.StripNumber) + 2 * float(args.StripSpacing)
    corners = [[moduleSideSpacing/2, moduleAnodeSpacing/2, 0]] #, [-values[2] - moduleSideSpacing/2, moduleAnodeSpacing/2, 0]] #, [moduleSideSpacing/2, -anodeToAnode - moduleAnodeSpacing/2, 0], [-values[2] - moduleSideSpacing/2, -anodeToAnode - moduleAnodeSpacing/2, 0]]
    # LAr Volume
    shape = [Box(Pnt(-50, -50, -50), Pnt(moduleSideSpacing/2 + values[2] + 10, moduleAnodeSpacing/2 + anodeToAnode + 10, values[3] + 50))]
    # Module 0
    for i in range(len(corners)):
        module = buildGeometry(float(args.StripWidth), float(args.StripSpacing), int(args.StripNumber), corners[i])
        for sh in module:
            shape[0] -= sh
            shape.append(sh)

    mesh(shape, args.outFolderName, int(args.MeshFineness))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description = 'Create ND LAr geometry and export mesh')
    parser.add_argument('outFolderName',
                        help = 'output folder name (default: LArBox)')
    parser.add_argument('StripWidth',
                        help = 'Set the width of each strip')
    parser.add_argument('StripSpacing',
                        help = 'Set the spacing between each strip')
    parser.add_argument('StripNumber',
                        help = 'Set the number of strips')
    parser.add_argument('MeshFineness',
                        help='Set the fineness of the mesh')
    
    args = parser.parse_args()

    main(args)
