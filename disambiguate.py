from __future__ import division
from numpy import ceil
import logging

def beta_from_As(As):
    """find beta given the stopband attenuation (in dB)

    This is a standard formula."""
    if As>50:
        return 0.1102*(As-8.7)
    else if As>21:
        return 0.5842*(As-21)**0.4 + 0.07886*(As-21)
    else:
        return 0.0

def disambiguate_params(As=None, N=None, df=None, beta=None):
    """disambiguate the parameters passed to the resampler.

    We need two parameters to specify the window, but the ones we
    need to calculate it are not the natural ones we might want to
    specify.  So, we need to figure out N and beta from the parmeters
    given: beta is directly related to the stopband attenuation, but
    the window lenght is a function of the transition band width and the
    stopband attenuation.
    
    If beta and As (the stopband attenuation in dB) are given, As is used.
    If neither is given, assume As = 60 dB.
    
    If N is not given, we can compute it from a desired transition band
    width (and the stopband attenuation), else we use a default of
    32001 samples.
    
    There is one edge case which rare, but is handled first: beta can be
    derived (via As) if N and df ONLY are given.
    """
    default_N = 32001
    default_As = 60
    
    if beta is None:
        if As is None:
            if N is not None and df is not None:
                As = 14.36*df*N + 7.95
            else As = default_As
            beta = beta_from_As(As)
    else if As is not None:
        logging.warning('Both beta and the stopband attenuation specified. Stopband attenuation used.')
        beta = beta_from_As(As)

    assert(beta is not None)
    assert(As is not None)

    if N is None:
        if df is not None:
            N = ceil((As-7.95)/14.36*df)
        else N = default_N

    return N, beta
