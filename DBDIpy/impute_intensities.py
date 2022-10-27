def impute_intensities(df, method = "linear"):
    
    """Fills nan values in data tables.
    Imputes NaN values contained in a DataFrame consisting of aligned mass spectra.
    Input DataFrame can be provided by align_spectra().
    
    Extracted Ion Chromatograms often are not of the same length. To generate a set of 
    uniform-length ion intensity series, a multi-step imputation approach is used:
        I)  Missing values within the detected signal region are interpolated.
        II) A noisy baseline is added for all XIC to be of uniform length which 
            the length of the longest XIC in the dataset.
    The returned DataFrame is suitable for time series analysis or other multivariate statistics.
    
    Parameters
    ----------    
    df : pd.DataFrame 
         A DataFrame containing missing (NaN) values to be imputed.
         Input DataFrame can be provided by align_spectra().
    
    method : str
            Intepolation method to be used; default is "linear". 
            Supported imputation methods are all  methods from 
            pandas.DataFrame.interpolate() and
            scipy.interpolate.interp1d().
    
    Returns
    -------
    A DataFrame of equal length ion intensity series without NaN.
    
    See Also
    --------
    align_spectra() : For preparation of the input data.
    
    
    """
    
    import math
    from tqdm import tqdm
    import random
    import pandas as pd
    import warnings
    
    ##check if user imput is valid
    if not isinstance(df, pd.DataFrame):
        raise TypeError('Argument for df should be of instance pandas.DataFrame.')
        
    if method not in ("linear", "time", "index", "pad", "nearest", "zero", "slinear", 
                      "quadratic", "cubic", "spline", "barycentric", "polynomial",
                      "krogh", "from_derivatives"):
        raise ValueError("Invalid imputation method.")
        
    if 'mean' in df.columns:
        warnings.warn("Possible bad composition of input. Check if DataFrames only is composed if XIC")
       
    ##define function for addition of a baseline 
    def baselinefill():
        s_min = v.min()
        fill_min = s_min - s_min * 0.01
        fill_max = s_min + s_min * 0.01  
        return round(random.uniform(fill_min, fill_max),2)
    
    ##fill the DataFrame row by row
    for i, v in tqdm(df.iterrows(), desc='progress'):                                    
        ##part 1: filling NaN within data region
        vnotNA = v.notna()                                           
        vnotNA[::1].idxmax()                                         
        vnotNA[::-1].idxmax()                                      
        datareg = v[vnotNA[::1].idxmax():vnotNA[::-1].idxmax()]       
        datareg = datareg.interpolate(method = method)                              
        v[vnotNA[::1].idxmax():vnotNA[::-1].idxmax()] = datareg     
        ##part : adding a baseline
        v[v.isna()] = v[v.isna()].apply(lambda x: baselinefill() if math.isnan(x) else x)
    
    ##fix all dtypes to float64    
    df = df.apply(lambda col:pd.to_numeric(col, errors = 'coerce'))

    return df
