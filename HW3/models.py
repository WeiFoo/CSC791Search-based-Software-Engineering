from __future__ import division
import sys, random, math, datetime, time,re
sys.dont_write_bytecode = True


exp = math.e
sqrt = math.sqrt
sin = math.sin
pi = math.pi

class Model:

  def name(i):
    return i.__class__.__name__
  
  def generate_x(i):  
    x= [i.lo + (i.hi-i.lo)*random.random() for _ in range(i.n)]  
    return x
  def getDepen(i, xlst):
    y = [i.f1, i.f2]
    return sum([f(xlst) for f in y])
  def sa_neighbor(i, old):  
    p = 1/i.n
    new = old
    for j in range(len(old)):
      if random.random() <=p:
      	new_gen = i.generate_x()
        old[j] = new_gen[0] 
    # print old    
    return old
  def mws_neighbor(i,solution):  
    optimized_index = random.randint(0, len(solution)-1)
    increment = (i.hi - i.lo)/10
    temp_min = 10*(5)
#   print "old solution : %s" % solution
    for _ in range(10):
      solution[optimized_index] = i.lo + increment
      temp = i.norm(i.getDepen(solution))
      if temp < temp_min:
        temp_min = temp
#   print "new solution : %s" % solution
    return solution
  def baseline(i):
  # model = eval(model+"()")
    i.min = 10**(5)
    i.max = -10**(5)
    for _ in xrange(100000):
      temp = i.getDepen(i.generate_x())
      if temp > i.max:
        i.max = temp
      if temp < i.min:
	    i.min = temp
    return i.min, i.max
  def norm(i, x):
  	e = (x - i.min)/(i.max - i.min)
  	return e #avoid values <0 or >1

'''Schaffer'''
class Schaffer(Model):
  def __init__(i):
    i.lo = -2
    i.hi = 2
    i.n = 1
  def f1(i, x):
    return x[0] * x[0]
  def f2(i, x):
    return (x[0]-2) ** 2

'''Fonseca'''
class Fonseca(Model):
  def __init__(i):
    i.lo = -4
    i.hi = 4
    i.n = 3
  def f1(i, xlst):
    return (1 - exp**(-1 * sum([(xlst[k] - 1/sqrt(i.n))**2 for k in xrange(i.n)])))
  def f2(i, xlst):
    return (1 - exp**(-1 * sum([(xlst[k] + 1/sqrt(i.n))**2 for k in xrange(i.n)])))
    
'''Kusarvs'''
class Kursawe(Model):
  def __init__(i):
    i.lo = -5
    i.hi = 5
    i.n = 3
  def f1(i, xlst):
    return sum([-10*exp**(-0.2 * sqrt(xlst[k]**2 + xlst[k+1]**2)) for k in xrange(i.n -1)])
  def f2(i, xlst):
    a = 0.8
    b = 3
    return sum([abs(x)**a + 5*sin(x)**b for x in xlst]) 

'''ZDT1'''
class ZDT1(Model):
  def __init__(i):
    i.lo = 0
    i.hi = 1
    i.n = 30
  def f1(i, xlst):
    return xlst[0]
  def g(i, xlst):
    return (1 + 9 * (sum(xlst[1:]))/(i.n-1))
  def f2(i,xlst):
    g1 = i.g(xlst)
    return g1*(1-sqrt(xlst[0]/g1))

'''ZDT3'''
class ZDT3(Model):
  def __init__(i):
    i.lo = 0
    i.hi = 1
    i.n = 30
  def f1(i, xlst):
    return xlst[0]
  def g(i, xlst):
    return (1 +  (9/(i.n-1)) * sum(xlst[1:]))
  def h(i,f1,g):
    return (1 - sqrt(f1/g) - f1/g) * sin(10 * pi * f1)
  def f2(i, xlst):
    return i.g(xlst) * i.h(i.f1(xlst),i.g(xlst)) 

'''Viennet3'''
class Viennet3(Model):
  def __init__(i):
    i.lo = -3
    i.hi = 3
    i.n = 2
  def f1(i, xlst):
    xy2 = xlst[0]**2 + xlst[1]**2
    return 0.5* (xy2) + sin(xy2)
  def f2(i, xlst):
    x = xlst[0]
    y = xlst[1]
    return ((3*x -2*y +4)**2/8 + (x-y+1)**2/27 + 15)
  def f3(i, xlst):
    xy2 = xlst[0]**2 + xlst[1]**2
    return (1/(xy2+1) - 1.1* exp**(-xy2))

