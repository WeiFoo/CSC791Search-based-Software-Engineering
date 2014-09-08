from __future__ import division
import sys, random, math
import numpy as np
sys.dont_write_bytecode = True
# np.random.seed(0)
# random.seed(44)
def generate_x():
  lo = -4
  hi = 4
  x = []
  x =[lo + (hi-lo)*random.random() for _ in range(3)]
  return x

def neighbor(s):
  lo = -4
  hi = 4
  new = s + 1
  if new > hi:
    new = s-1
  return new


# def cal_schaffer(x):
#   f1 = x**2
#   f2 = (x - 2)**2
#   return f1+f2

# def squared_sum(x, n = 0):
#   print x
#   print n
#   if n < 0:
#   # for item in x:
#       # value += (item - 1/math.sqrt(abs(n))**2 
#   # elif n >= 0:
#   #   for item in x:
#   #     value += (item + 1/math.sqrt(abs(n))**2 
def f1_sum(x, n):
  value = []
  for item in x:
    value.append((item - 1/math.sqrt(abs(n))**2)
  # xx = sum(value)
  return 

def sdfsdf():
  return sdf 

def f2_sum(x, n):
  value = []
  for item in x:
    value.append((item + 1/math.sqrt(abs(n))**2)
  return sum(value)
  
def fonseca(x_list):
  n = 3
  f1 = 1 - math.e**(-1 * f1_sum(x_list, n))
  f2 = 1 - math.e**(-1 * f2_sum(x_list, n))
  return f1+f2

def find_max_min():
  current_min = 10**(10)
  current_max = 10**(-10)
  for i in range(100):
    temp = fonseca(generate_x())	
    if temp > current_max:
      current_max = temp
    if temp < current_min:
      current_min = temp
  # print current_max, current_min
  return current_min, current_max    

def energy(x, min, max):
  e = (cal_schaffer(x)- min) / (max - min)
  # print e
  return e

def P(old, new, t):
  x = math.e**(-1*(old - new )/t)
  return x

def say(mark):
  sys.stdout.write(mark)
  sys.stdout.flush()


def my_main():
  min, max = find_max_min()
  print min, max
  # s = generate_x()
  # e = energy(s, min, max)
  # sb = s
  # eb = e
  # k = 1
  # kmax = 1000
  # # emax = 0.0001
  # while k < kmax:
  #   sn = neighbor(s)
  #   en = energy(sn, min, max)
  #   if en < eb:
  #     sb = sn
  #     eb = en 
  #     say('!')
  #   if en < e:
  #     s = sn
  #     e = en
  #     say('+')
  #   elif P(e, en, k/kmax)> random.random(): 
  #     s = sn
  #     e = en
  #     say('?')
  #   say('.')
  #   k = k + 1
  #   if k % 30 == 0: 
  #      print "\n"
  #      say(str(round(sb,3)))
  # return sb

if __name__ == "__main__":my_main()

