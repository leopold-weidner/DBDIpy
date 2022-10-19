def align_spectra(spec, ppm_window = 0.2):
    
    """
    Aligns a list of matchms.Spectra objects into two-dimensional tabular data containing m/z features.
    Utilizes data loaded by matchms.importing module and connects to matchMS (pre-)processing workflows.
    
    Parameters
    ----------    
    spec: Spectra imported by matchMS from mass spectrometric experiments (MS1) of instance matchms.Spectrum.
    
    ppm_window: Window for mass alignment in ppm. Default is 0.2.
    
    Returns
    -------
    A two-dimensional pd.DataFrames containing aligned mass spectrometric features.
    
    """
    
    import matchms
    from tqdm import tqdm
    import pandas as pd
    import numpy as np
    
    
    if not isinstance(spec[0], matchms.Spectrum):
        raise TypeError("Argument for spec should be a list of matchms.Spectrum.")
        
    aldf = pd.DataFrame({"mean": spec[0].peaks.mz, "scan1": spec[0].peaks.intensities})
    aldf = aldf.reset_index(drop = True)
    
    massdf = pd.DataFrame({"scan1": spec[0].peaks.mz})
    
    for s in tqdm(range(1, len(spec)), desc = 'progress'):                                                            ## s iterates over number oof spectra
                                                                                                                      ## p iterates over number of peaks in spectrum
        spec_s = pd.DataFrame({"mz_s": spec[s].peaks.mz, "scan_s": spec[s].peaks.intensities})   
                     ## peak is help df to locate values
        spec_s = spec_s.reset_index(drop = True)                                                                      ##hard intensity cutoff: RMOVE!!!

        aldf[f"scan{s+1}"] = np.nan
        massdf[f"scan{s+1}"] = np.nan
        
        for p in range(spec_s.shape[0]):
                                                                                                                      ##peak is subset of possible matches in aldf
            peak = aldf.loc[(aldf["mean"] >= spec_s.loc[p, "mz_s"] - ppm_window * 1e-6) & (aldf["mean"] <= spec_s.loc[p, "mz_s"] + ppm_window * 1e-6)]
            
            if peak.shape[0] == 0:                                                                                    ##case 1: add a new ferature
                aldf = pd.concat([aldf, pd.DataFrame(columns = aldf.columns, index = range(0,1))])                    ##add empty new row
                aldf = aldf.sort_values('mean')                                                                       ##reorder column
                aldf = aldf.reset_index(drop = True)                                                                  ##reset indices!
                aldf.loc[aldf.shape[0]-1, "mean"] = spec_s.loc[p, "mz_s"]                                             ##add m/z
                aldf.iloc[aldf.shape[0]-1, aldf.shape[1]-1] = spec_s.loc[p, "scan_s"]                                 ##add intensity in 
                
                massdf = pd.concat([massdf, pd.DataFrame(columns = massdf.columns, index = range(0,1))])              ##add empty new row to mass data frame                                                         
                massdf = massdf.reset_index(drop = True)                                                              ##reset indices!
                massdf.iloc[massdf.shape[0]-1,  massdf.shape[1]-1] = spec_s.loc[p, "mz_s"]                            ##add m/z
                      
            if peak.shape[0] == 1:                                                                                    ##case 2: existing feature
                 aldf.iloc[aldf["mean"].values == peak.iloc[0,0], aldf.shape[1] - 1] = spec_s.loc[p, "scan_s"]        ##add intensity
                 massdf.iloc[massdf["scan1"].values == peak.iloc[0,0], massdf.shape[1]-1] = spec_s.loc[p, "mz_s"]     ##add mass to mass df

            if peak.shape[0] > 1:                                                                                     ##case3: unambiguous features
                peak = peak.iloc[(peak['mean'] - spec_s.loc[p, "mz_s"]).abs().argsort()[:1]]                          ##find closest matching feature
                aldf.iloc[aldf["mean"].values == peak.iloc[0,0], aldf.shape[1] - 1] = spec_s.loc[p, "scan_s"]         ##add intensity
                massdf.iloc[massdf["scan1"].values == peak.iloc[0,0], massdf.shape[1]-1] = spec_s.loc[p, "mz_s"]      ##add mass to mass df          
                
        aldf = aldf.sort_values('mean')                                                                               ##reorder column
        aldf = aldf.reset_index(drop = True) 
        
        massdf["mean"] = massdf.mean(axis = 1, skipna = True)                                                         ##calculate mean mz for every feature                   
        massdf = massdf.sort_values('mean')                                                                           ##reorder column
        massdf = massdf.reset_index(drop = True) 
        
        aldf["mean"] = massdf["mean"]                                                                                 ##replace "static" mass with mean mass
              
    
    aldf = aldf.sort_values('mean')

    aldf = aldf.reset_index(drop = True)
    aldf.index = ["ID" + s for s in [str(x) for x in list(range(1, aldf.shape[0] + 1, 1))]]  
    
    return aldf    
