from netgen.occ import *
from ngsolve import *


# All lengths are in units of millimeters!!!!

def buildGeometry(stripWidth, stripSpacing, numberOfStrips):
    # Parameters for geometry
    stripDistance = stripWidth + stripSpacing
    stripThickness = 0.1
    boardThickness = 6.35
    boxLength = 1000
    boxHeight = 3000
    boxWidth = stripDistance * numberOfStrips + stripSpacing
    LArExtension = 100

    # Constructing the geometry

    # LAr Volume
    shapeLAr = Box(Pnt(-LArExtension, -(boxWidth + (boardThickness/2) + stripThickness + boardThickness) - LArExtension, -LArExtension),
                   Pnt(boxLength + LArExtension, boxWidth + (boardThickness/2) + stripThickness + boardThickness + LArExtension, boxHeight + LArExtension))

    # FR4 board for field cage
    outerInsul = Box(Pnt(0, -(boxWidth + (boardThickness/2) + stripThickness + boardThickness), 0), Pnt(boxLength, boxWidth + (boardThickness/2) + stripThickness + boardThickness, boxHeight))
    innerInsul = Box(Pnt(boardThickness, -(boxWidth + (boardThickness/2) + stripThickness), boardThickness), Pnt(boxLength - boardThickness, (boxWidth + (boardThickness/2) + stripThickness), boxHeight - boardThickness))

    shapeInsul = outerInsul
    shapeInsul -= innerInsul

    # Cathode in the middle of the field cage
    shapePlateMid1 = Box(Pnt(boardThickness, (boardThickness/2), boardThickness), Pnt(boxLength - boardThickness, (boardThickness/2) + stripThickness, boxHeight - boardThickness))
    shapePlateMid2 = Box(Pnt(boardThickness, -(boardThickness/2), boardThickness), Pnt(boxLength - boardThickness, -(boardThickness/2) - stripThickness, boxHeight - boardThickness))

    # Anodes on either end
    shapePlate1 = Box(Pnt(boardThickness, boxWidth + (boardThickness/2), boardThickness), Pnt(boxLength - boardThickness, boxWidth + (boardThickness/2) + stripThickness, boxHeight - boardThickness))
    shapePlate2 = Box(Pnt(boardThickness, -boxWidth - (boardThickness/2), boardThickness), Pnt(boxLength - boardThickness, -boxWidth - (boardThickness/2) - stripThickness, boxHeight - boardThickness))

    shapeInsul -= shapePlateMid1
    shapeInsul -= shapePlateMid2
    shapeInsul -= shapePlate1
    shapeInsul -= shapePlate2

    # Strips for one side
    strips1 = []
    for x in range(numberOfStrips):
        outerStripTemp = Box(Pnt(boardThickness, (boardThickness/2) + stripSpacing + x*stripDistance, boardThickness), Pnt(boxLength - boardThickness, (boardThickness/2) + stripSpacing + stripWidth + x*stripDistance, boxHeight - boardThickness))
        innerStripTemp = Box(Pnt(boardThickness + stripThickness, (boardThickness/2) + stripSpacing + x*stripDistance, boardThickness + stripThickness),
                             Pnt(boxLength - boardThickness - stripThickness, (boardThickness/2) + stripSpacing + stripWidth + x*stripDistance,
                                 boxHeight - boardThickness - stripThickness))
        outerStripTemp -= innerStripTemp
        strips1.append(outerStripTemp)

    # Strips for other side
    strips2 = []
    for x in range(numberOfStrips):
        outerStripTemp = Box(Pnt(boardThickness, -((boardThickness/2) + stripSpacing + x*stripDistance), boardThickness), Pnt(boxLength - boardThickness, -((boardThickness/2) + stripSpacing + stripWidth + x*stripDistance), boxHeight - boardThickness))
        innerStripTemp = Box(Pnt(boardThickness + stripThickness, -((boardThickness/2) + stripSpacing + x*stripDistance), boardThickness + stripThickness),
                             Pnt(boxLength - boardThickness - stripThickness, -((boardThickness/2) + stripSpacing + stripWidth + x*stripDistance),
                                 boxHeight - boardThickness - stripThickness))
        outerStripTemp -= innerStripTemp
        strips2.append(outerStripTemp)

    # Cutting out of the LAr Volume
    shapeLAr -= shapeInsul
    shapeLAr -= shapePlateMid1
    shapeLAr -= shapePlateMid2
    shapeLAr -= shapePlate1
    shapeLAr -= shapePlate2

    for strip in strips1:
        shapeLAr -= strip
    for strip in strips2:
        shapeLAr -= strip

    # Input for Glue
    shape = []

    shape.append(shapeLAr)
    shape.append(shapeInsul)
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

    # Make solver file (I think this is only necessary when running the elmer GUI)
    solver = open("./" + folderName + "/ELMERSOLVER_STARTINFO", 'w')
    solver.write("case.sif\n1\n")
    solver.close()


def main(args):
    # Builds the geometry and then meshes it
    Shape = buildGeometry(int(args.StripWidth), int(args.StripSpacing), int(args.StripNumber))
    mesh(Shape, args.outFolderName, int(args.MeshFineness)) # I had issues when trying to use too coarse of a mesh
    # (30 mm), however, even a 10mm mesh took close to 2 hours to run on our cluster


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description = 'Create ND LAr geometry and export mesh')
    parser.add_argument('-o', '--outFolderName',
                        default = 'LArBox',
                        help = 'output folder name (default: LArBox)')
    parser.add_argument('StripWidth',
                        help = 'Set the width of each strip')
    parser.add_argument('StripSpacing',
                        help = 'Set the spacing between each strip')
    parser.add_argument('StripNumber',
                        help = 'Set the number of strips (on one side of the box)')
    parser.add_argument('MeshFineness',
                        help='Set the fineness of the mesh')
    
    args = parser.parse_args()

    main(args)
