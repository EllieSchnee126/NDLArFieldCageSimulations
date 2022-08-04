from netgen.occ import *
from ngsolve import *

# This code only differs from geoBox.py in two ways. The first is that it includes the light collection panels.
# The second is that the entire field cage geometry is based around a single point and thus by supplying a list of
# coordinates, a multiple module setup can be constructed.

# Geometry Values IN MILLIMETERS
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
    volWidth = stripDistance * numberOfStrips

    # FR4 board for field cage
    outerInsul = Box(Pnt(insideCorner[0], insideCorner[1], insideCorner[2]), Pnt(insideCorner[0] + boxLength,
                                                                                 insideCorner[
                                                                                     1] + 2 * volWidth + 4 * stripThickness + 3 * boardThickness + 2 * stripSpacing,
                                                                                 insideCorner[2] + boxHeight))
    innerInsul = Box(
        Pnt(insideCorner[0] + boardThickness, insideCorner[1] + boardThickness, insideCorner[2] + boardThickness),
        Pnt(insideCorner[0] + boxLength - boardThickness,
            insideCorner[1] + 2 * volWidth + 4 * stripThickness + 2 * boardThickness + 2 * stripSpacing,
            insideCorner[2] + boxHeight - boardThickness))

    midInsul = Box(Pnt(insideCorner[0] + boardThickness,
                       insideCorner[1] + boardThickness + 2 * stripThickness + volWidth + stripSpacing,
                       insideCorner[2] + boardThickness),
                   Pnt(insideCorner[0] + boxLength - boardThickness,
                       insideCorner[1] + 2 * boardThickness + 2 * stripThickness + volWidth + stripSpacing,
                       insideCorner[2] + boxHeight - boardThickness))
    shapeInsul = outerInsul
    shapeInsul -= innerInsul
    shapeInsul += midInsul

    # Cathode in the middle of the field cage
    shapePlateMid1 = Box(Pnt(insideCorner[0] + boardThickness,
                             insideCorner[1] + boardThickness + stripThickness + volWidth + stripSpacing,
                             insideCorner[2] + boardThickness),
                         Pnt(insideCorner[0] + boxLength - boardThickness,
                             insideCorner[1] + boardThickness + 2 * stripThickness + volWidth + stripSpacing,
                             insideCorner[2] + boxHeight - boardThickness))
    shapePlateMid2 = Box(Pnt(insideCorner[0] + boardThickness,
                             insideCorner[1] + 2 * boardThickness + 2 * stripThickness + volWidth + stripSpacing,
                             insideCorner[2] + boardThickness),
                         Pnt(insideCorner[0] + boxLength - boardThickness,
                             insideCorner[1] + 2 * boardThickness + 3 * stripThickness + volWidth + stripSpacing,
                             insideCorner[2] + boxHeight - boardThickness))

    # Anodes on either end
    shapePlate1 = Box(
        Pnt(insideCorner[0] + boardThickness, insideCorner[1] + boardThickness, insideCorner[2] + boardThickness),
        Pnt(insideCorner[0] + boxLength - boardThickness, insideCorner[1] + boardThickness + stripThickness,
            insideCorner[2] + boxHeight - boardThickness))
    shapePlate2 = Box(Pnt(insideCorner[0] + boardThickness,
                          insideCorner[1] + 2 * volWidth + 3 * stripThickness + 2 * boardThickness + 2 * stripSpacing,
                          insideCorner[2] + boardThickness),
                      Pnt(insideCorner[0] + boxLength - boardThickness,
                          insideCorner[1] + 2 * volWidth + 4 * stripThickness + 2 * boardThickness + 2 * stripSpacing,
                          insideCorner[2] + boxHeight - boardThickness))

    shapeInsul -= shapePlateMid1
    shapeInsul -= shapePlateMid2
    shapeInsul -= shapePlate1
    shapeInsul -= shapePlate2

    # Light Collection Panels
    shapeLight1 = Box(
        Pnt(insideCorner[0] + boardThickness + 50 * stripThickness,
            insideCorner[1] + boardThickness + 6 * stripThickness,
            insideCorner[2] + boardThickness + 5 * stripThickness),
        Pnt(insideCorner[0] + boardThickness + 50 * stripThickness + lightPanelThickness,
            insideCorner[1] + boardThickness + stripSpacing + volWidth - 4 * stripThickness,
            insideCorner[2] + boxHeight - boardThickness - 5 * stripThickness))

    shapeLight2 = Box(
        Pnt(insideCorner[0] + boardThickness + 50 * stripThickness,
            insideCorner[1] + 2 * boardThickness + 8 * stripThickness + stripSpacing + volWidth,
            insideCorner[2] + boardThickness + 5 * stripThickness),
        Pnt(insideCorner[0] + boardThickness + 50 * stripThickness + lightPanelThickness,
            insideCorner[1] + 2 * boardThickness + 2 * stripSpacing + 2 * volWidth - 2 * stripThickness,
            insideCorner[2] + boxHeight - boardThickness - 5 * stripThickness))

    shapeLight3 = Box(
        Pnt(insideCorner[0] + boxLength - boardThickness - 5 * stripThickness,
            insideCorner[1] + boardThickness + 6 * stripThickness,
            insideCorner[2] + boardThickness + 5 * stripThickness),
        Pnt(insideCorner[0] + boxLength - boardThickness - 5 * stripThickness - lightPanelThickness,
            insideCorner[1] + boardThickness - 4 * stripThickness + stripSpacing + volWidth,
            insideCorner[2] + boxHeight - boardThickness - 5 * stripThickness))

    shapeLight4 = Box(
        Pnt(insideCorner[0] + boxLength - boardThickness - 5 * stripThickness,
            insideCorner[1] + 2 * boardThickness + 8 * stripThickness + stripSpacing + volWidth,
            insideCorner[2] + boardThickness + 5 * stripThickness),
        Pnt(insideCorner[0] + boxLength - boardThickness - 5 * stripThickness - lightPanelThickness,
            insideCorner[1] + 2 * boardThickness - 2 * stripThickness + 2 * stripSpacing + 2 * volWidth,
            insideCorner[2] + boxHeight - boardThickness - 5 * stripThickness))

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
                                 insideCorner[
                                     1] + 2 * boardThickness + 3 * stripThickness + 2 * stripSpacing + volWidth + x * stripDistance,
                                 insideCorner[2] + boardThickness),
                             Pnt(insideCorner[0] + boxLength - boardThickness,
                                 insideCorner[
                                     1] + 2 * boardThickness + 3 * stripThickness + 2 * stripSpacing + volWidth + stripWidth + x * stripDistance,
                                 insideCorner[2] + boxHeight - boardThickness))
        innerStripTemp = Box(Pnt(insideCorner[0] + boardThickness + stripThickness,
                                 insideCorner[
                                     1] + 2 * boardThickness + 3 * stripThickness + 2 * stripSpacing + volWidth + x * stripDistance,
                                 insideCorner[2] + boardThickness + stripThickness),
                             Pnt(insideCorner[0] + boxLength - boardThickness - stripThickness,
                                 insideCorner[
                                     1] + 2 * boardThickness + 3 * stripThickness + 2 * stripSpacing + volWidth + stripWidth + x * stripDistance,
                                 insideCorner[2] + boxHeight - boardThickness - stripThickness))
        outerStripTemp -= innerStripTemp
        strips2.append(outerStripTemp)

    # Make it 1/4th

    shapeLargeCut = Box(Pnt(insideCorner[0] + boxLength/2, insideCorner[1], insideCorner[2]), Pnt(insideCorner[0] + boxLength,
        insideCorner[1] + 2*volWidth + 3*boardThickness + 4 *stripThickness + 2*stripSpacing, insideCorner[2] + boxHeight))
    shapeSmallCut = Box(Pnt(insideCorner[0], insideCorner[1] + 1.5 * boardThickness + 2*stripThickness + stripSpacing +
        volWidth, insideCorner[2]), Pnt(insideCorner[0] + boxLength/2, insideCorner[1] + 2*volWidth + 3*boardThickness +
        4 *stripThickness + 2 * stripSpacing, insideCorner[2] + boxHeight))

    # Input for Glue
    shape = []

    shapeInsul -= (shapeLargeCut + shapeSmallCut)
    shapeLight1 -= (shapeLargeCut + shapeSmallCut)
    shapeLight2 -= (shapeLargeCut + shapeSmallCut)
    shapeLight3 -= (shapeLargeCut + shapeSmallCut)
    shapeLight4 -= (shapeLargeCut + shapeSmallCut)
    shapePlate1 -= (shapeLargeCut + shapeSmallCut)
    shapePlate2 -= (shapeLargeCut + shapeSmallCut)
    shapePlateMid1 -= (shapeLargeCut + shapeSmallCut)
    shapePlateMid2 -= (shapeLargeCut + shapeSmallCut)

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
        strip -= (shapeLargeCut + shapeSmallCut)
        shape.append(strip)
    for strip in strips2:
        strip -= (shapeLargeCut + shapeSmallCut)
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
    anodeToCathode = 1.5 * values[1] + 2 * values[0] + stripDistance * int(args.StripNumber) + float(args.StripSpacing)
    # Each corner listed will create a module. The modules are of size [boxLength, anodeToAnode, boxHeight]
    corner = [moduleSideSpacing / 2, moduleAnodeSpacing / 2, 0]
    # LAr Volume -- Adjust this as necessary to cover the modules
    lar = Box(Pnt(-20, -20, -50), Pnt(values[2]/2 + 15, moduleAnodeSpacing + anodeToCathode + 10, value[3] + 50))
    shape = [lar]
    # Module Creation
    module = buildGeometry(float(args.StripWidth), float(args.StripSpacing), int(args.StripNumber), corner)
    for sh in module:
        shape[0] -= sh
        shape.append(sh)

    mesh(shape, args.outFolderName, int(args.MeshFineness))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Create ND LAr geometry and export mesh')
    parser.add_argument('outFolderName',
                        help='output folder name (default: LArBox)')
    parser.add_argument('StripWidth',
                        help='Set the width of each strip')
    parser.add_argument('StripSpacing',
                        help='Set the spacing between each strip')
    parser.add_argument('StripNumber',
                        help='Set the number of strips')
    parser.add_argument('MeshFineness',
                        help='Set the fineness of the mesh')

    args = parser.parse_args()

    main(args)
