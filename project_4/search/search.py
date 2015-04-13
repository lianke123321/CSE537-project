# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util 
class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  """
  This function makes a generic implementation of DFS.Following variables are mainly used -
  1. state_stack - It is the stack class imported from util class. It keeps track of the nodes to be expanded and pops the nodes depth first.
  2. parents - It is used to backtrack the path of the node after it reaches the goal.
  3. direction - This is also used to backtrack the path of the node once it reaches goal. It gives the exact direction to trace back.
  4. visited - This keeps track of visited nodes so as to avoid a deadlock.
  5. path - This is used to return the path to the main function
  """
  from game import Directions
  from spade import pyxf
  south = Directions.SOUTH
  west = Directions.WEST
  north = Directions.NORTH
  east = Directions.EAST
  
  myXSB = pyxf.xsb("/home/adrian/Applications/XSB/bin/xsb")
  myXSB.load("prolog_scripts/maze.P")
  myXSB.load("prolog_scripts/dfs.P")
  result1 = myXSB.query("dfs(start,[],P,D).")
  #print result1
  path = result1[0]['D']
  #print path, len(path)
  path2 = path[1:-6]
  #print path2
  import re
  path3 = re.split(',',path2)
  #print path3
  path4 = [word[:1].upper() + word[1:] for word in path3]
  #print path4
  #print "Sending the path"
  return path4

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"

  """
  This function makes a generic implementation of DFS.Following variables are mainly used -
  1. state_queue - It is the queue class imported from util class. It keeps track of the nodes to be expanded and pops the nodes breadth first.
  2. parents - It is used to backtrack the path of the node after it reaches the goal.
  3. direction - This is also used to backtrack the path of the node once it reaches goal. It gives the exact direction to trace back.
  4. visited - This keeps track of visited nodes so as to avoid a deadlock.
  5. path - This is used to return the path to the main function
  """
  from game import Directions
  from spade import pyxf
  south = Directions.SOUTH
  west = Directions.WEST
  north = Directions.NORTH
  east = Directions.EAST
  
  myXSB = pyxf.xsb("/home/adrian/Applications/XSB/bin/xsb")
  myXSB.load("prolog_scripts/maze.P")
  myXSB.load("prolog_scripts/bfs.P")
  result1 = myXSB.query("solve(start,D).")
  #print result1
  #print result1[0]['D']
  path = result1[0]['D']
  #print path, len(path)
  path2 = path[1:-7]
  #print path2
  import re
  path3 = re.split(',',path2)
  #print path3
  path4 = [word[:1].upper() + word[1:] for word in path3]
  #print path4
  path5 = path4[1:][::2]
  path6 = path5[::-1]
  #print path5, path6
  #print path[0]
  #print "Sending the path"
  return path6

     

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  """
  This function makes a generic implementation of UCS.Following variables are mainly used -
  1. state_queue - It is the priority queue class imported from util class. It keeps track of the nodes to be expanded and pops the nodes in order of their priotiy.
  2. parents - It is used to backtrack the path of the node after it reaches the goal.
  3. direction - This is also used to backtrack the path of the node once it reaches goal. It gives the exact direction to trace back.
  4. visited - This keeps track of visited nodes so as to avoid a deadlock.
  5. cost - this keeps track of the cost of the nodes and adds them to the child if needed.
  6. path - This is used to return the path to the main function
  """
  from game import Directions
  from spade import pyxf
  south = Directions.SOUTH
  west = Directions.WEST
  north = Directions.NORTH
  east = Directions.EAST
  
  myXSB = pyxf.xsb("/home/adrian/Applications/XSB/bin/xsb")
  myXSB.load("prolog_scripts/mazeastar.P")
  myXSB.load("prolog_scripts/astar.P")
  #result = myXSB.query("connected(start#A#D#E#F).")
  result1 = myXSB.query("solve(start, D).")
  #print "Result is -"
  #print result1
  path = result1[0]['D']
  path2 = path[1:-1]
  import re
  path3 = re.split(',',path2)
  final_path = []
  i=1
  for it in path3:
    temp = re.split('#',it.replace(" ",""))
    final_path.append(temp[1])

  del final_path[-1]
  path4 = [word[:1].upper() + word[1:] for word in final_path]
  path6 = path4[::-1]
  #print "Sending the path"
  return path6
 

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
