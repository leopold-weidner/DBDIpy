import random 
import pandas as pd
import numpy as np
import DBDIpy as dbdi
import pytest

#%%trigger input errors
def test_type_errors_IDs():
    with pytest.raises(TypeError):
        testdata = pd.DataFrame(np.random.randint(100, 1000000, size = (100, 100)))        
        dbdi.plot_adducts(IDs = {}, df = testdata)
        
def test_type_errors_df():
    with pytest.raises(TypeError):
        testID = random.sample(range(1, 99), 3)        
        dbdi.plot_adducts(IDs = testID, df = np.zeros(shape=(100, 100)))
        
def test_name_errors_metadata():
    with pytest.raises(NameError):
        meta = pd.DataFrame(np.random.randint(0, 10, size = (5, 5)), columns = list('ABCDE'))
        testdata = pd.DataFrame(np.random.randint(100, 1000000, size = (100, 100)))
        testID = random.sample(range(1, 99), 3)
        dbdi.plot_adducts(testID, testdata, metadata = meta, transform = False)     

def test_nan_error():
    with pytest.raises(ValueError):
        testdata = pd.DataFrame(np.random.randint(100, 1000000, size = (100, 100)))
        testdata.iloc[random.randint(1,99), random.randint(1,99)] = np.nan
        testID = random.sample(range(1, 99), 3)
        dbdi.plot_adducts(testID, testdata, metadata = None, transform = False)
        

#%%test for correct output
def test_plot_adducts_non_scaled():
    
    testID = random.sample(range(1, 99), 3)
    testdata = pd.DataFrame(np.random.randint(100, 1000000, size = (100, 100)))
    fig = dbdi.plot_adducts(testID, testdata, metadata = None, transform = False) 
    assert fig is not None
    
def test_plot_adducts_scaled():
    
    testID = random.sample(range(1, 99), 3)
    testdata = pd.DataFrame(np.random.randint(100, 1000000, size = (100, 100)))
    fig = dbdi.plot_adducts(testID, testdata, metadata = None, transform = True)
    assert fig is not None
