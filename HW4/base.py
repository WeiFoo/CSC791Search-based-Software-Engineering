from __future__ import division
import sys, random, math, datetime, time,re
sys.dont_write_bytecode = True

class Options: #"Thanks for Peter Norvig's trick"
  def __init__(i, **d): i.__dict__.update(d)

Settings = Options(sa = Options(kmax = 1000, 
	                              baseline = 1000,
                                score = {}),
                   mws= Options(threshold = 0.05,
                                max_tries = 50, 
                                max_changes = 1000,
                                prob = 0.25,
                                score = {}
                                ) )

def reseed():
	seed = 1
	return random.seed(seed)

def say(mark):
  sys.stdout.write(mark)
  sys.stdout.flush()

def printlook(f):
  def wrapper(*lst): #tricks from Dr.Menzies
    ShowDate = datetime.datetime.now().strftime
    print "\n###", f.__name__, "#" * 50
    print "#", ShowDate("%Y-%m-%d %H:%M:%S")
    beginTime = time.time()
    x = f(*lst)
    endTime = time.time()
    print "\n" +("-"*60)
    dump(Settings, f.__name__)
    print "\n# Runtime: %.3f secs" % (endTime-beginTime)
    return f.__name__, x # return the searcher name and the results
  return wrapper

def dump(d, searchname, lvl = 0): # tricks from Dr. Menzies
  d = d if isinstance(d, dict) else d.__dict__
  callableKey, line , gap = [], "", "  "*lvl
  for k in sorted(d.keys()):
    val= d[k]
    if isinstance(val, (dict, Options)):
      callableKey += [k]
    else:
      #if callable(val):
      #	val = val.__name__
      line +=("  {0} :{1}".format(k, val))
  print gap + line
  for k in callableKey:
    if k == searchname:
      print gap + (" :{0} {1}".format(k, "options"))
      dump(d[k], lvl+1)

