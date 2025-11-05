
from simulation.prediction_system import Prediction_System
from examples.data_recording.data_recorder import Data_Recorder

import pandas as pd

from sklearn import tree

class Decision_Tree_Predictor(Prediction_System):
    """
        Example for how a prediction system for dataset creation can be implemented.
        TODO: implemnt correctly!
        
        The dataframe recorded here has the following features:
        - weekday: the day of the week.
        - hour: the hour the data point occurred in.
        - minute: the inute the data point occurred in.
        - room_n: the value of one room (0 or 1)
    """

    def __init__(self, record_data):
        if(record_data):
            self.data_recorder = Data_Recorder("examples/data_recording/data/running.pickle")
        else:
            self.data_recorder = None

    def set_simulation(self, simulation):
        super().set_simulation(simulation)
        if(self.data_recorder is not None):
            self.data_recorder.set_simulation(simulation)


    def on_new_datapoint(self, time, sensor_data, prediction ):
        if self.data_recorder is not None:
            self.data_recorder.on_new_datapoint(time, sensor_data, prediction)


    def on_simulation_start(self):
        if self.data_recorder is not None:
            self.data_recorder.on_simulation_start()

        print("simulation started. Training Model.")

        # load data
        file_name = "examples/data_recording/data/recording.pickle"
        data_frame = pd.read_pickle(file_name)
        training_features = ["weekday","hour", "minute"]
        predicted_features = []
        for index in range(len(self.simulation.rooms)):
            predicted_features.append("room_" + str(index))

        # train model
        X = data_frame[training_features]
        y = data_frame[predicted_features]
        self.model = tree.DecisionTreeClassifier()
        self.model.fit(X.values,y)
        
        print("Model trained.")



    def predict_presence(self, time):
        weekday = time.weekday()
        hour = time.hour
        minute = time.minute 
        prediction = self.model.predict([[weekday, hour, minute]])
        return prediction[0]


    def on_simulation_end(self):
        if self.data_recorder is not None:
            self.data_recorder.on_simulation_end()

        print("simulation ended.")
       
