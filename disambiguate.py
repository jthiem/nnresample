from __future__ import division
from numpy import ceil

def beta_from_As(As):
    """find beta given the stopband attenuation (in dB)

    This is a standard formula."""
    if As>50:
        return 0.1102*(As-8.7)
    else if As>21:
        return 0.5842*(As-21)**0.4 + 0.07886*(As-21)
    else:
        return 0.0

def N_from_As_and_df(As, df):
    """estimate the N required to satisfy a given stopband
    attenuation (As, in dB) and transition band (df).
    
    Standard formula."""
    return ceil((As-7.95)/14.36*df)

def As_from_beta(beta):
    raise NotImplementedError()

def As_from_N_and_df(N, df):
    """Get stopband attenuation given N and transition band width.

    Derived from the standard way to estimate N from As and df."""
    return 14.36*df*N + 7.95

def disambiguate_params(As=None, N=None, df=None, beta=None):
    """disambiguate the parameters passed to the resampler.

    We need two parameters to specify the window, but the ones we
    need to calculate it are not the natural ones we might want to
    specify.  So, we need to figure out N and beta from the parmeters
    given - if more than 2 are given the priorities are N, As, delta
    f (df) and beta.  If one parameter (which is not N) is given, we
    use the default N=32001, if none (or only N) are given, we use
    As = 60 dB.
    
    The function returns N and beta.
    """
    default_N = 32001
    default_As = 60
    
    if N is not None:
        if As is not None:
            return N, beta_from_As(As)
        else if df is not None:
            return N, beta_from_As(As_from_N_and_df(N, df))
        else if beta is not None:
            return N, beta
        else:
            return N, beta_from_As(default_As)
    else if As is not None:
        if df is not None:
            N = N_from_As_and_df(As, df)
            return N, beta_from_As(As)
        else if beta is not None:
            N = N_from_As_and_beta(As, beta)
        else:
            return default_N, beta_from_As(As)
    else if df is not None:
        if beta is not None:
            # I have df and beta.
            return N_from_As_and_df(As_from_beta(beta), df), beta
        else:
            # I have only df
            return default_N, beta_from_As(As_from_N_and_df(default_N, df))
    else if beta is not None:
        # I have only beta
        return default_N, beta
    else:
        # No parameters given
        return default_N, beta_from_As(default_As)
