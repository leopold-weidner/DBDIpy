import DBDIpy as dbdi
import pytest
import pandas as pd
import numpy as np
import feather


#%%trigger input errors
def test_input_format_df():
    with pytest.raises(TypeError):
        dbdi.propose_adducts([212], method = "linear")
              
def test_input_format_method():
    with pytest.raises(ValueError):
        dummy = pd.DataFrame(np.random.randint(1, 2, size = (20, 20)))
        dbdi.propose_adducts(dummy, method = "trash")


#%% test output of function 
def test_proposals_output():
    testdata = feather.read_dataframe("C:/Users/weidner.leopold/Nextcloud/Project212/src/data/example_dataset.feather")
    annotation_metadata = feather.read_dataframe("C:/Users/weidner.leopold/Nextcloud/Project212/src/data/example_metadata.feather")
    
    testproposal = dbdi.propose_adducts(ID = 55, df = testdata, 
                                        masses = annotation_metadata["ThMass.Ion"],
                                        method = "pearson", threshold = 0.95, 
                                        mass_error = 0.005)
    
    assert not testproposal.isnull()
