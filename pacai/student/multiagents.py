import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core.distance import manhattan
from pacai.core.distance import euclidean

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        # Useful information you can extract.
        # newPosition = successorGameState.getPacmanPosition()
        # oldFood = currentGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPosition = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        for ghost in newGhostStates:
            # Checks if ghost is dangerous and near pacman
            if ghost.isBraveGhost() and manhattan(newPosition, ghost.getPosition()) < 2:
                return -999999
        if newFood.count() == 0:
            return 999999
        oldFood = currentGameState.getFood()
        foodDist = []
        # Checks distance of food and how far it is from other food
        for food in newFood.asList():
            foodDist.append(euclidean(newPosition, food))
            largest = 0
            for diff_food in newFood.asList():
                if food == diff_food:
                    continue
                largest = max(euclidean(food, diff_food), largest)
            foodDist[-1] += largest
        # Reward successfully eating food
        if newFood != oldFood:
            return currentGameState.getScore() + max(foodDist)
        return 1 / min(foodDist) - abs(currentGameState.getScore())

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def minimax_search(self, state):
        # Psuedo code from textbook
        value, move = self.max_value(state, 0, 0)
        return move

    def max_value(self, state, index, depth):
        actions = state.getLegalActions()
        if "Stop" in actions:
            actions.remove("Stop")
        # Arbitrary large number, neg infinity
        low = -999999
        move = None
        if depth == self.getTreeDepth():
            # Max depth hit
            return self.getEvaluationFunction()(state), move
        for a in actions:
            # Generate moves for all ghosts
            utility, a2 = self.min_value(state.generateSuccessor(0, a), index + 1, depth)
            if utility > low:
                low, move = utility, a
        if actions == []:
            # Returns if no actions available
            return self.getEvaluationFunction()(state), move
        return low, move

    def min_value(self, state, index, depth):
        # Positive infinity
        high = 999999
        move = None
        actions = state.getLegalActions(index)
        if actions == []:
            return self.getEvaluationFunction()(state), move
        for a in actions:
            if index == state.getNumAgents() - 1:
                # Min completed for all ghosts, Pacman takes max
                utility, a2 = self.max_value(state.generateSuccessor(index, a), 0, depth + 1)
            else:
                # Generate next ghost successor, order doesn't matter
                utility, a2 = self.min_value(state.generateSuccessor(index, a), index + 1, depth)
            if utility < high:
                high, move = utility, a
        return high, move

    def getAction(self, state):
        return self.minimax_search(state)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def alpha_beta_search(self, state):
        # Psuedo code from textbook
        value, move = self.max_value(state, 0, 0, -999999, 999999)
        return move

    def max_value(self, state, index, depth, alpha, beta):
        actions = state.getLegalActions()
        if "Stop" in actions:
            actions.remove("Stop")
        # Arbitrary large number, neg infinity
        low = -999999
        move = None
        if depth == self.getTreeDepth():
            return self.getEvaluationFunction()(state), move
        for a in actions:
            utility, a2 = self.min_value(state.generateSuccessor(0, a),
            index + 1, depth, alpha, beta)
            if utility > low:
                low, move = utility, a
                alpha = max(alpha, low)
            if low >= beta:
                return low, move
        if actions == []:
            return self.getEvaluationFunction()(state), move
        return low, move

    def min_value(self, state, index, depth, alpha, beta):
        # Positive infinity
        high = 999999
        move = None
        actions = state.getLegalActions(index)
        if actions == []:
            return self.getEvaluationFunction()(state), move
        for a in actions:
            if index == state.getNumAgents() - 1:
                # Min completed, Pacman takes max
                utility, a2 = self.max_value(state.generateSuccessor(index, a),
                0, depth + 1, alpha, beta)
            else:
                # Generate next ghost successor, order doesn't matter
                utility, a2 = self.min_value(state.generateSuccessor(index, a),
                index + 1, depth, alpha, beta)
            # Logic to check if further searching needed
            if utility < high:
                high, move = utility, a
                beta = min(beta, high)
            if high <= alpha:
                return high, move
        return high, move

    def getAction(self, state):
        return self.alpha_beta_search(state)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def minimax_search(self, state):
        # Psuedo code from textbook
        value, move = self.max_value(state, 0, 0)
        return move

    def max_value(self, state, index, depth):
        actions = state.getLegalActions()
        if "Stop" in actions:
            actions.remove("Stop")
        # Arbitrary large number, neg infinity
        low = -999999
        move = None
        if depth == self.getTreeDepth():
            return self.getEvaluationFunction()(state), move
        for a in actions:
            utility, a2 = self.min_value(state.generateSuccessor(0, a), index + 1, depth)
            if utility > low:
                low, move = utility, a
        if actions == []:
            return self.getEvaluationFunction()(state), move
        return low, move

    def min_value(self, state, index, depth):
        # Positive infinity
        high = 999999
        move = None
        actions = state.getLegalActions(index)
        if actions == []:
            return self.getEvaluationFunction()(state), move
        # Randomly selects an action from list of possible ghost actions
        a = actions[random.randint(0, len(actions) - 1)]
        if index == state.getNumAgents() - 1:
            # Min completed, Pacman takes max of all mins
            utility, a2 = self.max_value(state.generateSuccessor(index, a), 0, depth + 1)
        else:
            # Generate next ghost successor, order doesn't matter
            utility, a2 = self.min_value(state.generateSuccessor(index, a), index + 1, depth)
        if utility < high:
            high, move = utility, a
        return high, move

    def getAction(self, state):
        return self.minimax_search(state)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """

    newPosition = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    ghostDist = 0
    for ghost in currentGameState.getGhostStates():
        dist = manhattan(newPosition, ghost.getPosition())
        # Return negative if Pacman dangerously near ghost
        if dist == 0:
            return -999
        ghostDist += dist
    foodDist = 0
    if newFood.count() == 0:
        return 999
    # Sum up food distance
    for food in newFood.asList():
        foodDist += manhattan(food, newPosition)
    # Multiplying 1/ghostdist by ghostcount didn't work for some reason
    sub = 0 if ghostDist == 0 else 1 / ghostDist
    add = 0 if foodDist == 0 else (1 / foodDist) * newFood.count()
    return currentGameState.getScore() - sub + add

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
