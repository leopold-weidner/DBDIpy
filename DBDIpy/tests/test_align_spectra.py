import matchms
import numpy as np
import DBDIpy as dbdi
import pandas as pd
import pytest

#%%trigger input errors
def test_input_format():
    with pytest.raises(TypeError):
        spectrums = pd.DataFrame(np.random.randint(100, 1000000, size = (100, 100)))        
        dbdi.align_spectra(spectrums, ppm_window = 0.2)
    
    with pytest.raises(TypeError):  
        spectrums = []
        for i in range(100):
            spectrum = matchms.Spectrum(mz = np.linspace(1, 9, 10), intensities = np.random.rand(10).astype(float), metadata={})
            spectrums.append(spectrum) 
        dbdi.align_spectra(spectrums, ppm_window = "X")
        
#%% test output of function
def test_align_spectra(): 
    
    spectrums = []
    for i in range(100):
        spectrum = matchms.Spectrum(mz = np.linspace(1, 9, 10), intensities = np.random.rand(10).astype(float), metadata={})
        spectrums.append(spectrum)
    
    specs_aligned = dbdi.align_spectra(spectrums, ppm_window = 0.2)
    
    assert specs_aligned is not None
    assert isinstance(specs_aligned, pd.DataFrame)
    assert "mean" in specs_aligned.columns
    assert specs_aligned.shape[1]-1 == len(spectrums)
    assert all(specs_aligned.index.str.contains('ID'))
    assert all(specs_aligned.columns.str.contains('scan') |specs_aligned.columns.str.contains('mean'))
    assert specs_aligned["mean"].is_monotonic_increasing    