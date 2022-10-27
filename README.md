# DBDIpy (Version 0.8.1)
DBDIpy is an open-source Python library for the curation and interpretation of dielectric barrier discharge ionisation mass spectrometric datasets.

# tl;dr
1. [Installation](#installation)
2. [User Tutorial](#tutorial)

# Introduction

Mass spectrometric data from direct injection analysis is hard to interpret as missing chromatographic separation complicates identification of fragments and adducts generated during the ionization process.

Here we present an *in-silico* approach to putatively identify multiple ion species arising from one analyte compound specially tailored for time-resolved datasets from dielectric barrier discharge ionization (DBDI). DBDI is a relatively young technology which is rapidly gaining popularity in applications as breath analysis, process control or food research. 

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
| `Updated`           | ![latest commit](https://img.shields.io/github/last-commit/leopold-weidner/DBDIpy?style=plastic)|
| `Language`          | [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)|
| `Version`           | [![Python - 3.7, 3.8, 3.9, 3.10](https://img.shields.io/static/v1?label=Python&message=3.7+,+3.8+,+3.9+,+3.10&color=2d4b65)](https://www.python.org/)|
| `Operating Systems` | [![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg) [![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)|
| `Documentation`     | [![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](https://github.com/leopold-weidner/DBDIpy)|
| `Supporting Data`   | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7221089.svg)](https://doi.org/10.5281/zenodo.7221089)|
| `Further Reads`     | [![Researchgate](https://img.shields.io/badge/Research_Gate-00CCBB.svg?&style=for-the-badge&logo=ResearchGate&logoColor=white)](https://www.researchgate.net/profile/Leopold-Weidner)|


Latest Changes (since 0.6.0)
------------
- updated descriptions.
- improved help pages.
- finished tutorial.


User guide
============

## Installation

Prerequisites:  

- Anaconda (recommended)
- Python 3.7, 3.8, 3.9 or 3.10

DBDIpy can be installed from PyPI 
with:

```python
# we recommend installing DBDIpy in a new virtual environment
conda create --name DBDIpy python=3.9
conda activate DBDIpy
python3 -m pip install DBDIpy
```


Known installation issues:
Apple M1 chip users might encounter issues with automatic installation of matchms. 
Manual installation of the dependency as described on the libraries [official site](https://github.com/matchms/matchms) helps solving the issue. 
  

## Tutorial

The following tutorial showcases an ordinary data analysis workflow by going through all functions of DBDIpy from loading data until visualization of correlation results. Therefore, we supplied a demo dataset which is publicly available [here](https://doi.org/10.5281/zenodo.7221089).

The demo data is from an experiments where wheat bread was roasted for 20 min and monitored by DBDI coupled to FT-ICR-MS. It consists of 500 randomly selected features. 

![bitmap](https://user-images.githubusercontent.com/81673643/198022057-8b5da4b9-f6bd-43b7-9b6c-32fd119f93a7.png)
<p align = "center">
Fig.1 - Schematic DBDIpy workflow for in-source adduct and fragment detection: imported MS1 data are aligned, imputed and parsed to combined correlation and mass difference analysis.
</p>

### 1. Importing MS data
DBDIpy core functions utilize 2D tabular data. Raw mass spectra containing *m/z*-intensity-pairs first will need to be aligned to a DataFrame of features. We build features by using the ``align_spectra()`` function. ``align_spectra()`` is the interface to load data from open file formats such as .mgf, .mzML or .mzXML files via ``matchms.importing``.

If your data already is formatted accordingly, you can skip this step.

```python
##loading libraries for the tutorial
import os
import feather
import numpy as np
import pandas as pd
import DBDIpy as dbdi
from matchms.importing import load_from_mgf
from matchms.exporting import save_as_mgf

##importing the downloaded .mgf files from demo data by matchms
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

We now can inspect the aligned data, e.g. by running: 

```python
specs_aligned.describe()
specs_aligned.info()
```

Likewise, ``specs_aligned.isnull().values.any()`` will give us an idea if there are missing values in the data. These cannot be handled by successive DBDIpy functions and most machine learning algorithms, so we need to impute them.

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
##check if NaN are present in DataFrame
specs_imputed.isnull().values.any()
Out[]: False
```


### 3. Detection of adducts and in-source fragments

Based on the ``specs_imputed``, we compute pointwise correlation of XIC traces to identify in-source adducts or in-source fragments generated during the DBD ionization process. The identification is performed in a two-step procedure: 
- First, calculation of pointwise intensity correlation identifies feature groups with matching temporal intensity profiles through the experiment.
- Second, (exact) mass differences are used to refine the nature of potential candidates. 

By default, ``identify_adducts()`` searches for [M-H<sub>2</sub>O+H]<sup>+</sup>, [M+O<sub>1</sub>+H]<sup>+</sup> and [M+O<sub>2</sub>+H]<sup>+</sup>. 
For demonstrational purposes we also want to search for [M+O<sub>3</sub>+H]<sup>+</sup> in this example.
Note that ``identify_adducts()`` has a variety of other parameters which allow high user customization. See the help file of the functions for details.

```python
##prepare a DataFrame to search for O3-adducts
adduct_rule = pd.DataFrame({'deltamz': [47.984744],'motive': ["O3"]})

##identify in-source fragments and adducts
search_res = dbdi.identify_adducts(df = specs_imputed, masses = feature_mz, custom_adducts = adduct_rule,
                                   method = "spearman", threshold = 0.9, mass_error = 2)
```

The function will return a dictionary holding one DataFrame for each adduct type that was defined. A typical output looks like the following:

```python
##output search results
search_res
Out[24]: 
{'O':   base_mz    base_index  match_mz  match_index    mzdiff      corr
 19     215.11789          24  231.11280        ID40  15.99491  0.963228
 310    224.10699          33  240.10191        ID51  15.99492  0.939139
 605    231.11280          39  215.11789        ID25  15.99491  0.963228
 1413   240.10191          50  224.10699        ID34  15.99492  0.939139
 1668   244.13321          55  260.12812        ID67  15.99491  0.976541,
                                 ...
 'O2':  base_mz    base_index  match_mz  match_index    mzdiff      corr
 1437   240.10191          50  272.09174        ID77  31.98983  0.988866
 1677   244.13321          55  276.12304        ID84  31.98983  0.972251
 2362   260.12812          66  292.11795       ID100  31.98983  0.964096
 3024   272.09174          76  240.10191        ID51  31.98983  0.988866
 3354   276.12304          83  244.13321        ID56  31.98983  0.972251,
                                 ...
 'H2O': base_mz    base_index  match_mz  match_index    mzdiff      corr
 621    231.11280          39  249.12337        ID60  18.01057  0.933640
 1883   249.12337          59  231.11280        ID40  18.01057  0.933640
 3263   275.13902          82  293.14958       ID102  18.01056  0.948774
 4775   293.14958         101  275.13902        ID83  18.01056  0.948774
 5573   300.08665         112  318.09722       ID140  18.01057  0.905907
                                  ...
 'O3':  base_mz    base_index  match_mz  match_index    mzdiff      corr
 320    224.10699          33  272.09174        ID77  47.98475  0.924362
 1688   244.13321          55  292.11795       ID100  47.98474  0.964896
 3013   272.09174          76  224.10699        ID34  47.98475  0.924362
 4631   292.11795          99  244.13321        ID56  47.98474  0.964896
 13597  438.28502         308  486.26976       ID356  47.98474  0.935359
                                  ...
````
The ``base_mz`` and ``base_index`` column give us the index of the features which correlates with a correlation partner specified in ``match_mz`` and ``match_index``.
The mass difference between both is given for validation purpose and the correlation coefficient between both features is listed. 

Now we can for example search series of Oxygen adducts of a single analyte:

```python
##search for oxygenation series
two_adducts = np.intersect1d(search_res["O"]["base_index"], np.intersect1d(search_res["O"]["base_index"],search_res["O2"]["base_index"]))
three_adducts = np.intersect1d(two_adducts , search_res["O3"]["base_index"])

three_adducts
Out[33]: array([55, 99], dtype=int64)
```

This tells us that features 55 and 99 both putatively have [M+O<sub>1-3</sub>+H]<sup>+</sup> adduct ions with correlations of  R<sup>2</sup> > 0.9 in our dataset.
Let's visualize this finding!


### 4. Visualization of correlation results

Now that we putatively identified some related ions of a single analyte, we want to check their temporal response during the baking experiment.
Therefore, we can use the ``plot_adducts()`` function to conveniently draw XICs.
The demo dataset even comes along with some annotated metadata for our features, so we can decorate the plot and check our previous results!

```python
##load annotation metadta
demo_path = ""                                                     #enter path to demo dataset
demo_meta = os.path.join(demo_path, "example_metadata.feather")
annotation_metadata = feather.read_dataframe(demo_meta)

##plot the XIC
dbdi.plot_adducts(IDs = [55,66,83,99], df = specs_imputed, metadata = annotation_metadata, transform = True)
```

<p align="center">
  <img width="600" height="288" src="https://user-images.githubusercontent.com/81673643/198047792-9a9019ab-5c00-4365-a25c-2cbcd0d3d20f.png">
</p>
<p align = "center">
Fig.2 - XIC plots for features 55, 66, 83 and 99 which have highly correlated intensity profile through the baking experiment.
</p>

We see that the XIC traces show a similar intensity profile through the experiment. The plot further tells us the correlation coefficients of the identified adducts.
From the metadata we can see that the detected mass signals were previously annotated as C<sub>15</sub>H<sub>17</sub>O<sub>2-5</sub>N which tells us that we most probably found an Oxgen-adduct series. 

If MS2 data was recorded during the experiment we now can go on further and compare fragment spectra to reassure the identifications. You might find [ms2deepscore](https://github.com/matchms/ms2deepscore) to be a usefull library to do so in an automated way. 

### 5. Exporting tabular MS data to match.Spectra objects

If you want to export your (imputed) tabular data to ``matchms.Spectra`` objects, you can do so by calling the ``export_to_spectra()`` function. We just need to re-add a column containing *m/z* values of the features.
This gives you access to the matchms suite and enables you to safe your mass spectrometric data to open file formats.
Hint: you can manually add some metadata after construction of the list of spectra.  

```python
##export tabular MS data back to list of spectrums.
specs_imputed["mean"] = feature_mz

speclist = dbdi.export_to_spectra(df = specs_imputed, mzcol = 88)

##write processed data to .mgf file
save_as_mgf(speclist, "DBDIpy_processed_spectra.mgf")
```

We hope you liked this quick introduction into DBDIpy and will find its functions helpful and inspiring on your way to work through data from direct infusion mass spectrometry. Of course, the functions are applicable to all sort of ionisation mechanisms and you can modify the set of adducts to search in accordance to your source. 

If you have open questions left about functions, their parameter or the algorithms we invite you to read through the built-in help files. If this does not clarify the issues, please do not hesitate to get in touch with us!

Contact
============
leopold.weidner@tum.de

