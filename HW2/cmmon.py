from __future__ import division
import sys, random, math
import numpy as np
sys.dont_write_bytecode = True

class common:
  def __init__(i):
    pass
    
  def generate_x(i):
    return [i.lo + (i.hi-i.lo)*random.random() for _ in range(i.n)]  
    
  def find_max_min():
    min = 10**(5)
    max = -10**(5)
    for i in range(10000):
      temp = eval(model+'(generate_x())')
      if temp > max:
        max = temp
      if temp < min:
        min = temp
    return min, max  