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
@printlook
def part6():
  def genvariants(i):
    Settings.sa.cooling =[0.9, 0.85, 0.8, 0.75, 0.7][i] # get variants of sa, mws
    Settings.mws.prob = [0.15,0.35, 0.5, 0.75, 0.95][i]
    Settings.mws.max_changes = int(1000*rand())
  r = 20
  Settings.other.repeats = 1
  Settings.other.reportrange = False
  for klass in [ZDT1]:
    print "\n !!!!", klass.__name__
    for variant in range(5):
      ShowDate = datetime.datetime.now().strftime
      print "#", ShowDate("%Y-%m-%d %H:%M:%S")
      beginTime = time.time()
      genvariants(variant)
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
      dump(Settings,lvl = 0)
      rdivDemo(allEB)
      endTime = time.time()
      print "\n" +("-"*60)
      # dump(Settings, f.__name__)
      print "\n# Runtime: %.3f secs" % (endTime-beginTime)
      print "\n" +("-"*60)
      print "\n"

@demo
def testmodel():
  # model = ZDT3()
  model = Schaffer()
  depen = model.getDepen(model.generate_x())
  print depen

if __name__ == "__main__": eval(cmd())










