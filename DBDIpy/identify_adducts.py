def identify_adducts(df, masses, custom_adducts = None, method = "spearman", threshold = 0.90, mass_error = 2):
    
    """Finds different ion species of a single analyte molecule. 
    Computes pointwise correlation of XIC traces to identify in-source adducts or in-source fragments
    generated during direct infusion mass spectrometric data aquisition. 
    Putative identification of adducts and fragments is based on a correlation threshold and mass differences. 
    
    Parameters
    ----------    
    df : pd.DataFrame
         A DataFrame of equal-length ion traces formated as rows.
         Input DataFrame can be provided by align_spectra() and impute_intensities().
    
    masses : pd.series 
             A series of m/z values for specification of adduct or fragment types. 
            Use of theoretic masses is strongly recommended for higher precission.
            If theoretic masses are not available, adapt mass_error 
            in accordance to the type of your mass analyzer.
        
    adduct_rules : pd.DataFrame, optional
                  The function searches for 1-Oxygen and 2-Oxygen adducts 
                  and in-source water-losses by default. 
                  Custom adduct rules need to be specified in a DataFrame as following:
                  custom_adducts = pd.DataFrame({'deltamz': [mz1, mz2, mz3],
                                                 'motive': ["motive1", "motive2", "motive3"]}). 
    
    method : str, {‘spearman’, 'pearson’, ‘kendall’}
            Correlation method for pointwise compariation of XIC traces. 
            
    threshold : float
                Correlation treshold to associate two ions. Default is 0.9.
               
    mass_error : int or float
                 Tolerance of the mass spectrometer in ppm. Default is 2 ppm. 
    
    Returns
    -------
    A dictionary of DataFrames containing pairwise information about correlation of XIC traces and 
    putatively identified in-source adducts or in-source fragments.
    
    
    Raises
    ------
    ValueError
        If the input DataFrame contains missing values.
        
    See Also
    --------
    align_spectra(), impute_intensities() : For preparation of the input data.
    
    """
#%%library import 
    import pandas as pd
    from tqdm import tqdm
    
#%%check if user imput is valid
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Argument for df should be of instance pandas.DataFrame.")  
        
    if df.isnull().values.any():
        raise ValueError("Input DataFrame contains missing values.")
    
    if masses.size != df.shape[0]:
        raise ValueError("Incompatible dimensions of mass list and number of XIC.")
        
#%%correlation matrix calculation            
    cormat = df.T.corr(method = method)
    
#%%set up adduct rules   
    massdifflib = pd.DataFrame({'deltamz': [15.994915, 31.98983, 18.010565],
                                 'motive': ["O", "O2", "H2O"]})
     
    if custom_adducts is not None: 
         if not isinstance(custom_adducts, pd.DataFrame):
             raise TypeError("Wrong format for custom adduct rules.")
     
         if list(massdifflib.columns) == list(custom_adducts.columns):
             massdifflib = pd.concat([massdifflib, custom_adducts])
             massdifflib = massdifflib.reset_index(drop = True) 
             
         else:
             raise TypeError("Wrong format for custom adduct rules. See documentation for example.")
             
    massdifflib["mass_upper"] = massdifflib["deltamz"] + massdifflib["deltamz"] * mass_error * 1e-6 
    massdifflib["mass_lower"] = massdifflib["deltamz"] - massdifflib["deltamz"] * mass_error * 1e-6 

#%%refine correlations by mass differences
    res_internal = pd.DataFrame({"base_mz": [], "base_index": [], "match_mz": [],
                             "match_index": [], "mzdiff": [],"corr": []})
     
    for i in tqdm(range(len(cormat)), desc='progress'):

        featnow = cormat.iloc[:,i]                                                      
        featnow = featnow[(featnow > threshold) & (featnow < 1)]     
    
        mzi = masses[i]                                        
        mz_matches = masses[featnow.index]                          
        mz_diff = abs(mz_matches - mzi)                                            
    
    
        for j in range(len(featnow)):
        
            res_internal.loc[len(res_internal)] = [masses[i], i, masses[featnow.index[j]],
                                                   featnow.index[j], mz_diff.values[j],
                                                   featnow.values[j]]
     
#%%extract different adduct types to lists
    reslist = {}   

    for a in range(massdifflib.shape[0]):
        
        dfnow = res_internal.loc[(res_internal["mzdiff"] >= massdifflib.loc[a, "mass_lower"]) &
                                 (res_internal["mzdiff"] <= massdifflib.loc[a, "mass_upper"])]
        
        reslist[massdifflib.loc[a, "motive"]] = dfnow
        
    return reslist
