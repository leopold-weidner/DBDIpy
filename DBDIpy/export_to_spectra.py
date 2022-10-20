def export_to_spectra(df, mzcol = 0):
    
    """
    Splits a two-dimensional pd.DataFrames containing tabular, aligned mass spectrometric features 
    to a list of matchms.Spectrum objects for further processing or exporting to .mgf-files.
    
    Parameters
    ----------    
    df: A pd.DataFrames containing tabular mass spectrometric data. The first column (by default) contains mass to charge ratios,
        successive columns contain corresponting signal intensities of each mass spectrometric scan.
        
    mzcol: Position of the column containing m/z values. 
    
    
    Returns
    -------
    A a list of matchms.Spectrum objects for each mass spectrometric scan.
    
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