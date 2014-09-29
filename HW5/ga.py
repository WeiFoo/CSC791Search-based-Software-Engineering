from __future__ import division
from log import *
from models import *
import sys, random, math, datetime, time,re, pdb, operator
sys.dont_write_bytecode = True

def ga():
  model = DTLZ7()
  mutationRate = 1/model.n 
  population = []
  solution =[]
  def selection(sortedFitness):
    return [population[sortedFitness[0][0]], population[sortedFitness[1][0]]] # sroted[0] and [1] are the smallest two we preferred
  def crossover(selected):
    children = []
    if rand()> Settings.ga.crossRate:
      return selected[0]
    else:
      index = sorted([random.randint(0, model.n - 1) for _ in xrange(Settings.ga.crossPoints)])
      parent = selected[0] 
      children = parent[:]
      children[index[0]:index[1]] = selected[1][index[0]:index[1]]
      return children
  def mutate(children, selected):
    # print children
    for k, n in enumerate(children):
      if rand()< mutationRate:
        print "mutation" + str(k)
        children[k] = selected[random.randint(0,1)][random.randint(0, model.n-1)] # pick value from mom or dad
    # print children
    return children

  def produce(selected):
  	children = crossover(selected)
  	children = mutate(children, selected)
  	return children

  for _ in xrange(Settings.ga.pop):
    temp = model.generate_x()
    population.append(temp)
  for num in Settings.ga.genNum:
    t = 0
    while(t < num ): # figure stop out
      fitness = {}
      for (k, xlst) in enumerate(population):
        fitness[k] = model.getDepen(xlst) 
      sortedFitness = sorted(fitness.items(), key = lambda x:x[1]) # a sorted list
      solution = sortedFitness[0]
      selected = selection(sortedFitness)
      children = produce(selected)
      population[sortedFiness[-1][1]] = children # replace the worst solution in population with children 


      # print sortedFitness

ga()


    

