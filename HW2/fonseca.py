from __future__ import division
import sys, random, math
import numpy as np
sys.dont_write_bytecode = True


class fonseca:
  def __init__(i):
    i.lo = -4
    i.hi = 4
    i.n =3
  
  def generate_x(i):
    return [i.lo + (i.hi-i.lo)*random.random() for _ in range(3)]  

def generate_x():
  lo = -4
  hi = 4
  x_list = [lo + (hi-lo)*random.random() for _ in range(3)]
  return x_list 
   
def fonseca(x_list):
  n = 3
  def f1_sum(x_list, n):
    value = []
    for item in x_list:
      value.append((item - 1/math.sqrt(n))**2)
    return sum(value)
   
  def f2_sum(x_list, n):
    value = []
    for item in x_list:
      value.append((item + 1/math.sqrt(n))**2)
    return sum(value)  
  
  f1 = 1 - math.e ** (-1* f1_sum(x_list, n))
  f2 = 1 - math.e ** (-1* f2_sum(x_list, n))
  return f1+f2
  
def find_max_min(model):
  min = 10**(5)
  max = 10**(-5)
  for i in range(10000):
    temp = eval(model+'(generate_x())')
    if temp > max:
      max = temp
    if temp < min:
      min = temp
  return min, max

def energy(x, min, max):
  e = (fonseca(x) - min)/(max - min)
  return e

def neighbor(s):  
  lo = -4
  hi = 4
  for i in range(3):
    if random.random() <=0.3:
	  x_new = lo + (hi-lo)*random.random()
	  s[i] = x_new
  return s
      
def P(old, new, t):
  prob = math.e**((old - new)/t) 
  return prob    
      
def say(mark):
  sys.stdout.write(mark)
  sys.stdout.flush()
      
def sa():
  model = raw_input("Type fonseca or kursawe:")
  min, max = find_max_min(model)
#   print min, max
#   min, max = 0.98, 2.0
  s = generate_x()
  e = energy(s, min, max)
  sb = s
  eb = e
  k = 1
  kmax = 1000
  while k < kmax:
    sn = neighbor(s)
    en = energy(sn, min,max)
    if en < eb:
	  sb = sn
	  eb = en 
	  say('!')
    if en < e:
      s = sn
      e = en
      say('+')
    elif P(e, en, (k/kmax)) < random.random():
      s = sn
      e = en
      say('?')
    say('.')
    k = k+1
    if k % 50 == 0: 
      print "\n"
      say(str(eb))
  return sb
  




if __name__ == "__main__": sa()