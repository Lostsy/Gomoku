import numpy as np
from collections import defaultdict
import gomoku_util as util

class MonteCarloTreeSearchNode:
 
    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent
        self.children = []

    @property
    def untried_actions(self):
        raise NotImplementedError

    @property
    def q(self):
        raise NotImplementedError

    @property
    def n(self):
        raise NotImplementedError

    def expand(self):
        raise NotImplementedError

    def is_terminal_node(self):
        raise NotImplementedError

    def rollout(self):
        raise NotImplementedError

    def backpropagate(self, reward):
        raise NotImplementedError


    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param = 1.4):
        choices_weights = [
            (c.q / (c.n)) + c_param * np.sqrt((2 * np.log(self.n) / (c.n)))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):        
        return possible_moves[np.random.randint(len(possible_moves))]

class Gomoku_MCTS(MonteCarloTreeSearchNode):
    # TODO implement UCB with Progressive bias
    # TODO implement Heuristic function for selecting unvisited nodes

    def __init__(self, state: util.Gomoku, parent):
        super(Gomoku_MCTS, self).__init__(state, parent)
        self._number_of_visits = 0.
        self._results = defaultdict(int)

    @property
    def untried_actions(self):
        if not hasattr(self, '_untried_actions'):
            # TODO implement get_legal_actions method for Gomuku Class
            self._untried_actions = self.state.get_legal_actions() 
        return self._untried_actions

    @property
    def q(self):
        # TODO this function needs to be thoroughly rewritten
        wins = self._results[self.parent.state.next_to_move]
        loses = self._results[-1 * self.parent.state.next_to_move]
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.state.make_move(action)
        child_node = Gomoku_MCTS(next_state, parent = self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_end()

    def rollout(self):
        current_rollout_state = self.state
        while not current_rollout_state.is_end():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.make_move(action)
        return current_rollout_state.game_result

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

class MonteCarloTreeSearch:

    def __init__(self, node: MonteCarloTreeSearchNode):
        self.root = node


    def best_action(self):
        while self.stop_condition():
            v = self.tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        # exploitation only
        return self.root.best_child(c_param = 0.)


    def tree_policy(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node
    
    def stop_condition(self):
        # TODO return False when there is not enough time or space
        return False
