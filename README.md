# SDF_Svmlight
convert sdf to svmlight
feature vec: ECFP4 (2048bit)

# requirement
* numpy
* RDKit (https://conda.anaconda.org/rdkit)

# demo
1. Go to PubChem assay page.

![](demo/1.PNG)

2. Download datatable (csv).

![](demo/2.PNG)

3. Download sdf file.

![](demo/3.PNG)

4. Run script.

`
python pubchem2svmlight.py pubchem_sdf datatable score_name
`

score_name for example: "%Inhibition at 10 uM"
