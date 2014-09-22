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
  eraScore = []
  icontrol = Control(model)
  while k < Settings.sa.kmax:
    stopsign = icontrol.next(k) #true ---stop
    if stopsign:
      break
    sn = model.sa_neighbor(s)
    en = model.norm(model.getDepen(sn))
    icontrol.logxy(sn)
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
    eraScore += [eb] # keep score for xtile
    if k % 50 == 0:
      Settings.sa.score[int(k/50-1)] = eraScore
      eraScore = []
      print "\n"  
      say(str(round(eb,3)))
  print "\n"
  line = ' '*26+'='*31
  print ('%31s, %5s, %5s, %5s, %5s' % (' 10%', ' 30%', ' 50%', ' 70%', ' 90%'))+'\n'+line
  for key, scorelist in Settings.sa.score.items():
    print xtile(scorelist,lo=0, hi=1.0,width = 25)      
  # say(str(sb))
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
  k = 0
  for _ in range(Settings.mws.max_tries):
    total_tries += 1
    solution = model.generate_x()
    for _ in range(Settings.mws.max_changes):
      norm_energy = model.norm(model.getDepen(solution))
      if norm_energy <= Settings.mws.threshold:
        say("\n")
        say(str(round(model.norm(model.getDepen(solution)), 3))) 
        print "\n"
        print "total tries: %s" % total_tries
        print "total changes: %s" % total_changes
        print "min_energy:{0}, max_energy:{1}".format(min_energy, max_energy)
        print "min_energy_obtained: %s" % model.getDepen(solution)
        print "\n------\n:e",str(round(norm_energy,3)),"\n:solution",solution, "\n"
        line = ' '*26+'='*31
        print ('%31s, %5s, %5s, %5s, %5s' % (' 10%', ' 30%', ' 50%', ' 70%', ' 90%'))+'\n'+line
        for key, scorelist in Settings.sa.score.items():
          print xtile(scorelist,lo=0, hi=1.0,width = 25)      
        return norm_energy
      if Settings.mws.prob < random.random():
        solution[random.randint(0,model.n-1)] = model.generate_x()[random.randint(0,model.n-1)]
        say("+")
        eraScore += [str(round(model.norm(model.getDepen(solution)), 3))]
      else:
        # solution = optimal_neighbor(solution, model, min, max)
        solution = model.mws_neighbor(solution)
        say("!")
        eraScore += [str(round(model.norm(model.getDepen(solution)), 3))]
      say(".")
      if total_changes % 50 == 0:
        Settings.mws.score[k] = eraScore
        k +=1
        eraScore = []
        print "\n"
        say(str(round(model.norm(model.getDepen(solution)), 3))) 
      total_changes +=1     
@demo    
def start():
  r = 1
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
  model = Schaffer()
  depen = model.getDepen(model.generate_x())
  print depen

if __name__ == "__main__": eval(cmd())










