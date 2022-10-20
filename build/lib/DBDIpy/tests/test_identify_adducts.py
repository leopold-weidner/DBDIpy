import DBDIpy as dbdi
import pytest
import pandas as pd
import numpy as np
import feather
import random


##test data is available under https://doi.org/10.5281/zenodo.7221089

#%%trigger input errors

def test_input_TypeErr():
    with pytest.raises(TypeError):
        annotation_metadata = feather.read_dataframe("C:/Users/weidner.leopold/Nextcloud/Project212/src/data/example_metadata.feather")
        dbdi.identify_adducts([212], masses = annotation_metadata["ThMass.Ion"],
                              custom_adducts = None, method = "spearman", 
                              threshold = 0.90, mass_error = 2)
        
        
def test_input_ValErr():
    with pytest.raises(ValueError):
        testdata = feather.read_dataframe("C:/Users/weidner.leopold/Nextcloud/Project212/src/data/example_dataset.feather")
        annotation_metadata = feather.read_dataframe("C:/Users/weidner.leopold/Nextcloud/Project212/src/data/example_metadata.feather")
        testdata = testdata.drop("ID", axis = 1)
        imputed = dbdi.impute_intensities(testdata, method = "linear")
        dbdi.identify_adducts(df = imputed, masses = annotation_metadata["ThMass.Ion"][0:5],
                              custom_adducts = None, method = "spearman", 
                              threshold = 0.90, mass_error = 2)

def test_input_NaN():
    with pytest.raises(ValueError):
        testdata = feather.read_dataframe("C:/Users/weidner.leopold/Nextcloud/Project212/src/data/example_dataset.feather")
        annotation_metadata = feather.read_dataframe("C:/Users/weidner.leopold/Nextcloud/Project212/src/data/example_metadata.feather")
        testdata = testdata.drop("ID", axis = 1)
        imputed = dbdi.impute_intensities(testdata, method = "linear")
        for c in range(1, imputed.shape[1]-1):
            imputed.iloc[random.randint(0, 99), c] = np.nan  
        dbdi.identify_adducts(df = imputed, masses = annotation_metadata["ThMass.Ion"],
                              custom_adducts = None, method = "spearman", 
                              threshold = 0.90, mass_error = 2)

def test_input_custadd():
    with pytest.raises(TypeError):
        testdata = feather.read_dataframe("C:/Users/weidner.leopold/Nextcloud/Project212/src/data/example_dataset.feather")
        annotation_metadata = feather.read_dataframe("C:/Users/weidner.leopold/Nextcloud/Project212/src/data/example_metadata.feather")
        testdata = testdata.drop("ID", axis = 1)
        imputed = dbdi.impute_intensities(testdata, method = "linear")
        ca = pd.DataFrame({'deltamz': [5],'motive': ["fail"], 'trash': ["trash"]})
        dbdi.identify_adducts(df = imputed, masses = annotation_metadata["ThMass.Ion"],
                              custom_adducts = ca, method = "spearman", 
                              threshold = 0.90, mass_error = 2)
        
    with pytest.raises(TypeError):
        testdata = feather.read_dataframe("C:/Users/weidner.leopold/Nextcloud/Project212/src/data/example_dataset.feather")
        annotation_metadata = feather.read_dataframe("C:/Users/weidner.leopold/Nextcloud/Project212/src/data/example_metadata.feather")
        testdata = testdata.drop("ID", axis = 1)
        imputed = dbdi.impute_intensities(testdata, method = "linear")
        ca = {'deltamz': [5],'motive': ["fail"]}
        dbdi.identify_adducts(df = imputed, masses = annotation_metadata["ThMass.Ion"],
                                 custom_adducts = ca, method = "spearman", 
                                 threshold = 0.90, mass_error = 2)
        
def test_input_wrong_corr():
    with pytest.raises(ValueError):
        testdata = feather.read_dataframe("C:/Users/weidner.leopold/Nextcloud/Project212/src/data/example_dataset.feather")
        annotation_metadata = feather.read_dataframe("C:/Users/weidner.leopold/Nextcloud/Project212/src/data/example_metadata.feather")
        testdata = testdata.drop("ID", axis = 1)
        imputed = dbdi.impute_intensities(testdata, method = "linear")
        dbdi.identify_adducts(df = imputed, masses = annotation_metadata["ThMass.Ion"],
                              custom_adducts = None, method = "trash", 
                              threshold = 0.90, mass_error = 2)

#%% test output of function 
def test_impute_outputn():
    testdata = feather.read_dataframe("C:/Users/weidner.leopold/Nextcloud/Project212/src/data/example_dataset.feather")
    annotation_metadata = feather.read_dataframe("C:/Users/weidner.leopold/Nextcloud/Project212/src/data/example_metadata.feather")
    testdata = testdata.drop("ID", axis = 1)
    imputed = dbdi.impute_intensities(testdata, method = "linear")
    trtest= 0.90
    ertest = 5
    res_adductsearch =  dbdi.identify_adducts(df = imputed, masses = annotation_metadata["ThMass.Ion"],
                                              threshold = trtest, mass_error = ertest)
    
    assert res_adductsearch is not None
    assert isinstance(res_adductsearch, dict)
    assert isinstance(list(res_adductsearch.values())[0], pd.DataFrame)
    assert all(list(res_adductsearch.values())[0]["corr"] > trtest)
    assert all((list(res_adductsearch.values())[0]["mzdiff"] <= 15.994915 + 15.994915 * ertest * 1e-6) & 
               (list(res_adductsearch.values())[0]["mzdiff"] >= 15.994915 - 15.994915 * ertest * 1e-6))