import unittest

from nnresample.nnresample import compute_filt, resample
from nnresample.utility import beta_from_As, As_from_beta, disambiguate_params
from numpy import sum, cumsum, exp, log, sin, linspace, isclose, zeros, pi

class NNResampleUnittest(unittest.TestCase):

    # test data
    t441 = linspace(0, 1, 44100)
    t480 = linspace(0, 1, 48000)
    ifreq441 = exp(linspace(log(100), log(20000), 22050))
    ifreq480 = exp(linspace(log(100), log(20000), 24000))
    refsig441 = zeros(44100)
    refsig480 = zeros(48000)
    refsig441[11025:33075] = sin(cumsum(ifreq441*2*pi/44100))
    refsig480[12000:36000] = sin(cumsum(ifreq480*2*pi/48000))

    def test_beta_from_As(self):
        self.assertAlmostEqual(beta_from_As(60), 5.65326, places=5)
        self.assertAlmostEqual(beta_from_As(30), 2.11662, places=5)
        self.assertAlmostEqual(beta_from_As(20), 0)

    def test_As_from_beta(self):
        self.assertAlmostEqual(60, As_from_beta(beta_from_As(60)), places=5)
        self.assertAlmostEqual(30, As_from_beta(beta_from_As(30)), places=5)
        self.assertAlmostEqual(25, As_from_beta(beta_from_As(25)), places=5)

    def test_disambiguate_params_default(self):
        N, beta, As = disambiguate_params()
        self.assertEqual(N, 32001)
        self.assertAlmostEqual(beta, 5.65326)
        self.assertAlmostEqual(As, 60)

    def test_disambiguate_params_given_As(self):
        N, beta, As = disambiguate_params(As=70)
        self.assertEqual(N, 32001)
        self.assertAlmostEqual(beta, 6.75526)
        self.assertAlmostEqual(As, 70)

    def test_compute_filt(self):
        f = compute_filt(3, 2, N=1001)
        self.assertEqual(f.shape[0], 1001)

    def test_compute_filt_invalid_arg(self):
        self.assertRaises(ValueError, compute_filt, 3, 2, fc='blah')

    def test_resample(self):
        out = resample(self.refsig441, 480, 441)
        diff = out - self.refsig480
        self.assertAlmostEqual(sum(diff**2)/len(diff), 0, places=2)

    def test_samerate(self):
        out = resample(self.refsig441, 441, 441)
        diff = out - self.refsig441
        self.assertAlmostEqual(sum(diff**2)/len(diff), 0)

if __name__ == '__main__':
    unittest.main()
