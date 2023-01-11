def align_spectra_b(spec, ppm_window = 2):
    
    """beta version of DBDIpy.align_spectra() with optimized runtime.
    Tests pending.
    
    """
    
    import matchms
    import numpy as np
    import pandas as pd
    from tqdm import tqdm
    
    if not isinstance(spec[0], matchms.Spectrum):
        raise TypeError("Argument for spec should be a list of matchms.Spectrum.")
        
    n_peaks = sum([len(s.peaks.mz) for s in spec])
    
    aldf = pd.DataFrame({"mean": np.zeros(n_peaks), "scan1": np.zeros(n_peaks)})
    
    massdf = pd.DataFrame({"scan1": np.zeros(n_peaks)})
    
    peak_count = 0
    
    for s in tqdm(range(1, len(spec)), desc = 'progress'):
        scan_s = spec[s]
        mz_s, scan_s_int = scan_s.peaks.mz, scan_s.peaks.intensities
        aldf_mz_mask = (aldf["mean"][peak_count:peak_count+len(mz_s)] >= mz_s[:, np.newaxis] - ppm_window * 1e-6) & (aldf["mean"][peak_count:peak_count+len(mz_s)] <= mz_s[:, np.newaxis] + ppm_window * 1e-6)
        idx = np.argmin(np.abs(aldf["mean"][peak_count:peak_count+len(mz_s)][aldf_mz_mask] - mz_s[:, np.newaxis][aldf_mz_mask]), axis=1)
        idx += peak_count
        aldf.iloc[idx, s+1] = scan_s_int
        massdf.iloc[idx, s+1] = mz_s
        peak_count += len(mz_s)
    
    return aldf, massdf
