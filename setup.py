from setuptools import setup

setup(name='nnresample',
      version='0.1',
      description='A resampling function based on placing the first null on Nyquist (Null-on-Nyquist Resample)',
      url='https://github.com/jthiem/nnresample',
      author='Joachim Thiemann',
      author_email='Joachim.Thiemann@gmail.com',
      license='CC-BY 3.0',
      py_modules=['nnresample'],
      install_reuires=[
          'scipy>=0.18.0',
          'numpy'
      ],
      )
