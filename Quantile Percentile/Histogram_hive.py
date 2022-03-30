from ast import While
import bisect
from tokenize import Double 


class Coord:

    def __init__(self, p, m) -> None:
        self.p = p
        self.m = m

    def __lt__(self, o) -> bool:
        if isinstance(o, Coord):
            return self.p < o.p
        elif isinstance(o, int):
            return self.p < o
        else:
            raise f"can not compare < between Coord and {type(o)}"

    def __eq__(self, o) -> bool:
        if isinstance(o, Coord):
            return self.p == o.p
        elif isinstance(o, int):
            return self.p == o
        else:
            raise f"can not compare == between Coord and {type(o)}"
    
    def inc(self):
        self.m += 1

class Histogram:

    # the histogram contains b bins
    def __init__(self, b:int) -> None:
        self.b = b
        self.h:list[Coord] = [Coord(0,0) for i in range(b)]
    
    def update(self, p):
        idx = bisect.bisect_left(self.h, p)
        if self.h[idx] == p:
            self.h[idx].inc()
        else:
            self.h.insert(idx, Coord(p, 1))
            self.trim()
    
    def merge(self, o):
        if not isinstance(o, Histogram):
            raise f"can not merge Histogram and {type(o)}"
        self.h.extend(o.h)
        self.h.sort()
        self.trim()

    def trim(self):
        diffs = None
        while len(self.h) > self.b:
            idx = 0
            min_diff = self.h[1].p-self.h[0].p
            for i in range(1,len(self.h)-1):
                cur_diff = self.h[i+1].p - self.h[i].p
                if cur_diff < min_diff:
                    min_diff = cur_diff
                    idx = i
            m = self.h[idx+1].m+self.h[idx].m
            if m != 0:
                p = self.h[idx+1].p*self.h[idx+1].m + self.h[idx].p*self.h[idx].m
            else:
                p = 0
            self.h[idx].p = p
            self.h[idx].m = m
            self.h.pop(idx+1)
            
            
                