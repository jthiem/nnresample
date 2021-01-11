from setuptools import setup, find_packages
# read the version information from nnresample/__init__.py
from nnresample import __version__ as nnresample_version

setup(name='nnresample',
      version=nnresample_version,
      description='A resampling function based on placing the first null on Nyquist (Null-on-Nyquist Resample)',
      url='https://github.com/jthiem/nnresample',
      author='Joachim Thiemann',
      author_email='Joachim.Thiemann@gmail.com',
      license='MIT',
      packages=find_packages(include=['nnresample']),
      install_requires=[
          'scipy>=0.18.0,<2.0.0'  # NumPy is a dependancy of SciPy
      ]
      )
