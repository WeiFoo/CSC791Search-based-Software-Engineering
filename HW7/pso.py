from __future__ import division
from log import *
from models import *
from xtile import *
from base import *
import sys,random, math, pdb, operator
sys.dont_write_bytecode = True

@printlook 
def pso(model):
  vel = []
  pos = []
  lbest = [] # local best position for each 
  gbest = model.generate_x() # global best position for all
  eb = 0.0
  N = Settings.pso.N
  repeats = Settings.pso.repeats
  threshold = Settings.pso.threshold
  fitness =lambda x: model.norm(model.getDepen(x))  
  def init(gbest = gbest):
    for n in xrange(N):
      vel.append([0 for _ in xrange(model.n)])
      pos.extend([model.generate_x() for _ in xrange(model.n)])
      lbest.append(pos[n])
      if fitness(pos[n]) < fitness(gbest): #??why I should pass gbest
        gbest = pos[n]
        eb = fitness(gbest)
  init() # init all parameters
  print vel
  print lbest
  print gbest
  for k in xrange(repeats):
    if eb < threshold:
      break
    






  
def start():
  for klass in [Schaffer, Fonseca, Kursawe, ZDT1, ZDT3, Viennet3]:
  # for klass in [DTLZ7]:
    print "="*50
    print "!!!!", klass.__name__, 
    print "\nSearcher: GA"
    reseed()
    pso(klass())


if __name__ == "__main__":start()
     # print sortedFitness




    

