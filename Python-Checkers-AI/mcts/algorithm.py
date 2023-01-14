import random
from math import sqrt
from numpy import log as ln
from copy import deepcopy
import sys
sys.path.insert(0, "D:\XAI Process Mining Research\Python-Checkers-AI")
import time

THINKTIME = 20

RED = (255,0,0)
WHITE = (255, 255, 255)

from checkers.constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE

class TreeNode():

    def __init__(self, board, turn, terminate, parent):
        self.board = board
        self.turn = turn
        self.terminate = terminate
        self.parent = parent
        self.children = {}
        self.visits = 0
        self.reward = [0, 0] # reward[0] for white # reward[1] for red
        self.isFullyExpanded = False
        
class MCTS_agent():

    def __init__(self, board, agent_color, exploration_constant = 1/sqrt(2)):
        self.board = board
        self.agent_color = agent_color
        self.exploration_constant = exploration_constant

    def get_action(self):

        node = TreeNode(self.board, self.agent_color, False, None)

        start_time = time.time()

        while time.time() - start_time < THINKTIME:
            
            new_node = self.selection(node)
            if new_node is None:
                break
            else:
                reward = self.simulation(new_node)
                self.backpropagation(new_node, reward)

        best_node = self.choose_best_node(node)

        return node.children.get(best_node)

    def selection(self, node):
        while not node.terminate:
            # expand the node if the node is not fully expanded
            if not node.isFullyExpanded:
                return self.expansion(node)
            # if the current node is fully expanded, apply UCB1 to find next node to check
            else:
                node = self.choose_best_node(node)

        return node

    def expansion(self, node):
        # get all legal moves of current node
        moves = self.get_moves(node)
        
        if not moves:
            return None

        # get pruned moves
        pruned_moves = []

        for move in moves:
            if move not in node.children.values():
                pruned_moves.append(move)

        # randomly choose a pruned move
        move = random.choice(pruned_moves)
        # generate the next game state
        board, reward, next_turn, terminate, movement_info = move
        # create a new node for the next state
        new_node = TreeNode(board, next_turn, terminate, node)
        # add new node and the move to new node as current node's child
        node.children[new_node] = move

        # check whether the current node is fully expanded
        if len(node.children) == len(moves):
            node.isFullyExpanded = True

        return new_node

    def simulation(self, node):
        # white, red
        reward = [0, 0]

        depth = 0

        while not node.terminate:
            # generate moves
            moves = self.get_moves(node)
            if not moves:
                break
            else:
                # choose a move
                move = random.choice(moves)
                # generate the next game state
                board, r, next_turn, terminate, movement_info = move
                # count reward
                if node.turn == WHITE:
                    reward[0] += r
                else:
                    reward[1] += r
                # create a new node for the next state
                node = TreeNode(board, next_turn, terminate, node)

                depth += 1
                if depth == 10:
                    break

        return reward

    def backpropagation(self, node, reward):

        while node != None:
            node.visits += 1
            node.reward[0] += reward[0]
            node.reward[1] += reward[1]
            node = node.parent

    def choose_best_node(self, node):

        best_nodes = []
        best_value = float("-inf")

        if node.turn == WHITE:
            # Apply UCB1
            for child in node.children.keys():
                node_value = child.reward[0] + (2 * self.exploration_constant * sqrt(2 * ln(node.visits) / child.visits))

                if node_value > best_value:
                    best_value = node_value
                    best_nodes = [child]
                elif node_value == best_value:
                    best_nodes.append(child)

        elif node.turn == RED:
            # Apply UCB1
            for child in node.children.keys():
                node_value = child.reward[1] + (2 * self.exploration_constant * sqrt(2 * ln(node.visits) / child.visits))

                if node_value > best_value:
                    best_value = node_value
                    best_nodes = [child]
                elif node_value == best_value:
                    best_nodes.append(child)

        return random.choice(best_nodes)

    def get_moves(self, node):

        moves = []

        for piece in node.board.get_all_pieces(node.turn):
            valid_moves = node.board.get_valid_moves(piece)

            for move_, skip in valid_moves.items():
                temp_board = deepcopy(node.board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                reward = temp_board.move(temp_piece, move_[0], move_[1])

                if skip:
                    temp_board.remove(skip)
                    reward += len(skip) * 40

                # piece, current position, target position, skip
                movement_info = (temp_piece, (piece.row, piece.col), move_, skip)

                if node.turn == RED:
                    next_turn = WHITE
                else:
                    next_turn = RED

                if temp_board.winner() != None:
                    terminate = True
                else:
                    terminate = False 

                moves.append((temp_board, reward, next_turn, terminate, movement_info))

        return moves








