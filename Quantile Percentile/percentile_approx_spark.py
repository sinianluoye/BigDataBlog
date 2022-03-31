import bisect
import math

class Coord:
    
    def __init__(self, v, g, d) -> None:
        self.v = v
        self.g = g        
        self.d = d

    def __lt__(self, o):
        if isinstance(o, Coord):
            return self.v < o.v
        elif isinstance(o, int) or isinstance(o, float):
            return self.v < o
        raise f"can not compare Coord with {type(o)}"


class GKSequence:
    
    def __init__(self, eps:float) -> None:
        self.t:list[Coord] = []
        self.n = 0
        self.s = 0
        self.eps = eps
    
    def insert(self, v):
        self.n += 1
        idx = bisect.bisect_left(self.t, v)
        if idx == 0 or idx == self.s:
            self.t.insert(idx, Coord(v,1,0))
        else:
            self.t.insert(v,1, math.floor(2*self.eps*self.n))
        self.s += 1
        
    def quantile(self, phi):
        # r_min(i) = r_min(i-1) + g[i]
        # r_max(i) = r_min(i) + d[i]
        
        r = math.ceil(phi*self.n)
        r_min = 0
        r_max = 0
        target = self.eps * self.n
        for item in self.t:
            r_min += item.g
            r_max = r_min + item.d
            if r - r_min <= target and r_max - r <= target:
                return item.v
            
if __name__ == "__main__":
    s = GKSequence(0.0001)
    for i in range(1,100001):
        s.insert(i)
    print(s.quantile(0.99))