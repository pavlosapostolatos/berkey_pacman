# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        foodPos = newFood.asList()
        foodCount = len(foodPos)
        prevfood=len(currentGameState.getFood().asList())
        if foodCount == 0 :#if action ate the last dot we will win so return maximum possible value in order to just do it
            return 1000000000
        # walls=successorGameState.walls
        usefullness= 1000000000#maximum possible value
        uselessness= 1000000000#maximum possible value
        for food in foodPos:
          distance = manhattanDistance(food,newPos) - (prevfood-foodCount)*30#this what makes evaluation greedy. we pick the position that is closest to a food
          distance-=(len(currentGameState.getCapsules()) -len(successorGameState.getCapsules()))*10000000#make eating an energizer a capsule thyta can scare ghosts really useful
          if distance < uselessness:
            uselessness = distance# (foodCount-prevfood)*500 makes it so that when action eats a dot it's uselessness factor isnt equal with the uselessness of position that has the same manhattan distance but doesnt eat a dot
            closestFood = foodPos#it gets complicated like that because line 70 renders the dot(food) already eaten so mahhattan distance can never amount to 0

        for ghostState in newGhostStates:
          ghostPos = ghostState.getPosition()
          if (newPos==ghostPos or manhattanDistance(ghostPos,newPos)<=1) and ghostState.scaredTimer==0 :
            uselessness = 1000000000#most useless move because it will kill pacman
          elif (newPos==ghostPos or manhattanDistance(ghostPos,newPos)<=1) and ghostState.scaredTimer>0 :
            uselessness = 1#i want to reward eating hosts when its easy(i.e they are next to you) this command makes it the 2nd best move overtaken only by the victory move

        return usefullness-uselessness #successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def MinMax(self,currentGameState, agent, depth):
        lastghost = currentGameState.getNumAgents() - 1
        if (currentGameState.isLose() or currentGameState.isWin() or (depth == self.depth)):
            return [self.evaluationFunction(currentGameState)]
        elif agent == lastghost:
            depth += 1
            nextAgent = self.index
        else:
            nextAgent = agent + 1
        legalActionList = currentGameState.getLegalActions(agent)
        moves=[]
        for action in legalActionList:#this creates the all the possible combinations of moves by mixing all agents' legal moves for a given depth.see the pdf for the size formula 
            successorGameState = currentGameState.generateSuccessor(agent, action)#first pacman plays and then the ghosts
            moves.append((self.MinMax(successorGameState, nextAgent, depth)[0],action))#by passing successor state pacman's and the previous ghosts moves have happened while the next ghost decides it's move
        if agent != 0:
            return min(moves)
        else:
            return max(moves)

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"


        return self.MinMax(gameState, self.index,0)[1]#my return object is a tuple that has the optimal value for the max or min node that called the function and the move(action) that produced it. getAction wants the move so i return [1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def AlphaBeta(self,currentGameState, agent, depth,alpha,beta):
        lastghost = currentGameState.getNumAgents() - 1
        if (currentGameState.isLose() or currentGameState.isWin() or (depth == self.depth)):
            return [self.evaluationFunction(currentGameState)]
        elif agent == lastghost:
            depth += 1
            nextAgent = self.index
        else:
            nextAgent = agent + 1
        legalActionList = currentGameState.getLegalActions(agent)
        v=(1000000 - (agent== self.index)*2000000,"tuplify")#min or maximum int value if agent isnt MAX . the [1] part which has the action is irrelevant
        for action in legalActionList:#this creates the all the possibloe combinations on moves by mixing all agents' legal moves for a given depth.see the pdf for the size formula 
            # if beta < alpha:
            #     break
            # if agent != 0 and v<alpha:
            #     return v
            # elif agent == 0 and v>beta:
            #     return v
            successorGameState = currentGameState.generateSuccessor(agent, action)#first pacman plays and then the ghosts
            temp=(self.AlphaBeta(successorGameState, nextAgent, depth,alpha,beta)[0],action)#by passing successor state pacman's and the previous ghosts moves have happened while the next ghost decides it's move
            if agent != self.index:
                v=min(v,temp)
                # if temp<v:
                #     v=temp
                beta=min(beta,v) 
                if v<alpha:# the pruning condition
                    return v#break doesnt let it examine more states it prunes them
                      
            #Player is MAX
            else:
                v=max(v,temp)
                # if temp>v:
                #     v=temp
                alpha=max(alpha,v)
                if v>beta:
                    return v  
            if beta < alpha:
                break
        # if agent != 0:
        #     return beta
        # else: 
        #     return alpha 
        return v       

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.AlphaBeta(gameState, self.index,0,(-1000000,"tuplify"),(1000000,"tuplify"))[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def ExcpMax(self,currentGameState, agent, depth):
        lastghost = currentGameState.getNumAgents() - 1
        if (currentGameState.isLose() or currentGameState.isWin() or (depth == self.depth)):
            return [self.evaluationFunction(currentGameState)]
        elif agent == lastghost:
            depth += 1
            nextAgent = self.index
        else:
            nextAgent = agent + 1
        legalActionList = currentGameState.getLegalActions(agent)
        moves=[]
        for action in legalActionList:#this creates the all the possibloe combinations on moves by mixing all agents' legal moves for a given depth.see the pdf for the size formula 
            successorGameState = currentGameState.generateSuccessor(agent, action)#first pacman plays and then the ghosts
            moves.append((self.ExcpMax(successorGameState, nextAgent, depth)[0],action))#by passing successor state pacman's and the previous ghosts moves have happened while the next ghost decides it's move
        if agent != 0:
            return  (sum([move[0] for move in moves])/len(moves),"tuplify")#the only difference is min now returns an average
        else:
            return max(moves)
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.ExcpMax(gameState, self.index,0)[1]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    pacmanPosition = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    foodList = currentGameState.getFood().asList()
    numFood = currentGameState.getNumFood()
    capsules=currentGameState.getCapsules()
    numCapsules = len(currentGameState.getCapsules())#get the values that are gonna be graded
    if currentGameState.isWin():
        return 1000000000
    elif currentGameState.isLose():
        return -1000000000#best ad worst case
    score = 1000 * currentGameState.getScore()
    score += 10000000/(numCapsules+1)#like in q1 the difference in numCapsules between 2 states can be 1 and the state that has 1 less is rewarded more
    score +=1000/(numFood+1)#same idea here
    for food in foodList:
        score += 1/(manhattanDistance(pacmanPosition, food))
    for capsule in capsules:
        score += 50/(manhattanDistance(pacmanPosition, capsule))#as i said in the pdf distances are also taken account of
    for ghostState in ghostStates:
        if ghostState.scaredTimer==0:# if the ghost isnt scared reward being far from it
            score +=  manhattanDistance(pacmanPosition, ghostState.getPosition())
        else:#else reward being closer
            score += 1/ (manhattanDistance(pacmanPosition, ghostState.getPosition()) +1)
    return score 


# Abbreviation
better = betterEvaluationFunction
