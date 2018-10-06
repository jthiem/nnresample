"""A resampling function based on placing the first null on Nyquist
   (Null-on-Nyquist Resample)
"""

__version__ = "0.2.4.dev0"

__all__ = ["resample", "compute_filt"]

from .nnresample import resample, compute_filt
