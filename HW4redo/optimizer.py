from __future__ import division
import sys, random, math
from models import *
from sk import *
from base import *
import numpy as np
from xtile import *
sys.dont_write_bytecode = True
@printlook      
def sa(model):
  def P(old, new, t):
    prob = math.e**((old - new)/(t+0.00001)) 
    return prob 
  history = {}
  for _ in xrange(Settings.other.repeats):
    #reseed()
    min_energy, max_energy = model.baseline()
    s = model.generate_x()
    e = model.norm(model.getDepen(s))
    sb = s[:]
    eb = e
    k = 1
    icontrol = Control(model, history)
    while k < Settings.sa.kmax:
      stopsign = icontrol.next(k) #true ---stop
      if stopsign:
        break
      sn = model.sa_neighbor(s)
      en = model.norm(model.getDepen(sn))
      icontrol.logxy(sn)
      temp = (k/Settings.sa.kmax)**Settings.sa.cooling
      if en < eb:
        sb = sn[:] ###!!!!! can't do sb = sn for lists, because
        eb = en
        if Settings.other.show: say('!')
      if en < e:
        s = sn[:]
        e = en
        if Settings.other.show:say('+')
      elif P(e, en, temp) < random.random():
        s = sn[:]
        e = en
        if Settings.other.show:say('?')
      if Settings.other.show:say('.')
      k = k + 1
      if k % 30 == 0:
        if Settings.other.show:print "\n"  
        if Settings.other.show:say(str(round(eb,3)))
  printReport(model, history)
  print "\n"
  printSumReport(model, history)
  # print "\n------\n:Normalized Sum of Objectives : ",str(round(eb,3)),"\n:Solution",sb
  lohi=printRange(model, history)
  return eb,lohi
#   
@printlook
def mws(model):
  norm_energy = 0
  eraScore = []
  control = Control(model)
  optimalsign = False
  eb = 0
  norm_energy = 10
  history = {}
  for _ in xrange(Settings.other.repeats):
    min_energy, max_energy = model.baseline()
    control = Control(model, history)
    total_changes = 0
    total_tries = 0
    for k in xrange(Settings.mws.max_tries):
      if control.lives ==0:
        break
      solution = model.generate_x()
      total_tries += 1
      for _ in range(Settings.mws.max_changes):
        stopsign = control.next(total_changes) #true ---stop
        if stopsign:
          break
        norm_energy = model.norm(model.getDepen(solution))
        if norm_energy < Settings.mws.threshold:
          optimalsign = True
          break
        if  random.random()<Settings.mws.prob:
          solution[random.randint(0,model.n-1)] = model.generate_x()[random.randint(0,model.n-1)]
          control.logxy(solution)
          if Settings.other.show:say("+")
        else:
          solution = model.mws_neighbor(solution)
          control.logxy(solution)
          if Settings.other.show:say("!")
        if Settings.other.show:say(".")
        if total_changes % 30 == 0:
          if Settings.other.show:print "\n"
          if Settings.other.show:say(str(round(model.norm(model.getDepen(solution)), 3))) 
        total_changes +=1   
    # if optimalsign or k == Settings.mws.max_tries-1:
  say("\n")
  say(str(round(model.norm(model.getDepen(solution)), 3))) 
  print "\n"
  # print "total tries: %s" % total_tries
  # print "total changes: %s" % total_changes
  # print "min_energy:{0}, max_energy:{1}".format(min_energy, max_energy)
  # print "min_energy_obtained: %s" % model.getDepen(solution)
  printReport(model, history)
  print "\n"
  printSumReport(model, history)
  lohi =printRange(model, history)
  # print "\n------\n:Normalized Sum of Objectives: ",str(round(norm_energy,3)),"\n:Solution",solution, "\n"    
  return norm_energy, lohi


def printReport(m, history):
  for i, f in enumerate(m.log.y):
    print "\n <f%s" %i
    for era in sorted(history.keys()):
      # pdb.set_trace()
      log = history[era].log.y[i]
      print str(era).rjust(7), xtile(log._cache, width = 33, show = "%5.2f", lo = 0, hi = 1)


