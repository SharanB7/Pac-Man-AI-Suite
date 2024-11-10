import util
from util import Stack, Queue, PriorityQueue

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
    return [s, s, w, s, w, w, s, w]

def genericSearch(problem, fringe):

    visited = set()
    totalPath = list()
    fringe.push((problem.getStartState(), list(), 0))
    while not fringe.isEmpty():
        currentState = fringe.pop()
        if problem.isGoalState(currentState[0]) == True:
            return currentState[1]
        if currentState[0] not in visited:
            for childNode, action, childCost in problem.getSuccessors(currentState[0]):
                    totalPath = currentState[1].copy()
                    totalPath.append(action)
                    totalCost = currentState[2] + childCost
                    fringe.push((childNode, totalPath, totalCost))
        visited.add(currentState[0])

    return None


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
    # Maintaining a list to store visited nodes.
    visitedStates = list()
    # Maintaining a stack for accessing nodes in LIFO order.
    fringe = Stack()
    fringe.push((problem.getStartState(), [], 0))
    # Everytime a node is evaluated and expanded, its children are added. Stack will be emptied only at the end.
    while not fringe.isEmpty():
        thisState, path, cost = fringe.pop()
        # Return the path if goal is found.
        if problem.isGoalState(thisState):
            return path
        # Else, expand and add its children to the stack, updating the path and costs.
        if thisState not in visitedStates:
            visitedStates.append(thisState)
            for childState, action, childCost in problem.getSuccessors(thisState):
                fringe.push((childState, path + [action], cost + childCost))
    # Return empty array if goal node is not found.
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Maintaining a list to store visited nodes.
    visitedStates = list()
    # Maintaining a queue for accessing nodes in FIFO order.
    fringe = Queue()
    fringe.push((problem.getStartState(), [], 0))
    # Everytime a node is evaluated and expanded, its children are added. Stack will be emptied only at the end.
    while not fringe.isEmpty():
        thisState, path, cost = fringe.pop()
        # Return the path if goal is found.
        if problem.isGoalState(thisState):
            return path
        # Else, expand and add its children to the queue, updating the path and costs.
        if thisState not in visitedStates:
            visitedStates.append(thisState)
            for childState, action, childCost in problem.getSuccessors(thisState):
                fringe.push((childState, path + [action], cost + childCost))
    # Return empty array if goal node is not found.
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Maintaining a list to store visited nodes.
    visitedStates = list()
    # Maintaining a priority queue for accessing nodes according to their g values.
    fringe = PriorityQueue()
    fringe.push((problem.getStartState(), [], 0), 0)
    # Everytime a node is evaluated and expanded, its children are added. Stack will be emptied only at the end.
    while not fringe.isEmpty():
        thisState, path, cost = fringe.pop()
        # Return the path if goal is found.
        if problem.isGoalState(thisState):
            return path
        # Else, expand and add its children to the priority queue, updating the path and costs.
        if thisState not in visitedStates:
            visitedStates.append(thisState)
            for childState, action, childCost in problem.getSuccessors(thisState):
                fringe.push((childState, path + [action], cost + childCost), cost + childCost)
    # Return empty array if goal node is not found.
    return []
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # Maintaining a list to store visited nodes.
    visitedStates = list()
    # Maintaining a priority queue for accessing nodes according to their f (= g + h) values .
    fringe = PriorityQueue()
    startState = problem.getStartState()
    # Using the heuristic function to get h values.
    fringe.push((startState, [], 0), 0 + heuristic(startState, problem))
    # Everytime a node is evaluated and expanded, its children are added. Stack will be emptied only at the end.
    while not fringe.isEmpty():
        thisState, path, cost = fringe.pop()
        # Return the path if goal is found.
        if problem.isGoalState(thisState):
            return path
        # Else, expand and add its children to the priority queue, updating the path and costs.
        if thisState not in visitedStates:
            visitedStates.append(thisState)
            for childState, action, childCost in problem.getSuccessors(thisState):
                fringe.push((childState, path + [action], cost + childCost), cost + childCost + heuristic(childState, problem))
    # Return empty array if goal node is not found.
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
