import scipy.signal as sig
from math import gcd
import numpy as np

__version__ = '0.1.1'

# global cache of resamplers
_precomputed_filters = {}

def compute_filt(up, down, beta=5.0, L=32001):
    r"""
    Computes a filter to resample a signal from rate "down" to rate "up"
    
    Parameters
    ----------
    up : int
        The upsampling factor.
    down : int
        The downsampling factor.
    beta : float
        Beta factor for Kaiser window.  Determines tradeoff between
        stopband attenuation and transition band width
    L : int
        FIR filter order.  Determines stopband attenuation.  The higher
        the better, ath the cost of complexity.
        
    Returns
    -------
    filt : array
        The FIR filter coefficients
        
    Notes
    -----
    This function is to be used if you want to manage your own filters
    to be used with scipy.signal.resample_poly (use the `window=...`
    parameter).  WARNING: Some versions (at least 0.19.1) of scipy
    modify the passed filter, so make sure to make a copy beforehand:
    
    out = scipy.signal.resample_poly(in up, down, window=numpy.array(filt))
    """
    
    # Determine our up and down factors
    g = gcd(up, down)
    up = up//g
    down = down//g
    max_rate = max(up, down)

    sfact = np.sqrt(1+(beta/np.pi)**2)
            
    # generate first filter attempt: with 6dB attenuation at f_c.
    init_filt = sig.fir_filter_design.firwin(L, 1/max_rate, window=('kaiser', beta))
    
    # convert into frequency domain
    N_FFT = 2**19
    NBINS = N_FFT/2+1
    paddedfilt = np.zeros(N_FFT)
    paddedfilt[:L] = init_filt
    ffilt = np.fft.rfft(paddedfilt)
    
    # now find the minimum between f_c and f_c+sqrt(1+(beta/pi)^2)/L
    bot = int(np.floor(NBINS/max_rate))
    top = int(np.ceil(NBINS*(1/max_rate + 2*sfact/L)))
    firstnull = (np.argmin(np.abs(ffilt[bot:top])) + bot)/NBINS
    
    # generate the proper shifted filter
    return sig.fir_filter_design.firwin(L, -firstnull+2/max_rate, window=('kaiser', beta))
    
    
def resample(s, up, down, beta=5.0, L=16001, axis=0):
    r"""
    Resample a signal from rate "down" to rate "up"
    
    Parameters
    ----------
    x : array_like
        The data to be resampled.
    up : int
        The upsampling factor.
    down : int
        The downsampling factor.
    beta : float
        Beta factor for Kaiser window.  Determines tradeoff between
        stopband attenuation and transition band width
    L : int
        FIR filter order.  Determines stopband attenuation.  The higher
        the better, ath the cost of complexity.
    axis : int, optional
        The axis of `x` that is resampled. Default is 0.
        
    Returns
    -------
    resampled_x : array
        The resampled array.
        
    Notes
    -----
    The function keeps a global cache of filters, since they are
    determined entirely by up, down, beta, and L.  If a filter
    has previously been used it is looked up instead of being
    recomputed.
    """   
    
    # check if a resampling filter with the chosen parameters already exists
    params = (up, down, beta, L)
    if params in _precomputed_filters.keys():
        # if so, use it.
        filt = _precomputed_filters[params]
    else:
        # if not, generate filter, store it, use it
        filt = compute_filt(up, down, beta, L)
        _precomputed_filters[params] = filt
        
    return sig.resample_poly(s, up, down, window=np.array(filt), axis=axis)
