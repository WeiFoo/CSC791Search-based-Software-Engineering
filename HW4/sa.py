from __future__ import division
import sys, random, math
from models import *
from base_noprint import *
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
	  # say('!')
    if en < e:
      s = sn
      e = en
      # say('+')
    elif P(e, en, temp) < random.random():
      s = sn
      e = en
      # say('?')
    # say('.')
    k = k + 1
    # if k % 50 == 0:
      # print "\n"  
      # say(str(round(eb,3)))
  # print "\n"
  # printReport(model)
  # print "\n------\n:Normalized Sum of Objectives : ",str(round(eb,3)),"\n:Solution",sn
  lohi=printRange(model)
  return eb,lohiÍ