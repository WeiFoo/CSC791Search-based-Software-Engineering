from __future__ import division
import sys, random, math
from sk import *
from sa import *
from mws import *
sys.dont_write_bytecode = True
@demo
def part345(): #part 5 with part 3 and part4 
  for klass in [Schaffer,Fonseca, Kursawe, ZDT1, ZDT3, Viennet3]:
    print "\n !!!!", klass.__name__
    for searcher in [sa, mws]:
      reseed()
      x, rrange=searcher(klass()) #rrange is a dic: key is range, value is the obj name
      for key in rrange.keys():
        print "# The range of objective "+ str(rrange[key])+" during %s repeats is %s " \
             % (Settings.other.repeats, str(key))  
@demo
def part6():
  def genvariants():
    Settings.sa.cooling = rand() # get variants of sa, mws
    Settings.mws.prob = rand()
    Settings.mws.max_changes = int(1000*rand())
  r = 20
  Settings.other.repeats = 1
  Settings.other.reportrange = False
  for klass in [ZDT1]:
    print "\n !!!!", klass.__name__
    for variant in range(1):
      genvariants()
      allEB = []
      searcher = { "sa": sa, "mws" :mws}
      for key in searcher.keys():
        lastera = []
        reseed()
        for _ in range(r):
          model = klass()
          x = searcher[key](model)
          lastera += [x]
        label = key + str(variant) 
        lastera.insert(0,label)
        allEB.append(lastera)
      rdivDemo(allEB) 
 
@demo
def testmodel():
  # model = ZDT3()
  model = Schaffer()
  depen = model.getDepen(model.generate_x())
  print depen

if __name__ == "__main__": eval(cmd())










