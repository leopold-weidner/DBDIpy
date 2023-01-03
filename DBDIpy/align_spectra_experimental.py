import numpy as np
import pandas as pd

def align_features(features, num_scans, accuracy):
  sorted_features = sorted(features, key=lambda x: x[1])
  aligned_features = {}
  

  for i, feature in enumerate(sorted_features):
    mass_to_charge, intensities = feature
    
    if i == 0:
      aligned_features[mass_to_charge] = intensities
    else:
      prev_mass_to_charge, prev_intensities = list(aligned_features.items())[-1]
      
      diff = mass_to_charge - prev_mass_to_charge
     
      if abs(diff) <= accuracy:
        aligned_features[mass_to_charge] = intensities
      else:
       
        aligned_mass_to_charge = prev_mass_to_charge + np.sign(diff) * accuracy
        aligned_features[aligned_mass_to_charge] = intensities
  

  df = pd.DataFrame.from_dict(aligned_features, orient='index', columns=range(num_scans))
  
  df.index.name = 'm/z'
  
  df = df.fillna(value=np.nan)
  
  df['mean m/z'] = df.mean(axis=1)
  
  df = df[['mean m/z'] + [col for col in df.columns if col != 'mean m/z']]
  
  return df


import time

starttime = time.process_time()
testXX = dbdi.align_spectra(spectrums)
elapsed = time.process_time() - starttime
print(elapsed)   ##7.24 sec


