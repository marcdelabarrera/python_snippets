import optimize_vec
import numpy as np

def test_a():
    a=np.array([1,2])
    assert np.all(optimize_vec.minimize_scalar_vec(lambda x:(x-a)**2,bracket=[-10,1]).x==a)