def printSumReport(m, history):
  # for i, f in enumerate(m.log.y):
  print "\n Objective Value" 
  for era in sorted(history.keys()):
    # pdb.set_trace()
    log = [history[era].log.y[k] for k in range (len(m.log.y))]
    ss = []
    ss.extend([log[s]._cache for s in range(len(log))])
    logsum = map(sum, zip(*ss))
    minvalue = min(logsum)
    maxvalue = max(logsum)
    normlog = [(x - minvalue)/(maxvalue - minvalue) for x in logsum]
    print str(era).rjust(7), xtile(normlog, width = 33, show = "%5.2f", lo = 0, hi = 1)

def printRange(m, history):
  lo = []
  lohi = []
  # print sorted(m.history.keys())
  for i, f in enumerate(m.log.y):
    tlo=10**5
    thi=-10**5
    for era in sorted(history.keys()):
      # pdb.set_trace()
      if history[era].log.y[i].lo < tlo:
        tlo= history[era].log.y[i].lo
      if history[era].log.y[i].hi > tlo:
        thi= history[era].log.y[i].hi
    lohi.append(tlo)
    lohi.append(thi)
  return  lohi
    # print "\n the range of f%s is %s to %s " % (i, str(tlo), str(thi))

@demo    
def start(): #part 5 with part 3 and part4 
  r = 1
  rlohi=[] # stupid codes here, to be fixed
  f1lo = []
  f1hi = []
  f0lo = []
  f0hi =[]
  f2lo =[]
  f2hi =[]
  for klass in [Schaffer,Fonseca, Kursawe, ZDT1, ZDT3, Viennet3]:
  # for klass in [Kursawe]:
    print "\n !!!!", klass.__name__
    for searcher in [mws]:
      name = klass.__name__
      n = 0.0
      reseed()
      # scorelist = []
      for _ in range(r):
        x, lohi=searcher(klass()) # lohi is a list containing [lo,hi] paris of f1&f2 
       #========part 5==========
        rlohi.append(lohi)
      for i in range(0, r):
        f0lo.append(rlohi[i][0])
        f0hi.append(rlohi[i][1])
        f1lo.append(rlohi[i][2])
        f1hi.append(rlohi[i][3])
        if name == "Viennet3": # f1, f2, f3
          f2lo.append(rlohi[i][4])
          f2hi.append(rlohi[i][5])
      print "# The range of f0 during %s repeats is from %s to %s " \
             % (Settings.other.repeats, str(round(sorted(f0lo)[0], 3)), str( round(sorted(f0hi)[-1])))
      print "# The range of f1 during %s repeats is from %s to %s " \
             % (Settings.other.repeats, str(round(sorted(f1lo)[0],3)), str(round(sorted(f1hi)[-1])))
      if name =="Viennet3":
        print "# The range of f2 during %s repeats is from %s to %s "\
             % (Settings.other.repeats, str(round(sorted(f2lo)[0],3)), str(round(sorted(f2hi)[-1])))
      rlohi = []
      #=====part 5 ends===========

      #the following codes for hw3
      # n += float(x)
      # scorelist +=[float(x)]
      # print xtile(scorelist,lo=0, hi=1.0,width = 25)
      # print "# {0}:{1}".format(name, n/r)
@demo 
def part6():
  r = 5
  lastera = []
  searchcount = 0
  for klass in [ZDT1]:
    print "\n !!!!", klass.__name__
    for searcher in [sa, mws]:
      reseed()
      for k in range(r):
        Settings.sa.cooling = rand() # get variants of sa, mws
        Settings.mws.prob = rand()
        Settings.mws.max_changes = int(1000*rand())
        model = klass()
        x, lohi = searcher(model)
        for i, f in enumerate(model.log.y):
          temp = []
          searchername = "mws" if searchcount else "sa"
          label = searchername + str(k) +"f%s" %i
          temp = (model.history[sorted(model.history.keys())[-1]].log.y[i]._cache)
          temp = [ float(i) for i in temp]
          temp.insert(0,str(label))
          lastera.append(temp) 
      rdivDemo(lastera) 
      searchcount +=1  
      lastera = []     
@demo
def testmodel():
  # model = ZDT3()
  model = Schaffer()
  depen = model.getDepen(model.generate_x())
  print depen

if __name__ == "__main__": eval(cmd())










