# prescribing


## Installation

### Basic package installation

For this project, you must have the following packages installed on your system:
```
    Python 3
    PIP 3
```
Check python3 is installed:
```
which python3
```
If not, install python3:
```
sudo apt-get install python3
```
Check pip3 is installed:
```
which pip3
```
If not, install pip3:
```
sudo apt-get install python3-pip
```

### Further package installation using virtualenv

It is recommended that you use virtualenv to create an isolated Python environment. This enables multiple side-by-side installations of Python, one for each project, allowing different project environments to remain isolated. This means you are able to run this script without its installations affecting other projects. 

Install virtualenv:
```
pip3 install virtualenv
```

The packages required to run the script are located in 'requirements.txt'. To install these packages, run:
```
pip3 install -r requirements.txt
```

## Analytical output

To run the python script, run:
```
python3 prescription_script.py
```
This will create a set of six graphical outputs, which can be found in the graphs directory.

### Antibiotics prescribed in Manchester CCG:
![](https://github.com/RachelDuffin/prescribing/blob/master/graphs/antibiotics_prescribed_in_Manchester_over_time.png)

### Normalised antibotics prescribed in Manchester CCG:
![](https://github.com/RachelDuffin/prescribing/blob/master/graphs/normalised_antibiotics_prescribed_in_manchester_over_time.png)

### Mean, max, min and standard deviation plot:
![](https://github.com/RachelDuffin/prescribing/blob/master/graphs/Mean_and_sd_antibiotics_per_1000_patients.png)

### Outliers for antibiotic prescriptions in Manchester CCG:
![](https://github.com/RachelDuffin/prescribing/blob/master/graphs/Prescription_outliers_in_Manchester_CCG.png)

### Box plot of antibiotics prescribed in Manchester CCG:
![](https://github.com/RachelDuffin/prescribing/blob/master/graphs/Box_plot.png)

### Heatmap of antibotics prescribed in Manchester CCG:
![](https://github.com/RachelDuffin/prescribing/blob/master/graphs/heatmap.png)



