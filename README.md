# NDLArFieldCageSimulations
<br />
Both of these programs should be run in the same directory as eachother as well as sif1.txt and sif2.txt.<br />
<br />
geoBox.py builds and meshes the geometry of the field cage.<br />
Example: 'geoBox.py -o example 10 3 38 10'<br />
This runs the program with an output folder (which it creates) named "example", strip width of 10mm, strip spacing of 3mm, 38 strips, and a mesh fineness of 10mm<br />
<br />
geoBoxSingleVol.py takes the same parameters as geoBox.py but builds a model with a single drift volume. There is a section at the top of this program's code in order to change the other dimensions of the field cage.<br />
<br />
sifWriter.py writes the sif file for elmer using sif1.txt, sif2.txt, and mesh.boundary.<br />
Example: 'sifWriter.py example 38'<br />
This runs the program with the input/output folder of "example" and the parameter of 38 strips<br />
<br />
After running these files, either open the example folder in the elmer GUI (not recomended for large mesh files) and click the run button or if Elmer Solver is installed, cd into the example folder and run the command 'Elmer Solver case.sif'. Both of these will output 'data_t0001.vtu'<br />
