# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    closed=dict()
    path=util.Queue()#queue is used because when i insert directions to the path i want it to be put at the last start of the list because directions are added in reverse
    fringe=util.Stack()#by theory we know dfs uses stack 
    start=problem.getStartState()
    fringe.push((start, 'south', 0,(0,0)))#making dummy it has the same data type with all the other fringe nodes and this dummy will never be used
    while 1:
        if fringe.isEmpty():
            return [] #return failure
        node=fringe.pop()
        # node=node[0]
        closed[node[0]]=(node[1],node[3])#for each we state we have a pair of data that tells us what direction took us there and from where(the parent state)
        if problem.isGoalState(node[0]):
            temp=node[0]
            while temp!=start:#strating from the goal until we reach the start state so in reverse
                path.push(closed[temp][0])#add the direction we took to path. we start by inserting the direction to goal but with queue push to index 0 that ends up last
                temp=closed[temp][1]#set temp as it's parent state
            return path.list
        children=problem.getSuccessors(node[0])
        for x in children:
            if x[0] not in closed:#reexamining states is useless
                x+=(node[0],)#getsuccessors function gives us 3 info about the children but to construct a path i found it necessary to also know the parent(previous) state so i add it to each fringe node that gets popped later
                fringe.push(x)#when i  write "x[0](state) not in closed" it searches for it in the keys of the dictionary not in the values


def existsinfringe(fringe,xo):
    for f in fringe:
        if f[0]==xo:
            return True
    return False

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    closed=util.Counter()
    path=util.Queue()
    fringe=util.Queue()#only difference is bfs uses queue for level order traveral
    start=problem.getStartState()
    # print(start)
    fringe.push((start, 'south', 0,(0,0)))
    while 1:
        #print("once")
        if fringe.isEmpty():
            return []
        node=fringe.pop()
        # node=node[0]
        closed[node[0]]=(node[1],node[3])
        if problem.isGoalState(node[0]):
            temp=node[0]
            while temp!=start:
                path.push(closed[temp][0])
                temp=closed[temp][1]
            return path.list
        children=problem.getSuccessors(node[0])
        for x in children:
            if x[0] not in closed and existsinfringe(fringe.list,x[0])==False:#second difference is i gotta also check for existance in fringe because i dont want the same node getting pushed twice and the parent getting overwritten
                x+=(node[0],)#this change is unecessary in dfs because by the time we return to that level this child is popped from the fringe and inside closed. this change i what makes bfs give the optimal solution
                fringe.push(x)


def updatewithoutadd(fringe, item, priority):
    for index, (p, c, i) in enumerate(fringe.heap):
        if i == item:
            if p <= priority:
                return False
            del fringe.heap[index]
            fringe.heap.append((priority, c, item))
            util.heapq.heapify(fringe.heap)
            return True

def heappopwithpriority(heap):
    (prio, _, item) = util.heapq.heappop(heap.heap)
    return item,prio


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    closed=dict()
    path=util.Queue()
    fringe=util.PriorityQueue()
    start=problem.getStartState()
    fringe.push((start),0 )
    closed[start]=('south',0,(0,0))
    while 1:
        if fringe.isEmpty():
            return []
        node,nodep=heappopwithpriority(fringe)
        # node=node[0] if not
        #closed[node[0]]=(node[1],node[2],node[3])
        if problem.isGoalState(node):
            temp=node
            while temp!=start:
                path.push(closed[temp][0])
                temp=closed[temp][2]
            return path.list
        children=problem.getSuccessors(node)
        for x in children:
            if x[0] not in closed:
                closed[x[0]]=(x[1],x[2]+nodep,node)
                fringe.push(x[0],x[2]+nodep)#nodep equals to closed[node] but its more readable to the programmer this way
            elif updatewithoutadd(fringe,x[0],x[2]+nodep)== True :
                closed[x[0]]=(x[1],x[2]+nodep,node)#if update = false(didnt happen) then dont change the parent

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    closed=dict()
    path=util.Queue()
    fringe=util.PriorityQueue()
    start=problem.getStartState()
    fringe.push((start),heuristic(start,problem) )
    closed[start]=('south',0,(0,0))
    while 1:
        if fringe.isEmpty():
            return []
        node,nodep=heappopwithpriority(fringe)
        # node=node[0] if not
        #closed[node[0]]=(node[1],node[2],node[3])
        if problem.isGoalState(node):
            temp=node
            while temp!=start:
                path.push(closed[temp][0])
                temp=closed[temp][2]
            return path.list
        children=problem.getSuccessors(node)
        for x in children:
            if x[0] not in closed:#nodep which is added contains the heuretic value of the parent which we dont want interffering anymore so i remove it with "- heuristic(node,problem)".
                closed[x[0]]=(x[1],x[2]+nodep + heuristic(x[0],problem) - heuristic(node,problem)  ,node)#in other words we want the sum of the weights of the path not of the heuretics
                fringe.push(x[0],x[2]+nodep + heuristic(x[0],problem) - heuristic(node,problem) )
            elif updatewithoutadd(fringe,x[0],x[2]+nodep + heuristic(x[0],problem) - heuristic(node,problem) )== True :
                closed[x[0]]=(x[1],x[2]+nodep + heuristic(x[0],problem) - heuristic(node,problem) ,node)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
