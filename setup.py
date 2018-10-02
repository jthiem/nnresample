from setuptools import setup, find_packages

setup(name='nnresample',
      version='0.2.4',
      description='A resampling function based on placing the first null on Nyquist (Null-on-Nyquist Resample)',
      url='https://github.com/jthiem/nnresample',
      author='Joachim Thiemann',
      author_email='Joachim.Thiemann@gmail.com',
      license='CC-BY 3.0',
      packages=find_packages(include=['nnresample']),
      install_requires=[
          'scipy>=0.18.0,<2.0.0'  # NumPy is a dependancy of SciPy
      ]
      )
