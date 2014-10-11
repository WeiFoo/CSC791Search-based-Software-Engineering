from __future__ import division
import sys, random, math
from models import *
from sk import *
from sa import *
from mws import *
sys.dont_write_bytecode = True

@demo    
def part345(): #part 5 with part 3 and part4 
  r = 1
  for klass in [Schaffer,Fonseca, Kursawe, ZDT1, ZDT3, Viennet3]:
    print "\n !!!!", klass.__name__
    for searcher in [sa, mws]:
      reseed()
      for _ in range(r):
        x, rrange=searcher(klass()) #rrange is a dic: key is range, value is the name
      for key in rrange.keys():
        print "# The range of objective "+ str(rrange[key])+" during %s repeats is %s " \
             % (Settings.other.repeats, str(key))
      
@demo 
def part6():
  r = 20
  searchcount = 0
  Settings.other.repeats = 1
  for klass in [ZDT1]:
    print "\n !!!!", klass.__name__
    for variant in range(5):
      Settings.sa.cooling = rand() # get variants of sa, mws
      Settings.mws.prob = rand()
      Settings.mws.max_changes = int(1000*rand())
      allEB = []
      for searcher in [sa, mws]:
        lastera = []
        reseed()
        for _ in range(r):
          model = klass()
          x, lohi = searcher(model)
          lastera += [x]
        searchername = "mws" if searchcount else "sa"
        label = searchername + str(variant) 
        lastera.insert(0,label)
        allEB.append(lastera)
        rdivDemo(allEB) 
        searchcount += 1
      searchcount = 0 
 
@demo
def testmodel():
  # model = ZDT3()
  model = Schaffer()
  depen = model.getDepen(model.generate_x())
  print depen

if __name__ == "__main__": eval(cmd())










