from __future__ import division
import sys, random, math
from models import *
from base import *
import numpy as np
from xtile import *
sys.dont_write_bytecode = True


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
  icontrol = Control(model)
  while k < Settings.sa.kmax:
    stopsign = icontrol.next(k) #true ---stop
    if stopsign:
      break
    sn = model.sa_neighbor(s)
    en = model.norm(model.getDepen(sn))
    icontrol.logxy(sn)
    temp = (k/Settings.sa.kmax)*Settings.sa.cooling
    if en < eb:
	  sb = sn
	  eb = en 
	  say('!')
    if en < e:
      s = sn
      e = en
      say('+')
    elif P(e, en, temp) < random.random():
      s = sn
      e = en
      say('?')
    say('.')
    k = k + 1
    if k % 50 == 0:
      print "\n"  
      say(str(round(eb,3)))
  print "\n"
  printReport(model)
  print "\n------\n:e",str(round(eb,3)),"\n:solution",sn
  return eb
#   
@printlook
def mws(model):

  min_energy, max_energy = model.baseline()
  total_changes = 0
  total_tries = 0
  norm_energy = 0
  eraScore = []
  control = Control(model)
  optimalsign = False
  solution = model.generate_x()
  norm_energy = model.norm(model.getDepen(solution))
  for k in range(Settings.mws.max_tries):
    total_tries += 1
    for _ in range(Settings.mws.max_changes):
      stopsign = control.next(total_changes) #true ---stop
      if stopsign:
        break
      if norm_energy <= Settings.mws.threshold:
        optimalsign = True
        break
      if  random.random()<=Settings.mws.prob:
        solution[random.randint(0,model.n-1)] = model.generate_x()[random.randint(0,model.n-1)]
        control.logxy(solution)
        say("+")
      else:
        solution = model.mws_neighbor(solution)
        control.logxy(solution)
        say("!")
      say(".")
      if total_changes % 50 == 0:
        print "\n"
        say(str(round(model.norm(model.getDepen(solution)), 3))) 
      total_changes +=1   
    if optimalsign or k == Settings.mws.max_tries-1:
      pdb.set_trace()
      say("\n")
      say(str(round(model.norm(model.getDepen(solution)), 3))) 
      print "\n"
      print "total tries: %s" % total_tries
      print "total changes: %s" % total_changes
      print "min_energy:{0}, max_energy:{1}".format(min_energy, max_energy)
      print "min_energy_obtained: %s" % model.getDepen(solution)
      printReport(model)
      print "\n------\n:e",str(round(norm_energy,3)),"\n:solution",solution, "\n"    
      return norm_energy


def printReport(m):
  for i, f in enumerate(m.log.y):
    print "\n <f %s" %i
    for era in sorted(m.history.keys()):
      # pdb.set_trace()
      log = m.history[era].log.y[i]
      print str(era).rjust(7), xtile(log._cache, width = 33, show = "%5.2f", lo = 0, hi = 1)

@demo    
def start():
  r = 1
  #for klass in [Schaffer, Fonseca, Kursawe, ZDT1]:
  for klass in [ZDT1]:
    print "\n !!!!", klass.__name__
    for searcher in [sa, mws]:
      name = searcher.__name__
      n = 0.0
      reseed()
      scorelist = []
      for _ in range(r):
        name, x =searcher(klass())
        print "xsssss %f" %x 
        n += float(x)
        scorelist +=[float(x)]
      print xtile(scorelist,lo=0, hi=1.0,width = 25)
      print "# {0}:{1}".format(name, n/r)
@demo
def testmodel():
  # model = ZDT3()
  model = Schaffer()
  depen = model.getDepen(model.generate_x())
  print depen

if __name__ == "__main__": eval(cmd())










