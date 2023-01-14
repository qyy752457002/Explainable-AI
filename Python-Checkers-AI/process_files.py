import pandas as pd
import os

class CSV_Processor():
    def __init__(self):
        self.white_policy_eventlog = {'task_ID':[], 'transition':[], 'skip': [], "make king": []}
        self.red_policy_eventlog = {'task_ID':[], 'transition':[], 'skip': [], "make king": []}
        self.policy_dir = "D:/XAI Process Mining Research/Python-Checkers-AI/RL policy traces"

    # for each epsidoe, we extract tasks IDs and corresponding events
    # we generate our event log through combining all epsiodes' task IDs and events 
    def process_policies(self):

        red_counter = 0
        white_counter = 0

        for file in os.listdir(self.policy_dir):
            full_path = self.policy_dir + f"/{file}"
            df = pd.read_csv(full_path)

            for tuple in df.itertuples():
                current_position = tuple[2]
                next_position = tuple[3]
                skip = tuple[4]
                reward = tuple[5]

                if reward % 10 == 0:
                    king = False
                elif reward % 4 == 0:
                    king = True

                transistion = (current_position, next_position, skip, king)

                if "red" in file:
                    self.red_policy_eventlog['task_ID'].append(red_counter)
                    self.red_policy_eventlog['transition'].append(transistion)
                    red_counter += 1

                elif "white" in file:
                    self.white_policy_eventlog['task_ID'].append(white_counter)
                    self.white_policy_eventlog['transition'].append(transistion)
                    white_counter += 1                  

        df = pd.DataFrame(self.white_policy_eventlog)
        df.to_csv(f"D:/XAI Process Mining Research/Taxi Environment/RL policy event log/white_policy_eventlog.csv")

        df = pd.DataFrame(self.red_policy_eventlog)
        df.to_csv(f"D:/XAI Process Mining Research/Taxi Environment/RL policy event log/red_policy_eventlog.csv")