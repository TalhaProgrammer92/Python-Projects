from PyMisc.sets import *

if __name__ == '__main__':
    A: Set = Set()
    B: Set = Set()
    U: Set = Set()

    A.add(1, 3, 5, 7, 9)
    B.add(0, 3, 4, 7, 8)
    U.add(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    print(f'''
{'*'*20} Test {'*'*20}
Set A:  {A}
Set B:  {B}
Set U:  {U}

Union:          {CommonOperation.union(A, B)}
Intersect:      {CommonOperation.intersect(A, B)}
Difference:     {CommonOperation.difference(A, B)}

Complement A:   {AdvanceOperation.complement(A, U)}
Complement B:   {AdvanceOperation.complement(B, U)}
Symmetric:      {AdvanceOperation.symmetric_difference(A, B)}
''')
