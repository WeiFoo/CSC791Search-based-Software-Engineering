from __future__ import division
import sys, random, math
from models import *
from base import *
import numpy as np
from xtile import *
sys.dont_write_bytecode = True


# random.seed(1)

# class generate:
#   def __init__(i, lo, hi, n):
#     i.lo = lo
#     i.hi = hi
#     i.n = n
#   def generate_x(i):  
#     x= [i.lo + (i.hi-i.lo)*random.random() for _ in range(i.n)]  
#     return x

# class Schaffer(Model):
#   def __init__(i):
#     i.lo = -2
#     i.hi = 2
#     i.n = 1
#   def f1_plus_f2(i, x_list):
#     # x = i.generate_x()
#     for item in x_list:
#       f1 = item**2
#       f2 = (item-2)**2
#     return f1 + f2


# class Fonseca(Model):
#   def __init__(i):
#     i.lo = -4
#     i.hi = 4
#     i.n = 3
    
#   # def gen(i):
#   #   return generate(i.lo, i.hi,i.n)
    
#   def f1_plus_f2(i, x_list):
#     n = i.n
# #     print x_list
#     def f1_sum(x_list, n):
# 	  value = []
# 	  for item in x_list:
# 	    value.append((item - 1/math.sqrt(n))**2)
# 	  return sum(value)

#     def f2_sum(x_list, n):
# 	  value = []
# 	  for item in x_list:
# 	    value.append((item + 1/math.sqrt(n))**2)
# 	  return sum(value)  

#     f1 = 1 - math.e ** (-1* f1_sum(x_list, n))
#     f2 = 1 - math.e ** (-1* f2_sum(x_list, n))
# #     print f1+f2
#     return f1+f2
    
# '''kusarvs'''
# class Kursawe(Model):
#   def __init__(i):
#     i.lo = -5
#     i.hi = 5
#     i.n = 3
    
#   # def gen(i):
#   #   return generate(i.lo, i.hi, i.n)
    
#   def f1_plus_f2(i, x_list):
#     n = i.n  
#     def f1_inner(x_list, n):
#       value = []
#       for i in range(n-1):
#         value.append(-10 * math.e **(-0.2 * math.sqrt(x_list[i]**2 + x_list[i+1]**2)))
#       return value
    
#     def f2_inner(x_list, n):
# 	  value = []
# 	  a = 0.8
# 	  b = 3
# 	  for item in x_list:
# 		value.append(abs(item)**a + 5 * math.sin(item)**b )
# 	  return value
#     f1 = sum(f1_inner(x_list, n))
#     f2 = sum(f2_inner(x_list, n))
# 	#   print f1+f2
#     return f1+f2

# class ZDT1(Model):
#   def __init__(i):
#     i.lo = 0
#     i.hi = 1
#     i.n = 30

#   def f1_plus_f2(i, x_list):
#     def f1(x_list):
#       return x_list[0]
#     def g(x_list):
#       val = 0
#       for item in x_list[1:]:
#         val += item
#       return 1+ 9*(val)/(i.n-1)
#     def f2(x_list):
#       g1 = g(x_list)
#       return  g1* (1 - math.sqrt(x_list[0]/g1))  
#     return f1(x_list)+f2(x_list)




# '''hello'''
# def find_max_min(model, gen):
#   # model = eval(model+"()")
#   min = 10**(5)
#   max = -10**(5)
#   for i in range(100000):
#     temp = model.f1_plus_f2(gen.generate_x())
#     if temp > max:
#       max = temp
#     if temp < min:
# 	  min = temp
#   return min, max


# def energy(x, min, max):
#   e = (x - min)/(max - min)
#   return e
# 

# def neighbor(old, generator):  # can put in to generator
#   for i in range(len(old)):
#     if random.random() <=0.33:
#       old[i] = generator.generate_x()[i] 
#   return old
      
