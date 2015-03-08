# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        score = successorGameState.getScore()   # initialize score
        if successorGameState.isWin():
            return 10000    # return a big num if this move will lead to win
        ghostPositions = currentGameState.getGhostPositions()    # get all positions of ghosts
        #print ghostPositions
        for ghostPos in ghostPositions:
            distFromGhost = util.manhattanDistance(newPos, ghostPos)
            if distFromGhost <= 1:
                return -10000   # return a big negative num if ghost is too close

        foods = newFood.asList()
        foodDists = []
        for foodPos in foods:
            foodDists.append(util.manhattanDistance(newPos, foodPos))
        #print min(foodDists)
        score -= min(foodDists)

        if(currentGameState.getNumFood()) > successorGameState.getNumFood():
            score += 50 # encourage eating food

        if action == Directions.STOP:
            score -= 10 # stop not preferred

        return score
        #return successorGameState.getScore()

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
        """
        "*** YOUR CODE HERE ***"
        def minValue(gameState, depth, agentIndex, numGhosts):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                #print "minValue reached bottom, returning ", self.evaluationFunction(gameState)
                return self.evaluationFunction(gameState)   # last ply simply return
            value = 10000   # to find min
            legalActions = gameState.getLegalActions(agentIndex)    # get all children
            if agentIndex == numGhosts:
                for action in legalActions:
                    value = min(value, maxValue(gameState.generateSuccessor(agentIndex, action), depth - 1, numGhosts))
            else:
                for action in legalActions:
                    value = min(value, minValue(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, numGhosts))
            #print "minValue normal return, returning ", value
            return value

        def maxValue(gameState, depth, numghosts):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                #print "maxValue reached bottom, returning ", self.evaluationFunction(gameState)
                return self.evaluationFunction(gameState)   # last ply simply return
            value = -10000  # to find max
            legalActions = gameState.getLegalActions(0) # always pacman move, with index 0
            for action in legalActions:
                value = max(value, minValue(gameState.generateSuccessor(0, action), depth - 1, 1, numghosts))
            #print "maxValue normal return, returning ", value
            return value

        legalActions = gameState.getLegalActions()
        numGhosts = gameState.getNumAgents() - 1
        chosen = Directions.STOP
        score = -10000  # find max so initializing score as a big negative num
        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            tmpScore = score
            # calculate the min value of each child then choose the max one
            score = max(score, minValue(nextState, self.depth, 1, numGhosts))
            if score > tmpScore:
                chosen = action
        return chosen
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def minValue(gameState, alpha, beta, agentIndex, depth, numGhosts):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                #print "minValue reached bottom, returning ", self.evaluationFunction(gameState)
                return self.evaluationFunction(gameState)   # last ply simply return
            value = 10000   # only care about minimum value
            legalActions = gameState.getLegalActions(agentIndex)
            if agentIndex == numGhosts:
                for action in legalActions:
                    value = min(value, maxValue(gameState.generateSuccessor(agentIndex, action),\
                                                alpha, beta, depth-1, numGhosts))
                    # critical step here, cause we will choose min, so final value must be
                    # smaller than this value, but parent is choosing a max, so if this
                    # value is smaller than current max (alpha), this child is useless,
                    # directly return w/o searching other children
                    if value <= alpha:
                        #print "minValue cut edge, returning ", value
                        return value
                    if value < beta:
                        beta = value    # update current min
            else:
                for action in legalActions:
                    value = min(value, minValue(gameState.generateSuccessor(agentIndex, action),\
                                                alpha, beta, agentIndex+1, depth, numGhosts))
                    if value <= alpha:
                        #print "minValue cut edge, returning ", value
                        return value
                    if value < beta:
                        beta = value
            #print "minValue normal return, returning ", value
            return value

        def maxValue(gameState, alpha, beta, depth, numGhosts):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                #print "maxValue reached bottom, returning ", self.evaluationFunction(gameState)
                return self.evaluationFunction(gameState)   # last ply simply return
            value = -10000  # only care about minimum value
            legalActions = gameState.getLegalActions(0)
            for action in legalActions:
                value = max(value, minValue(gameState.generateSuccessor(0, action),\
                                            alpha, beta, 1, depth-1, numGhosts))
                if value >= beta:   # same explanation as in minValue
                    #print "maxValue cut edge, returning ", value
                    return value
                if value > alpha:   # update current max
                    alpha = value
            #print "maxValue normal return, returning ", value
            return value

        legalActions = gameState.getLegalActions() # as usual, get all possible moves
        numGhosts = gameState.getNumAgents() - 1
        chosen = Directions.STOP
        score = -10000  # same with minimax
        alpha = -10000  # used to represent current max
        beta = 10000    # used to represent current min
        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            tmpScore = score
            score = max(score, minValue(nextState, alpha, beta, 1, self.depth, numGhosts))
            if score > tmpScore:
                chosen = action
            if score >= beta:   # same explanation as in minValue
                return chosen
            if score > alpha:
                alpha = score   # alpha is current max, if we found a larger score then use it to update alpha
        return chosen
        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

