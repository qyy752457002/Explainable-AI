# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from mcts.algorithm import MCTS_agent
import pandas as pd
import sys
sys.path.append('D:\XAI Process Mining Research\Python-Checkers-AI')

FPS = 60

# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption('Checkers')s

if __name__ == "__main__":
    
    for i in range(1, 101):

        white_traces = { 'piece id': [], 'move': [], "skip": [], 'reward': [] }
        red_traces = { 'piece id': [], 'move': [], "skip": [], 'reward': [] }

        run = True

        game = Game(None)

        winner = None

        while run:

            if game.turn == WHITE:
                white_agent = MCTS_agent(game.get_board(), WHITE)
                action = white_agent.get_action()

                if action == None:
                    winner = RED
                    run = False
                    continue

                new_board, reward, next_turn, terminate, movement_info = action

                white_traces['piece id'].append(movement_info[0])
                white_traces['move'].append(movement_info[1])
                white_traces['skip'].append(movement_info[2])
                white_traces['reward'].append(reward)

            else:
                red_agent = MCTS_agent(game.get_board(), RED)
                action = red_agent.get_action()

                if action == None:
                    winner = WHITE
                    run = False
                    continue

                new_board, reward, next_turn, terminate, movement_info = action

                red_traces['piece id'].append(movement_info[0])
                red_traces['move'].append(movement_info[1])
                red_traces['skip'].append(movement_info[2])
                red_traces['reward'].append(reward)

            game.ai_move(new_board)
            winner = game.winner()

            if winner:
                run = False

        print(f"episode{i} completed")
        print(f"{winner} won")
        print("-------------------------------------------------------------------------------------------")

        df = pd.DataFrame(white_traces)
        df.to_csv(f"D:/XAI Process Mining Research/Python-Checkers-AI/RL policy traces/white_episode{i}.csv")

        df = pd.DataFrame(red_traces)
        df.to_csv(f"D:/XAI Process Mining Research/Python-Checkers-AI/RL policy traces/red_episode{i}.csv")
