# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import sys
sys.path.append('D:\XAI Process Mining Research\Python-Checkers-AI')
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from mcts.algorithm import MCTS_agent
import pandas as pd

FPS = 60

# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def game(white_traces, red_traces, number):
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            white_agent = MCTS_agent(game.get_board(), WHITE)
            new_board, reward, next_turn, terminate, movement_info = white_agent.get_action()

            white_traces['piece'].append(WHITE)
            white_traces['current_position'].append(movement_info[1])
            white_traces['next_position'].append(movement_info[2])
            white_traces['skip'].append("-") if not movement_info[3] else white_traces['skip'].append(movement_info[3])
            white_traces['reward'].append(reward)

        else:
            red_agent = MCTS_agent(game.get_board(), RED)
            new_board, reward, next_turn, terminate, movement_info = red_agent.get_action()

            red_traces['piece'].append(RED)
            red_traces['current_position'].append(movement_info[1])
            red_traces['next_position'].append(movement_info[2])
            red_traces['skip'].append("-") if not movement_info[3] else red_traces['skip'].append(movement_info[3])
            red_traces['reward'].append(reward)

        game.ai_move(new_board)

        if game.winner() != None:
            run = False      

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        game.update()
    
    pygame.quit()

    df = pd.DataFrame(white_traces)
    df.to_csv(f"D:/XAI Process Mining Research/Python-Checkers-AI/RL policy traces/white_episode{number}.csv")

    df = pd.DataFrame(red_traces)
    df.to_csv(f"D:/XAI Process Mining Research/Python-Checkers-AI/RL policy traces/red_episode{number}.csv")

if __name__ == "__main__":
    
    episodes = 100

    white_traces = { 'piece': [], 'current_position': [], 'next_position': [], "skip": [], 'reward': [] }
    red_traces = { 'piece': [], 'current_position': [], 'next_position': [], "skip": [], 'reward': [] }

    for i in range(1, episodes + 1):

        run = True

        game = Game(None)

        while run:

            if game.turn == WHITE:
                white_agent = MCTS_agent(game.get_board(), WHITE)
                new_board, reward, next_turn, terminate, movement_info = white_agent.get_action()

                white_traces['piece'].append(WHITE)
                white_traces['current_position'].append(movement_info[1])
                white_traces['next_position'].append(movement_info[2])
                white_traces['skip'].append("-") if not movement_info[3] else white_traces['skip'].append(movement_info[3])
                white_traces['reward'].append(reward)

            else:
                red_agent = MCTS_agent(game.get_board(), RED)
                new_board, reward, next_turn, terminate, movement_info = red_agent.get_action()

                red_traces['piece'].append(RED)
                red_traces['current_position'].append(movement_info[1])
                red_traces['next_position'].append(movement_info[2])
                red_traces['skip'].append("-") if not movement_info[3] else red_traces['skip'].append(movement_info[3])
                red_traces['reward'].append(reward)

            game.ai_move(new_board)

            if game.winner() != None:
                run = False   

        print(f"episode{i} completed")

        df = pd.DataFrame(white_traces)
        df.to_csv(f"D:/XAI Process Mining Research/Python-Checkers-AI/RL policy traces/white_episode{i}.csv")

        df = pd.DataFrame(red_traces)
        df.to_csv(f"D:/XAI Process Mining Research/Python-Checkers-AI/RL policy traces/red_episode{i}.csv")


    
