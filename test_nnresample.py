from nnresample import compute_filt, resample
from disambiguate import beta_from_As, As_from_beta, disambiguate_params
from numpy import isclose

def test_beta_from_As():
    assert(isclose(beta_from_As(60), 5.65326))
    assert(isclose(beta_from_As(30), 2.11662))
    assert(isclose(beta_from_As(20), 0))

def test_As_from_beta():
    assert(isclose(60, As_from_beta(beta_from_As(60))))
    assert(isclose(30, As_from_beta(beta_from_As(30))))
    assert(isclose(25, As_from_beta(beta_from_As(25))))
    
def test_disambiguate_params_default():
    N, beta, As = disambiguate_params()
    assert(N==32001)
    assert(isclose(beta, 5.65326))
    assert(isclose(As, 60))

def test_disambiguate_params_given_As():
    N, beta, As = disambiguate_params(As=70)
    assert(N==32001)
    assert(isclose(beta, 6.75526))
    assert(isclose(As, 70))

def test_compute_filt():
    assert(False)

def test_resample():
    assert(False)

