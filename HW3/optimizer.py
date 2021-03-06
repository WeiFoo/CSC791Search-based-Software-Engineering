from __future__ import division
import sys, random, math
from models import *
from base import *
import numpy as np
from xtile import *
sys.dont_write_bytecode = True

def atom(x):
  try : return int(x)
  except ValueError:
    try : return float(x)
    except ValueError : return x

def cmd(com="demo('-h')"):
  "Convert command line to a function call."
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring)
  def wrap(x): return "'%s'"%x if strp(x) else str(x)  
  words = map(wrap,map(atom,sys.argv[2:]))
  return sys.argv[1] + '(' + ','.join(words) + ')'

def demo(f=None,cache=[]):   
  def doc(d):
    return '# '+d.__doc__ if d.__doc__ else ""  
  if f == '-h':
    print '# sample demos'
    for n,d in enumerate(cache): 
      print '%3s) ' %(n+1),d.func_name,doc(d)
  elif f: 
    cache.append(f); 
  else:
    s='|'+'='*40 +'\n'
    for d in cache: 
      print '\n==|',d.func_name,s,doc(d),d()
  return f

@printlook      
def sa(model):
  def P(old, new, t):
    prob = math.e**((old - new)/t) 
    return prob 
  min_energy, max_energy = model.baseline()
  s = model.generate_x()
  e = model.norm(model.getDepen(s))
  sb = s
  eb = e
  k = 1
  while k < Settings.sa.kmax:
    sn = model.sa_neighbor(s)
    en = model.norm(model.getDepen(sn))
    if en < eb:
	  sb = sn
	  eb = en 
	  say('!')
    if en < e:
      s = sn
      e = en
      say('+')
    elif P(e, en, (k/Settings.sa.kmax)) < random.random():
      s = sn
      e = en
      say('?')
    say('.')
    k = k+1
    if k % 40 == 0: 
      print "\n"  
      say(str(round(eb,3)))
        
  # say(str(sb))
  print "\n------\n:e",str(round(eb,3)),"\n:solution",sn
  return eb
#   
@printlook
def mws(model):
  max_tries = 50
  max_changes = 2000
  min_energy, max_energy = model.baseline()
  threshold = 0.01
  total_changes = 0
  total_tries = 0
  norm_energy = 0
  p = 0.25
  for _ in range(Settings.mws.max_tries):
    total_tries += 1
    solution = model.generate_x()
    for _ in range(Settings.mws.max_changes):
      norm_energy = model.norm(model.getDepen(solution))
      if norm_energy <= Settings.mws.threshold:
        print "total tries: %s" % total_tries
        print "total changes: %s" % total_changes
        print "min_energy:{0}, max_energy:{1}".format(min_energy, max_energy)
        print "min_energy_obtained: %s" % model.getDepen(solution)
        print "\n------\n:e",str(round(norm_energy,3)),"\n:solution",solution
        return norm_energy
      if Settings.mws.prob < random.random():
        solution[random.randint(0,model.n-1)] = model.generate_x()[random.randint(0,model.n-1)]
        say.("+")
      else:
        # solution = optimal_neighbor(solution, model, min, max)
        solution = model.mws_neighbor(solution)
        say.("!")
      say.(".")
      total_changes +=1     
@demo    
def StartSearcher():
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
@demo
def testmodel():
  # model = ZDT3()
  model = Viennet3()
  depen = model.getDepen(model.generate_x())
  print depen

if __name__ == "__main__": eval(cmd())










