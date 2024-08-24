# environment_manager.py
import os
import numpy as np
import pandas as pd
import gymnasium as gym

class EnvironmentManager:
    def __init__(self, world: str):
        self._load_environment(world)

    def _load_environment(self, world: str):
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, 'environments', f'{world}.csv')
        env = np.loadtxt(file_path, delimiter=';', dtype=object)
        base_shape = env.shape

        walls = np.array(['w'] * base_shape[0])
        env = np.c_[env, walls]
        env = np.c_[walls, env]
        walls = np.array([['w'] * (base_shape[1] + 2)])
        env = np.r_[env, walls]
        env = np.r_[walls, env]

        self.grid = env.T
        self._setup_observation_table()

        start_pos = np.where(env == 's')
        self.start_pos = np.array([int(start_pos[0]), int(start_pos[1])])
        end_pos = np.where(env == 't')
        self.end_pos = np.array([int(end_pos[0]), int(end_pos[1])])

    def _setup_observation_table(self):
        state_counter = 0
        self.observation_table = {}
        for x, row in enumerate(self.grid):
            for y, col in enumerate(row):
                if col != 'w':
                    self.observation_table[(x, y)] = state_counter
                    state_counter += 1
