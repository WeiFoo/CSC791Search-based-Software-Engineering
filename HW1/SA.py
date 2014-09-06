from __future__ import division
import sys, random, math
import numpy as np
sys.dont_write_bytecode = True
# np.random.seed(0)
# random.seed(44)
def generate_x():
  lo = -100
  hi = 100
  new = lo + (hi-lo)*random.random()
  return new

def neighbor(s):
  lo = -100
  hi = 100
  new = s + 1
  if new > hi:
    new = s-1
  return new


def cal_schaffer(x):
  f1 = x**2
  f2 = (x - 2)**2
  return f1+f2

def find_max_min():
  current_min = 1000
  current_max = 0
  for i in range(1000):
    temp = cal_schaffer(generate_x())	
    if temp > current_max:
      current_max = temp
    if temp < current_min:
      current_min = temp
  print current_max, current_min
  return current_min, current_max    

def energy(x, min, max):
  e = (cal_schaffer(x)- min) / (max - min)
  # print e
  return e

def P(old, new, t):
  x = math.e**((old - new )/t)
#   print x
  return x

def say(mark):
  sys.stdout.write(mark)
  sys.stdout.flush()


def my_main():
  min, max = find_max_min()
#   print min, max
  min = 2
  max = 20402
  s = generate_x()
  e = energy(s, min, max)
  sb = s
  eb = e
  k = 1
  kmax = 1000
  # emax = 0.0001
  while k < kmax:
#     sn = neighbor(s)
    sn = generate_x()
    en = energy(sn, min, max)
    if en < eb:
      sb = sn
      eb = en 
      say('!')
    if en < e:
      s = sn
      e = en
      say('+')
    elif P(e, en, k/kmax)< random.random(): 
      s = sn
      e = en
      say('?')
    say('.')
    k = k + 1
    if k % 30 == 0: 
       print "\n"
       say(str(round(sb,3)))
  return sb

if __name__ == "__main__":my_main()

