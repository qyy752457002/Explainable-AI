import random
from math import sqrt
from numpy import log as ln
from copy import deepcopy
import sys
import threading
import concurrent.futures

sys.path.append('D:\XAI Process Mining Research\Python-Checkers-AI')

RED = (255,0,0)
WHITE = (255, 255, 255)

from checkers.constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE

class TreeNode():
    def __new__(cls, *args, **kwargs):
        return super(TreeNode, cls).__new__(cls)
    
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
    def __new__(cls, *args, **kwargs):
        return super(MCTS_agent, cls).__new__(cls)
    
    def __init__(self, board, agent_color, exploration_constant = 1/sqrt(2), discounted_factor = 0.6):
        self.board = board
        self.agent_color = agent_color
        self.exploration_constant = exploration_constant
        self.discounted_factor = discounted_factor

    def get_action(self):

        def thread_task(lock, node):

             for _ in range(400):
                 lock.acquire()
                 selected_node = self.selection(node)
                 expanded_node = self.expansion(selected_node)
                 lock.release()

                 reward = self.simulation(expanded_node)

                 lock.acquire()
                 self.backpropagation(selected_node, reward)
                 lock.release()

        node = TreeNode(self.board, self.agent_color, False, None)
        lock = threading.Lock()

        # create a thread pool with 2 threads
        pool = concurrent.futures.ThreadPoolExecutor(max_workers = 10)

        # submit tasks to the pool
        pool.submit(thread_task(lock, node))
        pool.submit(thread_task(lock, node))
        pool.submit(thread_task(lock, node))
        pool.submit(thread_task(lock, node))
        pool.submit(thread_task(lock, node))
        pool.submit(thread_task(lock, node))
        pool.submit(thread_task(lock, node))
        pool.submit(thread_task(lock, node))
        pool.submit(thread_task(lock, node))
        pool.submit(thread_task(lock, node))

        # # wait for all tasks to complete
        pool.shutdown(wait = True)

        best_node = self.choose_best_node(node)
        return node.children.get(best_node)

    def selection(self, node):

        while not node.terminate:
            # expand the node if the node is not fully expanded
            if not node.isFullyExpanded:
                # return the selected node
                return node
            # if the current node is fully expanded, apply UCT to find next node to check
            else:
                node = self.choose_best_node(node)

    def expansion(self, node):
        
        # get all legal moves of current node
        moves = self.get_moves(node)

        # get all pruned moves
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
        # add new node to current node's children
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

            # set simulation depth to 20
            depth += 1
            if depth == 20:
                break

        return reward

    def backpropagation(self, node, reward):

        while node:
            node.visits += 1
            node.reward[0] = reward[0] + self.discounted_factor*node.reward[0]
            node.reward[1] = reward[1] + self.discounted_factor*node.reward[1]
            node = node.parent

    def choose_best_node(self, node):

        best_nodes = []
        best_value = float("-inf")

        children_nodes = list(node.children.keys())

        if node.turn == WHITE:
            # Apply UCT
            for child in children_nodes:

                if child.visits == 0:
                    child_value = 0 
                else:
                    exploit = child.reward[0] / child.visits
                    explore = sqrt(2 * ln(node.visits) / child.visits)

                    child_value = exploit + explore

                if child_value > best_value:
                    best_value = child_value
                    best_nodes = [child]

                elif child_value == best_value:
                    best_nodes.append(child)
                
        elif node.turn == RED:
            # Apply UCT
            for child in children_nodes:

                if child.visits == 0:
                    child_value = 0 
                else:
                    exploit = child.reward[0] / child.visits
                    explore = sqrt(2 * ln(node.visits) / child.visits)

                    child_value = exploit + explore

                if child_value > best_value:
                    best_value = child_value
                    best_nodes = [child]

                elif child_value == best_value:
                    best_nodes.append(child)

        return random.choice(best_nodes)
        
    def get_moves(self, node):

        moves = []

        # iterate over every single piece in the game board
        for piece in node.board.get_all_pieces(node.turn):
            # get all possible moves based on current piece
            valid_moves = node.board.get_valid_moves(piece)

            for move_, skip in valid_moves.items():
                # make a deepcopy of the board
                temp_board = deepcopy(node.board)
                # get the temp piece from the temp_board
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                # move the piece to the target position
                temp_board.move(temp_piece, move_[0], move_[1])

                # get the reward on the current temp board
                reward = temp_board.get_reward()

                if skip:
                    temp_board.remove(skip)
                    reward += len(skip) * 20

                # get removed piece id if the removed piece exists
                removed_piece_id = [p.id for p in skip]

                cur_x, cur_y = piece.row, piece.col
                target_x, target_y = move_[0], move_[1]

                dx = target_x - cur_x
                dy = target_y - cur_y

                move = None

                if dx > 0 and dy > 0:
                    move = ("right", "up")
                elif dx < 0 and dy > 0:
                    move = ("left", "up")
                elif dx < 0 and dy < 0:
                    move = ("left", "down")
                elif dx > 0 and dy < 0:
                    move = ("right", "down")

                # piece id, move, skip
                movement_info = (temp_piece.id, move, removed_piece_id)

                if node.turn == RED:
                    next_turn = WHITE
                else:
                    next_turn = RED

                if temp_board.winner():
                    terminate = True
                else:
                    terminate = False 

                moves.append((temp_board, reward, next_turn, terminate, movement_info))

        return moves
