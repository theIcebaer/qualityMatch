# qualityMatch

This repository contains my analysis for the bicycle project crowd evaluation.

Due to the explorative nature of this project I decided to keep it simple and just put everyting in a jupyter notebook.
To run the project clone the repository and install the reqirements.
```
git clone git@github.com:theIcebaer/qualityMatch.git
pip install requirements.txt
```
Add the given dataset to the project. I recommend to put the files anonymized_project.json and references.json into a seperate data folder, 
since the ```load_dataset``` function does default to this location. If you choose to use a different location you will have to pass the respective paths to the 
function inside the notebook.
```
qualityMatch_notebook.ipynb
data
  | anonymized_project.json
  | references.json
```
Now you can run the notebook.
```
jupyter-notebook qualityMatch_notebook.ipynb
```
