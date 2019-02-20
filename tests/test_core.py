import cosmicsense as cs

def test_n_to_theta():
    out = cs.core.n_to_theta(1000,100.,14, 1., 1., 1500., 1000.)
    shouldbe = 0.8333333333333334
    assert out==shouldbe
