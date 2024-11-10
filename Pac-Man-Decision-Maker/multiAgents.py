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
        # Extracting additional information
        newCapsules = successorGameState.getCapsules()

        currCapsules = currentGameState.getCapsules()
        currFood = currentGameState.getFood()

        value = 0

        # If next state is a win state, returns high positive value
        if successorGameState.isWin():
            value += float('inf')
            return value

        # Making the pacman to move towards a food pellet
        for food in newFood.asList():
            distance = manhattanDistance(newPos, food)
            value += 1.0 / distance

        # Rewarding the pacman for finding a food pellet
        if newPos in currFood:
            value += 5.0

        # Making the pacman to move towards a food capsule, with a higher factor
        for capsule in newCapsules:
            distance = manhattanDistance(newPos, capsule)
            value += 25.0 / distance

        # Rewarding the pacman for finding a food capsule
        if newPos in currCapsules:
            value += 100.0

        # Assessing pacman's position with respect to ghost positions
        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            distance = manhattanDistance(newPos, ghostPos)
            scaredTime = ghost.scaredTimer
            # If ghost is nearby and isn't scared, making the pacman avoid the state by assigning negative value
            if 0 < scaredTime < distance < 5:
                value -= 9999.9
            # If ghost is nearby and scare, making the pacman to go towards the ghost! That's how I play :)
            elif 0 < distance < 10 < scaredTime:
                value += 999.9
            # If pacman finds a ghost in the next position, strictly avoiding that state by assigning high negative value
            elif distance == 0:
                value -= float('inf')
                return value

        # Making the pacman to be in motion always by penalizing if stopped
        if action == Directions.STOP:
            value -= 10.0

        # Adding the state's score to value
        value += successorGameState.getScore()

        return value

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def miniMax(state, agentIndex, depth):
            # Pacman's turn
            if agentIndex == 0:
                # Returning state value if it is a terminal node or if depth limit is reached
                if state.isWin() or state.isLose() or depth == self.depth:
                    return self.evaluationFunction(state)
                # Setting parameters for next evaluation
                nextAgentIndex = 1
                depth += 1
            # Ghost's turn
            else:
                # Returning state value if it is a terminal node
                if state.isWin() or state.isLose():
                    return self.evaluationFunction(state)

                # Setting parameters for next evaluation
                # If it is the last ghost, then pacman is called in the next evaluation
                nextAgentIndex = 0 if agentIndex == (state.getNumAgents() - 1) else (agentIndex + 1)

            actions = state.getLegalActions(agentIndex)
            nextStateValues = []
            for action in actions:
                # Storing the state values for each action possible
                nextStateValues.append(miniMax(state.generateSuccessor(agentIndex, action), nextAgentIndex, depth))
            # Returning max value if it is pacman's turn (max agent) else min value if it is ghost's turn (min agent)
            return max(nextStateValues) if agentIndex == 0 else min(nextStateValues)

        actions = gameState.getLegalActions(0)
        actionValues = {}
        # Finding value for each action possible from root node (max agent)
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            value = miniMax(successor, 1, 1)
            actionValues[action] = value

        # Returning the action that gives maximum value
        return max(actionValues, key=lambda k: actionValues[k])

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphaBetaPruning(state, agentIndex, depth, alpha, beta, value):
            # Pacman's turn
            if agentIndex == 0:
                # Returning state value if it is a terminal node or if depth limit is reached
                if state.isWin() or state.isLose() or depth == self.depth:
                    return self.evaluationFunction(state)
                # Setting parameters for next evaluation
                nextAgentIndex = 1
                nextDepth = depth + 1
                nextValue = float('inf')
            else:
                # Returning state value if it is a terminal node
                if state.isWin() or state.isLose():
                    return self.evaluationFunction(state)
                # Setting parameters for next evaluation
                # If it is the last ghost, then pacman is called in the next evaluation
                nextAgentIndex = 0 if agentIndex == (state.getNumAgents() - 1) else (agentIndex + 1)
                nextDepth = depth
                nextValue = float('-inf') if agentIndex == (state.getNumAgents() - 1) else float('inf')
            actions = state.getLegalActions(agentIndex)
            for action in actions:
                stateValue = alphaBetaPruning(state.generateSuccessor(agentIndex, action), nextAgentIndex, nextDepth, alpha, beta, nextValue)
                # Pacman's turn.
                if agentIndex == 0:
                    # Finding the best action and updating beta value accordingly
                    value = max(value, stateValue)
                    if stateValue == value and depth == 0:
                        bestAction = action
                    if value > beta:
                        break
                    alpha = max(alpha, value)
                else:
                    # Updating alpha value
                    value = min(value, stateValue)
                    if value < alpha:
                        break
                    beta = min(beta, value)

            return bestAction if depth == 0 else value

        # Initializing alpha and beta values. alpha is the higher limit (hence, -inf) and beta is the lower level (hence, inf)
        alpha = float('-inf')
        beta = float('inf')
        # Max agent's turn the first time. So, -inf.
        value = float('-inf')
        return alphaBetaPruning(gameState, 0, 0, alpha, beta, value)

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
