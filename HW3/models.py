from __future__ import division
import sys, random, math, datetime, time,re
sys.dont_write_bytecode = True

exp = math.e
sqrt = math.sqrt

class Model:

  def name(i):
    return i.__class__.__name__
  
  def generate_x(i):  
    x= [i.lo + (i.hi-i.lo)*random.random() for _ in range(i.n)]  
    return x
  # def genDepen(i):
  #   return [ for x in i.]
  def score(i,xlst):
    return (i.f1(xlst) + i.f2(xlst))
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
      temp = i.norm(i.score(solution))
      if temp < temp_min:
        temp_min = temp
#   print "new solution : %s" % solution
    return solution
    

  def baseline(i):
  # model = eval(model+"()")
    i.min = 10**(5)
    i.max = -10**(5)
    for _ in xrange(100000):
      temp = i.score(i.generate_x())
      if temp > i.max:
        i.max = temp
      if temp < i.min:
	    i.min = temp
    return i.min, i.max
  
  def norm(i, x):
  	e = (x - i.min)/(i.max - i.min)
  	return max(0, min(e,1)) #avoid values <0 or >1


class Schaffer(Model):
  def __init__(i):
    i.lo = -2
    i.hi = 2
    i.n = 1
  def f1(i, x):
    return x[0] * x[0]
  def f2(i, x):
    return (x[0]-2) ** 2

  def f1_plus_f2(i, x_list):
    # x = i.generate_x()
    for item in x_list:
      f1 = item ** 2
      f2 = (item-2) **2
    return f1 + f2


class Fonseca(Model):
  def __init__(i):
    i.lo = -4
    i.hi = 4
    i.n = 3
  def f1(i, xlst):
    return (1 - exp**(-1 * sum([(xlst[k] - 1/sqrt(i.n))**2 for k in xrange(i.n)])))
  def f2(i, xlst):
    return (1 - exp**(-1 * sum([(xlst[k] + 1/sqrt(i.n))**2 for k in xrange(i.n)])))

  
  # def f1_plus_f2(i, x_list):
  #   n = i.n
  #   def f1_sum(x_list, n):
  #     value = []
  #     for item in x_list:
  #       value.append((item - 1/math.sqrt(n))**2)
  #     return sum(value)

  #   def f2_sum(x_list, n):
  #     value = []
  #     for item in x_list:
  #       value.append((item + 1/math.sqrt(n))**2)
  #     return sum(value)  

  #   f1 = 1 - math.e ** (-1* f1_sum(x_list, n))
  #   f2 = 1 - math.e ** (-1* f2_sum(x_list, n))
  #   return f1+f2
    
'''kusarvs'''
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
    return sum([abs(x)**a + 5*math.sin(x)**b for x in xlst]) 
  # def f1_plus_f2(i, x_list):
  #   n = i.n  
  #   def f1_inner(x_list, n):
  #     value = []
  #     for i in range(n-1):
  #       value.append(-10 * math.e **(-0.2 * math.sqrt(x_list[i]**2 + x_list[i+1]**2)))
  #     return value
    
  #   def f2_inner(x_list, n):
  #     value = []
  #     a = 0.8
  #     b = 3
  #     for item in x_list:
  #       value.append(abs(item)**a + 5 * math.sin(item)**b )
  #     return value
  #   f1 = sum(f1_inner(x_list, n))
  #   f2 = sum(f2_inner(x_list, n))
  #   return f1+f2

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

  # def f1_plus_f2(i, x_list):
  #   def f1(x_list):
  #     return x_list[0]
  #   def g(x_list):
  #     val = 0
  #     for item in x_list[1:]:
  #       val += item
  #     return 1+ 9*(val)/(i.n-1)
  #   def f2(x_list):
  #     g1 = g(x_list)
  #     return  g1* (1 - math.sqrt(x_list[0]/g1))  
  #   return f1(x_list)+f2(x_list)



