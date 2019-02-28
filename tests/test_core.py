import cosmicsense as cs

import numpy as np

def test_n_to_theta_desilets():
    out = cs.core.n_to_theta_desilets(1180., 1150.)
    shouldbe = 0.012796463706461009
    assert round(out, 5)==round(shouldbe, 5)
