# importing the downloaded .mgf files from demo data by matchms
import os
import feather
import numpy as np
import pandas as pd
import DBDIpy as dbdi
from matchms.importing import load_from_mgf
from matchms.exporting import save_as_mgf

#%%
demo_path = "C:/Users/weidner.leopold/Desktop/"                                                #enter path to demo dataset
demo_mgf = os.path.join(demo_path, "example_dataset.mgf")
spectrums = list(load_from_mgf(demo_mgf))

specs_aligned = dbdi.align_spectra(spectrums, ppm_window = 2) 
#%%
specs_aligned.describe()
specs_aligned.info()
#%%
feature_mz = specs_aligned["mean"]
specs_aligned = specs_aligned.drop("mean", axis = 1)

specs_imputed = dbdi.impute_intensities(specs_aligned, method = "linear")
#%%
adduct_rule = pd.DataFrame({'deltamz': [47.984744],'motive': ["O3"]})

##identify in-source fragments and adducts
search_res = dbdi.identify_adducts(df = specs_imputed, masses = feature_mz, custom_adducts = adduct_rule,
                                    method = "spearman", threshold = 0.9, mass_error = 2)
search_res
#%%
two_adducts = np.intersect1d(search_res["O"]["base_index"], np.intersect1d(search_res["O"]["base_index"],search_res["O2"]["base_index"]))
three_adducts = np.intersect1d(two_adducts , search_res["O3"]["base_index"])

three_adducts
#%%
demo_path = ""                                                    #enter path to demo dataset
demo_meta = os.path.join(demo_path, "example_metadata.feather")
annotation_metadata = feather.read_dataframe(demo_meta)

##plot the XIC
dbdi.plot_adducts(IDs = [55,66,83,99], df = specs_imputed, metadata = annotation_metadata, transform = True)
#%%
specs_imputed["mean"] = feature_mz

speclist = dbdi.export_to_spectra(df = specs_imputed, mzcol = 88)

##write processed data to .mgf file
save_as_mgf(speclist, "DBDIpy_processed_spectra.mgf")
