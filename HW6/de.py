from __future__ import division
import sys, random, math
from models import *
from base import *

def de(model):
  eb = 0.0
  min_energy, max_energy = model.baseline()
  s = model.generate_x()
  e = model.norm(model.getDepen(s))
  sb = s[:]
  eb = e
  population = []
  for _ in xrange(Settings.de.np):
    population.append(model.generate_x())
    