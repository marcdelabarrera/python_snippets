import numpy as np
from scipy.optimize import RootResults, OptimizeResult



def minimize_scalar_vec(fun:callable, bracket:np.ndarray, tol=1e-10, maximize=False,
                        maxit:int=1000):
  '''
  Optimization of scalar function of one variable in a vectorized way.

  Parameters
  -------------
  f: callable
    Objective function.
    Scalar function that is vectorized (takes a vector and returns a vector) 
  bracket : array
    Lower and upper bounds of the minimization
  tol : float, optional
    Tolerance for termination
  maximize : bool, optional
    If set to True, it performs maximization instead of minimization

Returns
------------
x1 : array
    Argument of the optimization problem
f1 : array
    Value of the optimization problem

Examples
----------
>>> a = np.array([1,2,3])
>>> golden_search(lambda x: (x-a)**2, bracket=(-5,5))
(array([1., 2., 3.]), array([4.10494703e-23, 1.50038420e-21, 4.18049201e-21]))
  '''
  ALPHA1,ALPHA2=(3-np.sqrt(5))/2,(np.sqrt(5)-1)/2
  f = (lambda x: -fun(x)) if maximize else fun
  
  a, b = np.atleast_1d(bracket[0]),np.atleast_1d(bracket[1])

  if len(a)==1:
    a = np.ones_like(f(a))*a
  if len(b)==1:
    b = np.ones_like(f(b))*b
  
  d = b-a
  x1 = a+ALPHA1*d
  x2 = a+ALPHA2*d
  f1, f2 = f(x1), f(x2)
  xx = np.zeros_like(x1)
  d = ALPHA1*ALPHA2*d
  for it in range(maxit):
    d = d*ALPHA2
    i1 = f2>f1
    i2 = np.invert(i1)
    x2[i1] = x1[i1]
    x1[i1] = x1[i1]-d[i1]
    f2[i1] = f1[i1]
    x1[i2] = x2[i2]
    x2[i2] = x2[i2]+d[i2]
    f1[i2] = f2[i2]
    xx[i1] = x1[i1]
    xx[i2] = x2[i2]
    ff = f(xx)
    f1[i1] = ff[i1]
    f2[i2] = ff[i2]
    if np.max(d)<tol:
      break
  i = f2<f1
  x1[i] = x2[i]
  f1[i] = f2[i]
  if maximize:
    f1 = -f1
  return OptimizeResult(x=x1, 
                        success=True, fun = f1,
                        nit=it,
                        message='Optimization terminated successfully')



def root_scalar_vec(fun:callable, bracket:np.ndarray=None, tol:float=1e-10,maxit=1000):
    """
    Find a root of a scalar function in a vectorized way
        Parameters
    ----------
    f: callable
    bracket: 
    """
    a = np.atleast_1d(bracket[0])
    b = np.atleast_1d(bracket[1])
    if len(a)==1:
        a = np.ones_like(fun(a))*a
    if len(b)==1:
        b = np.ones_like(fun(b))*b
    ALPHA1,ALPHA2=(3-np.sqrt(5))/2,(np.sqrt(5)-1)/2    
    d=b-a
    x1=a+ALPHA1*d
    x2=a+ALPHA2*d
    f1=fun(x1)**2
    f2=fun(x2)**2
    xx=np.zeros_like(x1)
    d=ALPHA1*ALPHA2*d
    for it in range(maxit):
        d=d*ALPHA2
        if2bigger=f2>f1
        i1=np.asarray(if2bigger==1).nonzero()[0]
        i2=np.asarray(if2bigger==0).nonzero()[0]
        x2[i1]=x1[i1]
        x1[i1]=x1[i1]-d[i1]
        f2[i1]=f1[i1]
        x1[i2]=x2[i2]
        x2[i2]=x2[i2]+d[i2]
        f1[i2]=f2[i2]
        xx[i1]=x1[i1]
        xx[i2]=x2[i2]
        ff=fun(xx)**2
        f1[i1]=ff[i1]
        f2[i2]=ff[i2]
        if np.max(d)<tol:
          break
    i2less=np.asarray(f2<f1).nonzero()[0]
    x1[i2less]=x2[i2less]
    f1[i2less]=f2[i2less]
    if np.max(fun(x1)**2)>1e-10:
        print('Something went wrong')
        return RootResults(root=x1, iterations=it, function_calls=it, flag=1)
    return RootResults(root=x1, iterations=it, function_calls=it, flag=0)