# def P(old, new, t):
#   prob = math.e**((old - new)/t) 
#   return prob    
      
# def say(mark):
#   sys.stdout.write(mark)
#   sys.stdout.flush()

@printlook      
def sa(model):
 #  model_str = raw_input("Type 1 for fonseca and 2 for kursawe:")
 #  if (model_str) == '1':
 #    model = fonseca()
 #  elif (model_str) == '2':
	# model = kursawe()
 #  else:
 #    print "please type 1 or 2!"
 #    exit()
#   model = ()
#   model = kursawe()
#   x = generate(model.lo, model.hi, model.n)
  def P(old, new, t):
    prob = math.e**((old - new)/t) 
    return prob 
  min_energy, max_energy = model.baseline()
  s = model.generate_x()
  e = model.norm(model.f1_plus_f2(s))
  sb = s
  eb = e
  k = 1
  # kmax = 1000
  while k < Settings.sa.kmax:
    # sn = neighbor(s, generator)
    sn = model.sa_neighbor(s)
    en = model.norm(model.f1_plus_f2(s))
    # en = energy(model.f1_plus_f2(sn), min,max)
    if en < eb:
	  sb = sn
	  eb = en 
	  # say('!')
    if en < e:
      s = sn
      e = en
      # say('+')
    elif P(e, en, (k/Settings.sa.kmax)) < random.random():
      s = sn
      e = en
      # say('?')
    # say('.')
    k = k+1
    if k % 40 == 0: 
      # print "s"
      say(str(round(eb,3)))
  # print "\n"    
#   say(str(sb))
  print "\n------\n:e",str(round(eb,3)),"\n:solution",sn
  return eb
#   
@printlook
def mws(model):
  max_tries = 50
  max_changes = 2000
  # model = fonseca()
  # generator = model.gen()
  # min, max = find_max_min(model, generator)
  min_energy, max_energy = model.baseline()
  threshold = 0.01
  total_changes = 0
  total_tries = 0
  norm_energy = 0
  p = 0.25
#   print threshold
#   
#   print solution
  for _ in range(Settings.mws.max_tries):
    total_tries += 1
    solution = model.generate_x()
#     print 'try {0} time(s) with solution {1}'.format( total_tries, solution)
    for _ in range(Settings.mws.max_changes):
      # final_score=score(model.f1_plus_f2(solution),min, max)
      norm_energy = model.norm(model.f1_plus_f2(solution))
#       print "final score: %s" % final_score
      if norm_energy <= Settings.mws.threshold:
        # print "p : %s" % p
        # print "threshold : %s" %threshold
        print "total tries: %s" % total_tries
        print "total changes: %s" % total_changes
        print "min_energy:{0}, max_energy:{1}".format(min_energy, max_energy)
        print "min_energy_obtained: %s" % model.f1_plus_f2(solution)
        # print "solution : %s" % solution
        # print "final_score: %s" % norm_energy
        print "\n------\n:e",str(round(norm_energy,3)),"\n:solution",solution
        return norm_energy
      if Settings.mws.prob < random.random():
        solution[random.randint(0,model.n-1)] = model.generate_x()[random.randint(0,model.n-1)]
      else:
        # solution = optimal_neighbor(solution, model, min, max)
        solution = model.mws_neighbor(solution)
      total_changes +=1     
    
#        c =  generator.generate_x() 
def Demo():
  r = 2
  for klass in [Schaffer, Fonseca, Kursawe, ZDT1]:
    print "\n !!!!", klass.__name__
    for searcher in [sa, mws]:
      name = searcher.__name__
      n = 0.0
      reseed()
      scorelist = []
      for _ in range(r):
        name, x =searcher(klass())
        n += float(x)
        scorelist +=[float(x)]
      print xtile(scorelist,lo=0, hi=1.0,width = 25)
      print "# {0}:{1}".format(name, n/r)
        






if __name__ == "__main__": Demo()