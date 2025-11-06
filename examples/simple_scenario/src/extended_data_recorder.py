
from simulation.data_recorder import Data_Recorder

import pandas as pd

class Extended_Data_Recorder(Data_Recorder):
    """
        Extended data recorder. This data recorder keeps track of teh following additional features:
        - weekday: the day of the week.
        - hour: the hour the data point occurred in.
        - minute: the inute the data point occurred in.
    """

    def on_simulation_start(self):
        super().on_simulation_start()
        self.weekdays = []
        self.hours = []
        self.minutes = []
        
    def on_new_datapoint(self, time, sensor_data, prediction ):
        super().on_new_datapoint(time, sensor_data, prediction)
        self.weekdays.append(time.weekday())
        self.hours.append(time.hour)
        self.minutes.append(time.minute)

    def compile_data(self):
        data = super().compile_data()
        data["weekday"] = self.weekdays
        data["hour"] = self.hours
        data["minute"] = self.minutes
        return data
