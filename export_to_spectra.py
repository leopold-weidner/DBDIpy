def export_to_spectra(df, mzcol = 0):
    
    """Builds a list of spectra from tabular data.
    Splits a two-dimensional pd.DataFrames containing aligned mass spectrometric features 
    to a list of matchms.Spectrum objects for further processing or exporting to .mgf-files.
    
    Parameters
    ----------    
    df : pd.DataFrame
         A DataFrame containing tabular mass spectrometric data. 
         The first column (by default) contains mass to charge ratios,
         successive columns contain corresponting signal intensities 
         of each mass spectrometric scan.
        
    mzcol : int, optional
            Position of the column containing m/z information of the features.
            Default is 0.
    
    Returns
    -------
    A a list containing a matchms.Spectrum object for each column of the input
    DataFrame except for the m/z column.
    
    See Also
    --------
    matchms.exporting : For information about writing mass spectrometric data
    to open file formats.
    
    """
    
    import matchms
    
    df.rename(columns = {df.columns[mzcol]: 'mean'}, inplace = True)
    
    df = df.sort_values('mean')
    
    speclist = []    
    
    for s in range(0,df.shape[1]):
        
        if s == mzcol:                                                         ##skip column with mz values
            continue
        
        spec_s = df.iloc[:,[mzcol,s]].copy()
        spec_s = spec_s.dropna()
        spec_s = spec_s.reset_index(drop = True)
        
        spec_s = matchms.Spectrum(mz = spec_s.iloc[:,0].to_numpy(dtype = float), 
                                  intensities = spec_s.iloc[:,1].to_numpy(dtype = float))
        
        speclist.append(spec_s)
  
    return speclist