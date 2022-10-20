import matchms
import DBDIpy as dbdi
import pytest
import pandas as pd
import numpy as np
import random


#%%trigger input errors
def test_input_format_df():
    with pytest.raises(AttributeError):
        dbdi.export_to_spectra(df = "A", mzcol = 0)
    
def test_input_format_mz():
    with pytest.raises(IndexError):
        aligned_spectra = pd.DataFrame(np.random.randint(40, 999, size = (100, 100)))
        dbdi.export_to_spectra(aligned_spectra, mzcol = "X")    

   
#%% test output of function   
def test_export_outputn():

    aligned_spectra = pd.DataFrame(np.random.randint(40, 999, size = (100, 100)))
    exp = dbdi.export_to_spectra(aligned_spectra, mzcol = 0)
   
    assert isinstance(exp, list) 
    assert isinstance(exp[0], matchms.Spectrum)
    assert all(exp[0].peaks.mz == aligned_spectra.iloc[:,0].sort_values())
    assert all(exp[0].peaks.mz == exp[1].peaks.mz)
    assert all(np.sort(exp[0].peaks.intensities) == aligned_spectra.iloc[:,1].sort_values())
    
def test_check_for_nan():
    aligned_spectra = pd.DataFrame(np.random.randint(40, 999, size = (100, 100)))
    for c in range(1, aligned_spectra.shape[1]-1):
        aligned_spectra.iloc[random.randint(0, 99), c] = np.nan  
    exp = dbdi.export_to_spectra(aligned_spectra, mzcol = 0) 
    
    for e in range(len(exp)):
        assert not all(np.isnan(exp[e].peaks.mz))