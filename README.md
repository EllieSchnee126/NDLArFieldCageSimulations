# NDLArFieldCageSimulations

Both of these programs should be run in the same directory as eachother as well as sif1.txt and sif2.txt.

geoBox.py builds and meshes the geometry of the field cage.
Example: 'geoBox.py -o example 10 3 38 10'
This runs the program with an output folder (which it creates) named "example", strip width of 10mm, strip spacing of 3mm, 38 strips, and a mesh fineness of 10mm

sifWriter.py writes the sif file for elmer using sif1.txt, sif2.txt, and mesh.boundary.
Example: 'sifWriter.py example 38'
This runs the program with the input/output folder of "example" and the parameter of 38 strips

After running these files, either open the example folder in the elmer GUI (not recomended for large mesh files) and click the run button or if Elmer Solver is installed, cd into the example folder and run the command 'Elmer Solver case.sif'. Both of these will output 'data_t0001.vtu'
