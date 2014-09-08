from __future__ import division
import sys, random, math
import numpy as np
sys.dont_write_bytecode = True

def generate_x():
  lo = -5
  hi = 5
  x_list = []
  x_list = [lo + (hi-lo)*random.random() for _ in range(3)]
#   print "x is : %s" %x_list
  return x_list
  
def mutate(x):
#    lo = -4
#    hi = 4
#    x_list = []
#    variable_new = lo + (hi-lo)*random.random()
#    random_index = random.randint(0,2)
#    x[random_index] = variable_new
   return x
def f1_inner(x_list, n):
  value = []
  for i in range(n-1):
    value.append(-10 * math.e **(-0.2 * math.sqrt(x_list[i]**2 + x_list[i+1]**2)))
  return value
   
def f2_inner(x_list, n):
  value = []
  a = 0.8
  b = 3
  for item in x_list:
    value.append(abs(item)**a + 5 * math.sin(item)**b )
  return value  
   
def kursawe(x_list):
  n = 3
  f1 = sum(f1_inner(x_list, n))
  f2 = sum(f2_inner(x_list, n))
#   print f1+f2
  return f1+f2
  
def find_max_min():
  min = 10**(5)
  max = 10**(-5)
  for i in range(10000):
    temp = kursawe(generate_x())
    if temp > max:
      max = temp
    if temp < min:
      min = temp
  return min, max

def energy(x, min, max):
  e = (kursawe(x) - min)/(max - min)
  return e

def neighbor(s):  
  lo = -5
  hi = 5
#   for i in range(3):
  if random.random() <=0.3:
    variable_new = lo + (hi-lo)*random.random()
#     s[1] = variable_new  
    random_index = random.randint(0,2)
    s[random_index] = variable_new
#     print s
  return s
  
    
def say(mark):
  sys.stdout.write(mark)
  # sys.stdout.flush()

def P(old, new, t):
  # say(str(old))
#   say(str(new))
  prob = math.e**(-1*(old - new)/t)-1 ### why the prob is greater than 1?????
  print prob+1.0
  return prob    
      
def my_main():
  min, max = find_max_min()
  print min, max
  s = generate_x()
#   print "s is %s" % s
  e = energy(s, min, max)
  sb = s
  eb = e
  print"eb is %s" % eb
  k = 1
  kmax = 1000
#   print e, s
  while k < kmax:
    sn = neighbor(s)
#     print "s is %s" % s
#     print "neighbor is %s" % sn
    en = energy(sn, min,max)
#     print "en is %s" % en
#     print "e is %s" % e
#     print "eb is %s" % eb
    if en < eb:
	  sb = sn
	  eb = en 
	  say('!')
    if en < e:
      s = sn
      e = en
      say('+')
    elif P(e, en, (k/kmax)) > random.random():
      s = sn
      e = en
      say('?')
    say('.')
    k = k+1
#     print k
    if k % 30 == 0: 
      print "\n"
#       say(str(sb))
#     print"eb is %s" % eb
  return sb
  




if __name__ == "__main__": my_main()