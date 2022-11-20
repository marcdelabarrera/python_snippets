import sympy as sym

print('here')

print(sym.Eq(1, sym.Symbol('x')+2))

print(sym.Eq.__new__(sym.Eq, 1, sym.Symbol('x')+2))

print('Done')

sym.Rel('1','2')
