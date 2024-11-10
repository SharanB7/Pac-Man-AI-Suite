import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # Iterating over the number of iterations
        for i in range(self.iterations):
            # Initializing a second counter as we need batch value iteration and not online
            values = util.Counter()
            # Updating value for every non-terminal state
            for state in self.mdp.getStates():
                if not self.mdp.isTerminal(state):
                    stateValues = []
                    # Finding Q-Values for all possible actions
                    for action in self.mdp.getPossibleActions(state):
                        stateValues.append(self.getQValue(state, action))
                    # Assigning the state value as maximum Q-Value
                    values[state] = max(stateValues)
            # Updating the state values - Batch version of value iteration
            for state in self.mdp.getStates():
                self.values[state] = values[state]

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # Finding Q-Value for a given state and action
        stateValue = 0.0
        for transitionState, transitionProbability in self.mdp.getTransitionStatesAndProbs(state, action):
            stateValue += transitionProbability * ((self.mdp.getReward(state, action, transitionState)) + (self.discount * self.getValue(transitionState)))
        return stateValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actionValues = {}
        # Fetching values of all actions from a given state
        for action in self.mdp.getPossibleActions(state):
            actionValues[action] = self.getQValue(state, action)
        # Returning None for terminal state and the action with maximum value for non-terminal states
        return None if self.mdp.isTerminal(state) else max(actionValues, key=lambda k: actionValues[k])


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        # Iterating over the number of iterations
        for i in range(self.iterations):
            # Selecting state according to the cycle, i.e., one state in each iteration in order
            state = self.mdp.getStates()[i % len(self.mdp.getStates())]
            # Updating the value of the selected state if it is a non-terminal state
            if not self.mdp.isTerminal(state):
                stateValues = []
                # Finding Q-Values for all possible actions
                for action in self.mdp.getPossibleActions(state):
                    stateValues.append(self.getQValue(state, action))
                # Assigning the state value as maximum Q-Value
                self.values[state] = max(stateValues)

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        statePredecessors = {}
        # Finding predecessors for all states
        for state in self.mdp.getStates():
            for action in self.mdp.getPossibleActions(state):
                for transitionState, transitionProbability in self.mdp.getTransitionStatesAndProbs(state, action):
                    # Creating a new set if encountering the state for the first time
                    if transitionState not in statePredecessors:
                        statePredecessors[transitionState] = {state}
                    # Updating the set if the state has been encountered already
                    else:
                        statePredecessors[transitionState].add(state)

        # Initialized a priority queue for storing difference in values
        absDifferences = util.PriorityQueue()
        # Updating the differences for all states
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                stateValues = []
                for action in self.mdp.getPossibleActions(state):
                    stateValues.append(self.getQValue(state, action))
                # Pushing the state into the queue along with priority -diff
                absDifferences.update(state, - abs(self.getValue(state) - max(stateValues)))

        for i in range(self.iterations):
            # Terminating if the queue is empty
            if absDifferences.isEmpty():
                return
            state = absDifferences.pop()
            # Updating the state's value if it is a non-terminal state
            if not self.mdp.isTerminal(state):
                stateValues = []
                for action in self.mdp.getPossibleActions(state):
                    stateValues.append(self.getQValue(state, action))
                self.values[state] = max(stateValues)
            # Finding difference in values for all predecessors of the given state
            for predecessor in statePredecessors[state]:
                if not self.mdp.isTerminal(predecessor):
                    stateValues = []
                    for action in self.mdp.getPossibleActions(predecessor):
                        stateValues.append(self.getQValue(predecessor, action))
                    # Pushing the predecessor into the priority queue if absolute difference is more than theta
                    if abs(self.getValue(predecessor) - max(stateValues)) > self.theta:
                        absDifferences.update(predecessor, - abs(self.getValue(predecessor) - max(stateValues)))
