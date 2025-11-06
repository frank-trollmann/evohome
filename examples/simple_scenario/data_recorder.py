
from simulation.prediction_system import Prediction_System

import pandas as pd

class Data_Recorder(Prediction_System):
    """
        Example for how a prediction system for dataset creation can be implemented.

        The dataframe recorded here has the following features:
        - weekday: the day of the week.
        - hour: the hour the data point occurred in.
        - minute: the inute the data point occurred in.
        - room_n: the value of one room (0 or 1)
    """

    def __init__(self,filename):
        self.filename = filename

    def on_simulation_start(self):
        print("simulation started")

        self.dates = []
        self.weekdays = []
        self.hours = []
        self.minutes = []
        self.rooms = [] 
        self.room_predictions = []
        for index in range(len(self.simulation.rooms)):
            self.rooms.append([])
            self.room_predictions.append([])


    def on_new_datapoint(self, time, sensor_data, prediction ):
        self.dates.append(time)
        self.weekdays.append(time.weekday())
        self.hours.append(time.hour)
        self.minutes.append(time.minute)
        for index in range(len(sensor_data)):
            self.rooms[index].append(int(sensor_data[index]))
            predicted_value = None
            if(prediction is not None):
                predicted_value = int(prediction[index])
            self.room_predictions[index].append(predicted_value)



    def on_simulation_end(self):
        print("simulation ended... storing dataframe")
        data = {"date": self.dates,
                "weekday": self.weekdays, 
                "hour": self.hours,
                "minute": self.minutes}
        for index in range(len(self.simulation.rooms)):
            data["room_" + str(index)] = self.rooms[index]
            data["prediction_" + str(index)] = self.room_predictions[index]

        data_frame = pd.DataFrame(data)

        data_frame.to_pickle(self.filename)

        print(f"Finished. Stored dataframe with {len(data_frame)} elements under: {self.filename}")
