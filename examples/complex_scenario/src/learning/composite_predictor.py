
from tornado.httputil import _FORBIDDEN_HEADER_CHARS_RE

from examples.complex_scenario.src.learning.room_predictor import Room_Predictor
from simulation.learning_system.prediction_system import Prediction_System

import pandas as pd

from sklearn import tree

class Composite_Predictor(Prediction_System):
    """
        A composite predictor delegating the training and prediction to a set of single predictors - one for each room.
        
        Each individual predictor uses the following features:
        - weekday: the day of the week.
        - hour: the hour the data point occurred in.
        - minute: the inute the data point occurred in.

    """

    def __init__(self,scenario):
        """
            constructor

            Args:
                scenario (Scenario): reference to the simulation scenario
        """
        self.scenario = scenario
        self.room_names = scenario.get_room_names()
        self.predictors = [None] * len(self.room_names)
        for room_index in range(len(self.room_names)):
            self.predictors[room_index] = Room_Predictor(self.room_names[room_index])

    def on_simulation_start(self):
        """
            Called when simulation is started.
            Loads the dataset and trains all models
        """
        # load data
        file_name = "examples/complex_scenario/data/recording.pickle"
        data_frame = pd.read_pickle(file_name)
        training_features = ["weekday","hour", "minute"]
        X = data_frame[training_features]

        room_names = self.scenario.get_room_names()
        for room_index in range(len(room_names)):
            room_key = f"room_{room_index}"
            predictor = self.predictors[room_index]
            y = data_frame[room_key]
            predictor.train_model(X,y)
             


    def predict_presence(self, time):
        """
            predicts the presence in all rooms by relegating predictions to the respective prediction functions.
        """
        predictions = [predictor.predict_presence(time) for predictor in self.predictors]
        return predictions



       
