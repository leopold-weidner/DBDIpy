import DBDIpy as dbdi
import pytest
import pandas as pd
import numpy as np
import feather


#%%trigger input errors
def test_input_format_df():
    with pytest.raises(TypeError):
        dbdi.impute_intensities([212], method = "linear")
        
def test_input_format_method():
    with pytest.raises(ValueError):
        dummy = pd.DataFrame(np.random.randint(40, 999, size = (100, 100)))
        dbdi.impute_intensities(dummy, method = "trash")


#%% test output of function 
def test_impute_outputn():
    testdata = feather.read_dataframe("C:/Users/weidner.leopold/Nextcloud/Project212/src/data/example_dataset.feather")
    testdata = testdata.drop("ID", axis = 1)
    raw = testdata.copy()
    imputed = dbdi.impute_intensities(testdata, method = "linear")
    
    assert not testdata.isnull().values.any()
    assert imputed.shape == raw.shape