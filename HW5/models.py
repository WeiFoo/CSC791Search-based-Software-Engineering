from __future__ import division
from log import *
import sys, random, math, datetime, time,re, pdb
sys.dont_write_bytecode = True


exp = math.e
sqrt = math.sqrt
sin = math.sin
pi = math.pi

class Model:

  def name(i):
    return i.__class__.__name__
  def setup(i):
    i.xy = Options(x = [i.generate_x()], y = [i.f1, i.f2])
    i.log = Options(x = [ Num() for _ in range(i.n)], y = [ Num() for _ in range(i.fn)]) # hardcode 2
    i.history = {} # hold all logs for eras
  def generate_x(i):  
    x= [i.lo + (i.hi-i.lo)*random.random() for _ in range(i.n)]  
    return x
  def getDepen(i, xlst):
    # y = [i.f1, i.f2]
    return sum([f(xlst) for f in i.xy.y])
  def getDepenlst(i, xlst):
    return [f(xlst) for f in i.xy.y]
  def cloneModel(i): # from Dr.Menzies'
    return i.__class__()
  def logxy(i, x):
    for val, log in zip(x, i.log.x): log += val
    y = i.getDepenlst(x)
    for val, log in zip(y, i.log.y): log += val
  def better(news,olds): # from Dr.Menzies'
    def worsed():
      return  ((same     and not betterIqr) or 
               (not same and not betterMed))
    def bettered():
      return  not same and betterMed
    out = False
    for new,old in zip(news.log.y, olds.log.y):
      betterMed, same, betterIqr = new.better(old)
      # print betterMed, same, betterIqr
      # pdb.set_trace()
      if worsed()  : return False # never any worsed
      if bettered(): out= out or True # at least one bettered
    return out
  def sa_neighbor(i, old):  
    p = 1/i.n
    new = old
    for j in range(len(old)):
      if random.random() < p:
      	new_gen = i.generate_x()
        old[j] = new_gen[random.randint(0, i.n-1)]   
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

class Control(object): # based on Dr.Menzies' codes
  def __init__(i, model):
    i.kmax = Settings.sa.kmax
    i.era = Settings.other.era
    i.lives = Settings.other.lives
    i.logAll = {}
    i.model = model
  def __call__(i, k):
    i.next(k)
  def logxy(i, results):
    both = [i.model.history, i.logAll]
    for log in both:
      if not i.era in i.logAll:
        log[i.era] = i.model.cloneModel()
    for log in both:
      log[i.era].logxy(results)
  def checkimprove(i):
      if len(i.logAll) >= 2:
        current = i.era
        before = i.era - Settings.other.era
        currentLog = i.logAll[current]
        beforeLog = i.logAll[before]
        # pdb.set_trace()
        if not currentLog.better(beforeLog):
          pass
        else:
          i.lives += 1
  def next(i, k):  
    if k >= i.era:
      i.checkimprove()
      i.era +=Settings.other.era
      if i.lives == 0:
        return True
      else:
        i.lives -=1
        return False



'''Schaffer'''
class Schaffer(Model):
  def __init__(i):
    i.lo = -2
    i.hi = 2
    i.n = 1
    i.fn = 2
    i.setup()
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
    i.fn = 2
    i.setup()
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
    i.fn = 2
    i.setup()
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
    i.fn = 2
    i.setup()
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
    i.fn = 2
    i.setup()
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
    i.fn = 3
    i.setup1()
  def setup1(i):
    i.xy = Options(x = [i.generate_x()], y = [i.f1, i.f2, i.f3])
    i.log = Options(x = [ Num() for _ in range(i.n)], y = [ Num() for _ in range(i.fn)]) # hardcode 2
    i.history = {} # hold all logs for eras
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

'''DTLZ7'''
class DTLZ7(Model):
  def __init__(i):
    i.M = 4
    i.K = 20
    i.lo = 0
    i.hi = 1
    i.n = i.M + i.K -1
    i.fn = i.M
    i.setup()
  def fi(i, x): # the frist one is x[0]
    return x
  def fm(i):
    return (1 + i.g())*i.h()
  def g(i):
    return 1 + 9/i.xy.x[i.M-1] * sum(i.xy.x[:i.M-1]) 
  def h(i):
    return i.M - sum([(i.xy.y[k]/(1+i.g()))*(1+sin(3*pi*i.xy.y[k])) for k in range(i.M-1)]) # k = 0,...., M-2
  def setup(i):
    tempx = i.generate_x()
    tempy = [i.fi(k) for k in tempx[:-1]]
    tempy.append(i.fm)
    i.xy = Options(x = tempx, y = tempy)
    i.log = Options(x = [ Num() for _ in range(i.n)], y = [ Num() for _ in range(i.fn)]) 
    i.history = {} # hold all logs for eras
  def getDepen(i, xlst):
    # y = [i.f1, i.f2]
    pdb.set_trace()
    temp = i.fm()
    return sum(xlst[:i.M])+temp


