from __future__ import division
import sys, random, math, datetime, time,re
sys.dont_write_bytecode = True


def pairs(lst):
  last=lst[0]
  for i in lst[1:]:
    yield last,i
    last = i

def xtile(lst,lo=0,hi=0.001, width = 50, 
             chops=[0.1 ,0.3,0.5,0.7,0.9],
             marks=["-" ," "," ","-"," "],
             bar="|",star="*",show=" %3.0f"):
  """The function _xtile_ takes a list of (possibly)
  unsorted numbers and presents them as a horizontal
  xtile chart (in ascii format). The default is a 
  contracted _quintile_ that shows the 
  10,30,50,70,90 breaks in the data (but this can be 
  changed- see the optional flags of the function).
  """
  ordered_list = sorted(lst)  # Dr.Menzies tricks
  lo = min(lo, ordered_list[0])
  hi = max(hi, ordered_list[-1])
  showNumbers = [ ordered_list[int(percent * len(lst))] for percent in chops]
  # print showNumbers
  showMarks = [" "] * width
  def find_index (x):
    return int(width*float((x-lo))/(hi-lo))
  markIndex = [find_index(i) for i in showNumbers]
  for i in range(width):
    if i in range(markIndex[0],markIndex[1]+1) or i in range(markIndex[-2],markIndex[-1]+1):
      showMarks[i] = "-"
  #print showMarks  
  showMarks[int(width * 0.5)] = "|"
  showMarks[find_index(ordered_list[int(len(lst)*0.5)])] = "*"  
  return " ".join(showMarks) + " ".join([str(round(i,3)) for i in showNumbers])  

def Demo() :
  import random
  random.seed(1)
  # nums = [random.random()**2 for _ in range(100)]
  #nums = [0.011,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]
  nums = [0,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1, 0.1]
  print xtile(nums,lo=0,hi=1.0,width=25,)


if __name__ == "__main__": Demo()