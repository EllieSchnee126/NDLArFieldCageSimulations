from netgen.occ import *
from ngsolve import *


def buildGeometry(stripWidth, stripSpacing, numberOfStrips):
    # parameters
    stripDistance = stripWidth + stripSpacing
    # ALL UNITS ARE IN MILLIMETERS!!!
    stripThickness = 0.1  # Thickness of the copper (or resistive polymer) on the FR-4 circuit board
    boardThickness = 6.35  # Thickness of the cicuit board: 1/4 inch = 6.35 mm
    plateTolerance = 0.5  # Distance between the endge of the cicuit board and the anode or cathode (can be 0)
    boxLength = 300  # The length of the outside of the field cage and is perpendicular to the drift direction
    boxHeight = 300  # The height of the outside of the field cage and is also perpendicular to the drift direction
    boxWidth = stripDistance*numberOfStrips  # The width of the outside of the field cage is parallel to the drift direction
    LArExtension = 50  # How much extra LAr is outside the field cage structure

    # Geometry
    #  LAr Volume
    shapeLAr = Box(Pnt(-LArExtension, -LArExtension, -LArExtension), Pnt(boxLength + LArExtension, boxWidth + LArExtension,
                                                                         boxHeight + LArExtension))
    #  Circuit board
    outerBoard = Box(Pnt(0, -stripSpacing, 0), Pnt(boxLength, boxWidth, boxHeight))
    innerBoard = Box(Pnt(boardThickness, -(stripWidth + 15), boardThickness), Pnt(boxLength - boardThickness,
                                                                      boxWidth+15, boxHeight - boardThickness))
    #  The anode and cathode (which is which is defined in the sif writer)
    shapePlate1 = Box(Pnt(boardThickness, -stripSpacing - plateTolerance, boardThickness),
                      Pnt(boxLength - boardThickness, -stripSpacing - stripThickness - plateTolerance, boxHeight - boardThickness))
    shapePlate2 = Box(Pnt(boardThickness, boxWidth + plateTolerance, boardThickness),
                      Pnt(boxLength - boardThickness, boxWidth + stripThickness + plateTolerance, boxHeight - boardThickness))
    
    #  Strips
    strips = []
    for x in range(numberOfStrips):
        outerStripTemp = Box(Pnt(boardThickness, x*stripDistance, boardThickness), Pnt(boxLength - boardThickness,
                                                            stripWidth + x*stripDistance, boxHeight - boardThickness))
        innerStripTemp = Box(Pnt(boardThickness + stripThickness, x*stripDistance, boardThickness + stripThickness),
                             Pnt(boxLength - boardThickness - stripThickness, stripWidth + x*stripDistance,
                                 boxHeight - boardThickness - stripThickness))
        outerStripTemp -= innerStripTemp
        strips.append(outerStripTemp)
    
    shapeInsul = outerBoard
    shapeInsul -= innerBoard
    
    shapeLAr -= shapeInsul
    for strip in strips:
        shapeLAr -= strip
    
    # Input for Glue
    shape = []
    
    shape.append(shapeLAr)
    shape.append(shapeInsul)
    shape.append(shapePlate1)
    shape.append(shapePlate2)
    for strip in strips:
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
    mesh(Shape, args.outFolderName, int(args.MeshFineness))  # Since this is smaller than the ND module,
    # the meshFineness could probably be less than 10 mm


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Create ND LAr geometry and export mesh')
    parser.add_argument('-o', '--outFolderName',
                        default='LArBox',
                        help='output folder name (default: LArBox)')
    parser.add_argument('StripWidth',
                        help='Set the width of each strip')
    parser.add_argument('StripSpacing',
                        help='Set the spacing between each strip')
    parser.add_argument('StripNumber',
                        help='Set the number of strips (on one side of the box)')
    parser.add_argument('MeshFineness',
                        help='Set the fineness of the mesh')

    args = parser.parse_args()

    main(args)

