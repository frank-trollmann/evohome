
from simulation.learning_system.data_recorder import Data_Recorder

import pandas as pd

class Extended_Data_Recorder(Data_Recorder):
    """
        Extended data recorder. In addition to the base implementation, this data recorder keeps track of the following features:
        - weekday: the day of the week.
        - hour: the hour the data point occurred in.
        - minute: the inute the data point occurred in.
    """

    def on_simulation_start(self):
        """
            Called when the simulation is started
        """
        super().on_simulation_start()
        self.weekdays = []
        self.hours = []
        self.minutes = []
        
    def on_new_datapoint(self, time, sensor_data, prediction, weather, prediction_metadata, adaptation_metadata):
        """
            Records a new data point.

            Args:
                time (Datetime): the moment of the datapoint
                sensor_data (List<int>): the occupancy of rooms, indexed by room number.
                prediction (List<int>): the prediction of each room, indexed by room number
                weather (float): the suitability of weather conditions for outside activities
                prediction_metadata: the metadata of predictions. In this scenario, this only contains prediction time.
                adaptation_metadata: the metadata of predictions. In this scenario, this only contains adaptation time.
        """
        super().on_new_datapoint(time, sensor_data, prediction, weather, prediction_metadata, adaptation_metadata)
        self.weekdays.append(time.weekday())
        self.hours.append(time.hour)
        self.minutes.append(time.minute)

    def compile_data(self):
        """
            Called to compile collected data into a dataset.
            This is called before storing the dataset to hard disk

            returns: the dataset to store
        """
        data = super().compile_data()
        data["weekday"] = self.weekdays
        data["hour"] = self.hours
        data["minute"] = self.minutes
        return data
