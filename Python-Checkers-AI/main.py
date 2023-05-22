# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import multiprocessing
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from mcts.algorithm import MCTS_agent
import pandas as pd
import sys
sys.path.append('D:\XAI Process Mining Research\Python-Checkers-AI')

FPS = 60

def main(simulation_depth, minimax_depth, iterations, file_path):
    
    for i in range(1, 101):

        white_traces = { 'last_turn_enemy_piece_id': [], 'last_turn_enemy_movement': [], 'piece id': [], 'move': [], "skip": [], 'reward': [] }
        red_traces = { 'last_turn_enemy_piece_id': [], 'last_turn_enemy_movement': [], 'piece id': [], 'move': [], "skip": [], 'reward': [] }

        run = True

        game = Game(None)
        winner = None

        last_turn_enemy_piece_id = -1
        last_turn_enemy_movement = tuple()

        while run:

            if game.turn == WHITE:
                white_agent = MCTS_agent(game.get_board(), WHITE, iterations, simulation_depth, minimax_depth)
                action = white_agent.get_action()

                if action == None:
                    winner = RED
                    run = False
                    continue

                new_board, reward, next_turn, terminate, movement_info = action

                white_traces['last_turn_enemy_piece_id'].append(last_turn_enemy_piece_id)
                white_traces['last_turn_enemy_movement'].append(last_turn_enemy_movement)
                white_traces['piece id'].append(movement_info[0])
                white_traces['move'].append(movement_info[1])
                white_traces['skip'].append(movement_info[2])
                white_traces['reward'].append(reward)

                # update last_turn_enemy_piece_id
                last_turn_enemy_piece_id = movement_info[0]
                # update last_turn enemy movement
                last_turn_enemy_movement = movement_info[1]

            else:
                red_agent = MCTS_agent(game.get_board(), RED, iterations, simulation_depth, minimax_depth)
                action = red_agent.get_action()

                if action == None:
                    winner = WHITE
                    run = False
                    continue

                new_board, reward, next_turn, terminate, movement_info = action

                red_traces['last_turn_enemy_piece_id'].append(last_turn_enemy_piece_id)
                red_traces['last_turn_enemy_movement'].append(last_turn_enemy_movement)
                red_traces['piece id'].append(movement_info[0])
                red_traces['move'].append(movement_info[1])
                red_traces['skip'].append(movement_info[2])
                red_traces['reward'].append(reward)

                # update last_turn_enemy_piece_id
                last_turn_enemy_piece_id = movement_info[0]
                # update last_turn enemy movement
                last_turn_enemy_movement = movement_info[1]

            game.ai_move(new_board)
            winner = game.winner()

            if winner:
                run = False

        print(f"episode{i} completed")
        print(f"{winner} won")
        print("-------------------------------------------------------------------------------------------")

        white_path = file_path + f"white_episode{i}.csv"
        red_path = file_path + f"red_episode{i}.csv"

        df = pd.DataFrame(white_traces)
        df.to_csv(white_path, index = False)

        df = pd.DataFrame(red_traces)
        df.to_csv(red_path, index = False)

if __name__ == "__main__":

    paths = [
            "D:/XAI Process Mining Research/Python-Checkers-AI/iterations_1000/", 
            "D:/XAI Process Mining Research/Python-Checkers-AI/iterations_2000/", 
            "D:/XAI Process Mining Research/Python-Checkers-AI/iterations_3000/", 
            ]


        # creating processes
    ''' Note: (10, ) 是tuple, (10) 是 int '''

    # main(30, 6, 2000, "D:/XAI Process Mining Research/Python-Checkers-AI/iterations_2000/")

    p1 = multiprocessing.Process(target = main, args=(30, 3, 1000, paths[0]))
    p2 = multiprocessing.Process(target = main, args=(30, 3, 2000, paths[1]))
    p3 = multiprocessing.Process(target = main, args=(30, 3, 3000, paths[2]))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    # main(2, 4, 2, paths[0])
    print("Done!")
