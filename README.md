# DBDIpy (Version 0.7.0)

DBDIpy is an open-source Python library for the curation and interpretation of dielectric barrier discharge ionisation mass spectrometric datasets.

# tl;dr
1. [Installation](#installation)
2. [User Tutorial](#tutorial)

# Introduction

Mass spectrometric data from direct injection analysis is hard to interprete as missing chromatographic separation complicates identification of fragments and adducts generated during the ionization process.

Here we present an *in-silico* approach to putatively identify multiple ion species arising from one analyte compound specially tailored for time-resolved datasets from dielectric barrier dischardge ionization (DBDI). DBDI is a relatively young technology which is rapidly gaining popularity in applications as breath analysis, process controll or food research. 

DBDIpy's core functionality relys on putative identification of in-source fragments (eg. [M-H<sub>2</sub>O+H]<sup>+</sup>) and in-source generated adducts (eg. [M+O<sub>n</sub>+H]<sup>+</sup>). 
Custom adduct species can be defined by the user and passed to this open-search algorithm. The identification is performed in a two-step procedure: 
- calculation of pointwise correlation identifies features with matching temporal intensity profiles through the experiment.
- (exact) mass differences are used to refine the nature of potential candidates. 

These putative identifications can than further be validated by the user, eg. based on tandem MS fragment data.               

DBDIpy further comes along with functions optimized for preprocessing of experimental data and visualization of identified adducts. The library is integrated into the matchms ecosystem to assimilate DBDIpy's functionalities into existing workflows.

For details, we invite you to read the [tutorial](#tutorial) or to try out the functions with our [demonstrational dataset](https://doi.org/10.5281/zenodo.7221089) or your own data!


|                     | Badges                                                                             |
|:-------------       |:-----------------------------------------------------------------------------------|
| `License`           | [![PyPi license](https://badgen.net/pypi/license/pip/)]([https://pypi.com/project/pip/](https://opensource.org/licenses/MIT/))|
| `Status`            | [![test](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/leopold-weidner/DBDIpy/graphs/commit-activity)|
| `Updated`           | [![GitHub latest commit](https://badgen.net/github/last-commit/Naereen/Strapdown.js)](https://GitHub.com/leopold-weidner/DBDIpy/commit/)|
| `Language`          | [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)|
| `Version`           | [![Python - 3.7, 3.8, 3.9, 3.10](https://img.shields.io/static/v1?label=Python&message=3.7+,+3.8+,+3.9+,+3.10&color=2d4b65)](https://www.python.org/)|
| `Operating Systems` | [![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg) [![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)|
| `Documentation`     | [![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](https://github.com/leopold-weidner/DBDIpy)|
| `Supporting Data`   | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7221089.svg)](https://doi.org/10.5281/zenodo.7221089)|
| `Further Reads`     | [![Researchgate](https://img.shields.io/badge/Research_Gate-00CCBB.svg?&style=for-the-badge&logo=ResearchGate&logoColor=white)](https://www.researchgate.net/profile/Leopold-Weidner)|


Latest Changes (since 0.6.0)
------------
- updated description.
- improved help pages.
- began writing tutorial.


User guide
============

## Installation

Prerequisites:  

- Anaconda (recommended)
- Python 3.7, 3.8, 3.9 or 3.10

DBDIpy can be installed from PyPI 
with:

```python
# we recomend installing DBDIpy in a new virtual environment
conda create --name DBDIpy python=3.9
conda activate DBDIpy
python3 -m pip install DBDIpy
```


Known installation issues:
Apple M1 chip users might encounter issues with automatic installation of matchms. 
Manual installation of the dependency as described on the libraries [official site](https://github.com/matchms/matchms) helps solving the issue. 
  

## Tutorial

The following tutorial showcases an ordinary data analysis workflow by going through all functions of DBDIpy from loading data until visualization of correlation results. Therefore, we supplied a demo dataset which is publicly available [here](https://doi.org/10.5281/zenodo.7221089).

The demo data is from an experiments where wheat bread was roasted for 20 min and monitored by DBDI coupled to FT-ICR-MS. It consits of 500 randomly selected features. 

![bitmap](https://user-images.githubusercontent.com/81673643/198022057-8b5da4b9-f6bd-43b7-9b6c-32fd119f93a7.png)
<p align = "center">
Fig.1 - Schematic DBDIpy workflow for in-source adduct and fragment detection: imported MS1 data are aligned, imputed and parsed to combined correlation and mass difference analysis.
</p>

### 1. Importing MS data
DBDIpy core functions utilize 2D tabular data. Raw mass spectra containing *m/z*-intensity-pairs first will need to be aligned to a DataFrame of features. We build features by using the ``align_spectra()`` function. ``align_spectra()`` is the interface to load data from open file formats such as .mgf, .mzML or .mzXML files via ``matchms.importing``.

If your data already is formatted accordingly, you can skip this step.

```python
# importing the downloaded .mgf files from demo data by matchms
import os
import pandas as pd
import DBDIpy as dbdi
from matchms.importing import load_from_mgf

demo_path = ""                                                #enter path to demo dataset
demo_mgf = os.path.join(demo_path, "example_dataset.mgf")
spectrums = list(load_from_mgf(demo_mgf))

##align the listed Spectra
specs_aligned = dbdi.align_spectra(df = spectrums, ppm_window = 2) 
```
We first imported the demo MS1 data into a list of ``matchms.Spectra`` objects. At this place you can run your personal ``matchms`` preprocessing pipelines or manually apply filters like noise reduction.
By aplication of ``align_spectra()``, we transformed the list of spectra objects to a two-dimensional ``pandas.DataFrame``. Now you have a column for each mass spectrometric scan and features are aligned to rows. The first column shows the mean *m/z* of a feature.
If a signal was not detected in a scan, the according field will be set to an instance of ``np.nan``.

Remember to set the ``ppm_window`` parameter according to the resolution of you mass spectrometric system. 

We now can inspect the aligned data, eg. by running: 

```python
specs_aligned.describe()
specs_aligned.info()
```

Likewise, ``specs_aligned.isnull().values.any()`` will give us an idea if there are missing values in the data. These cannot be handled by successive DBDIpy functions and most machine learning algorithms so we need to impute them.

### 2. Imputation of missing values

``impute_intensities()`` will assure that after imputation we will have a set of uniform length extracted ion chromatograms (XIC) in our DataFrame. This is an important prerequisite for pointwise correlation calculation and for many tools handling time series data.  

Missing values in our feature table will be imputed by a two-stage imputation algorithm. 
- First, missing values within the detected signal region are interpolated in between.
- Second, a noisy baseline is generated for all XIC to be of uniform length which the length of the longest XIC in the dataset.

The function lets the user decide which imputation method to use. Default mode is ``linear``, however several others are available. 

```python
feature_mz = specs_aligned["mean"]
specs_aligned = specs_aligned.drop("mean", axis = 1)

##impute the dataset
specs_imputed = dbdi.impute_intensities(df = specs_aligned, method = "linear")
```

Now ``specs_imputed`` does not contain any missing values anymore and is ready for adduct and in-source fragment detection.

```python
specs_imputed.isnull().values.any()
Out[]: False
```

specs_aligned.isnull().values.any

### 3. Detection of adducts and in-source fragments

Based on the ``specs_imputed``, we compute pointwise correlation of XIC traces to identify in-source adducts or in-source fragments generated during the DBD ionization process. The identification is performed in a two-step procedure: 
- First, calculation of pointwise intensity correlation identifies featur groups with matching temporal intensity profiles through the experiment.
- Second, (exact) mass differences are used to refine the nature of potential candidates. 

By default, ``identify_adducts()`` searches for [M-H<sub>2</sub>O+H]<sup>+</sup>, [M+O<sub>1</sub>+H]<sup>+</sup> and [M+O<sub>2</sub>+H]<sup>+</sup>. 
For demonstrational purposes we also want to search for [M+O<sub>3</sub>+H]<sup>+</sup> in this example.


```python
##prepare a DataFrame to search for O3-adducts
adduct_rule = pd.DataFrame({'deltamz': [47.984744],'motive': ["O3"]})

##identify in-source fragments and adducts
search_res = dbdi.identify_adducts(df = specs_imputed, masses = feature_mz, custom_adducts = adduct_rule,
                         method = "spearman", threshold = 0.9, mass_error = 2)
```
Note that ``identify_adducts()`` has a variety of parameters which allow high user cusomization. See the help file of the functions for details.




Contact
============
leopold.weidner@tum.de
