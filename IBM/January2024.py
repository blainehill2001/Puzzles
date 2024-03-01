from z3 import *
import numpy as np
from itertools import combinations



if __name__ == "__main__":
    results = set()
    s = Solver()
    g = np.array(IntVector("x", 4**2) , dtype=object).reshape((4,4))
    #horizontal eqns
    s += g[0,0]+g[0,1]-g[0,2]-g[0,3]==5
    s += g[1,0]+g[1,1]+g[1,2]-g[1,3]==10
    s += g[2,0]-g[2,1]+g[2,2]+g[2,3]==9
    s += g[3,0]-g[3,1]+g[3,2]-g[3,3]==0
    #vertical eqns
    s += g[0,0]+g[1,0]+g[2,0]-g[3,0]==17
    s += g[0,1]+g[1,1]-g[2,1]-g[3,1]==8
    s += g[0,2]-g[1,2]-g[2,2]+g[3,2]==11
    s += g[0,3]+g[1,3]+g[2,3]+g[3,3]==48
    s += [And(n>0, n<=16) for n in g.ravel()] # add value constraints
    s += Distinct([n for n in g.ravel()])

    def serialize(arr):
        return ",".join([str(n) for n in arr.ravel()])
    while s. check() == sat:
        m = s.model()
        evalu = np.vectorize(lambda x: m.evaluate(x).as_long())
        result = evalu(g)
        ser = serialize(result)
        results.add(ser)
        s += Or([g[i][j] != e for (i,j),e in np.ndenumerate(result)])

    print(len(results))

    for s in results:
        print(s)

    for (str1, str2) in list(combinations(results, 2)):
        list1 = str1.split(',')
        list2 = str2.split(',')
        are_different = all(x != y for x, y in zip(list1, list2))
        if are_different:
            print(f"\n\nThe numbers at each index for the following pair is different.\n{list1}\n{list2}")
        # else:
        #     print(f"The numbers at each index for the pairs {pair1} and {pair2} are not all different.")

