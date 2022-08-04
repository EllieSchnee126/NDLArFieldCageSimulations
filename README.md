# NDLArFieldCageSimulations
<br />
Both a geoBox and sifWriter program should be run in the same directory as eachother as well as sif1.txt and sif2.txt.<br />
<br />
geoBox.py builds and meshes the geometry of the field cage.<br />
Example: 'geoBox.py exampleFolder 10 3 38 10'<br />
This runs the program with an output folder (which it creates) named "example", strip width of 10mm, strip spacing of 3mm, 38 strips, and a mesh fineness of 10mm<br />
<br />
sifWriter.py writes the sif file for elmer using sif1.txt, sif2.txt, and mesh.boundary. Add a true or false to the end to impliment non-ideal resistors<br />
Example: 'sifWriter.py exampleFolder 38 False'<br />
This runs the program with the input/output folder of "example" and the parameter of 38 strips<br />
<br />
geoBoxSingleVol.py and sifWriterSingleVol.py take the same input parameters as their other respective programs but it will be for a model with a single drift volume. There is a section at the top of the geoBox program's code in order to change the other dimensions of the field cage.<br />
<br />
The multi-module programs can build multiple field cage structures near each other. This geometry also has the light collection panels with it. They take an extra parameter after the number of strips which is the number of modules.<br />
<br />
The 25p programs make a model which is one half of one drift volume. This allows for a finer mesh, but has no ability to look at cathode or TPC crossings.<br />
<br />
After running these files, either open the example folder in the elmer GUI (not recomended for large mesh files) and click the run button or if Elmer Solver is installed, cd into the example folder and run the command 'Elmer Solver case.sif'. Both of these will output 'data_t0001.vtu'<br />
