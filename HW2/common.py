from __future__ import division
import sys, random, math
import numpy as np
sys.dont_write_bytecode = True

class common:
  def __init__(self):
    i = i
    
  def generate_x():
    return [i.lo + (i.hi-i.lo)*random.random() for _ in range(i.n)]  
    
  def find_max_min(i):
    print "sdfd"
    print i.lo
    min = 10**(5)
    max = -10**(5)
    for i in range(10000):
      print i.generate_x()
#       temp = i.fon(i.generate_x(i))
      if temp > max:
        max = temp
      if temp < min:
        min = temp
    return min, max  