# data_handler.py
import pandas as pd

class DataHandler:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Time', 'x_coord', 'y_coord'])
        self.metrics = {'success_rate': 0, 'average_time': 0}

    def record_step(self, actor_position, step):
        x, y = actor_position
        new_data = pd.DataFrame({
            'Time': [step],
            'x_coord': [int(x)],
            'y_coord': [int(y)]
        })
        self.data = pd.concat([self.data, new_data], ignore_index=True)

    def calculate_metrics(self, steps, end_pos, actor_position):
        success = actor_position.tolist() == end_pos.tolist()
        self.metrics['success_rate'] = 1 if success else 0
        self.metrics['average_time'] = steps  # Adjust calculation as needed

    def save_metrics(self, filename: str):
        metrics_df = pd.DataFrame([self.metrics])
        metrics_df.to_csv(filename, index=False)
