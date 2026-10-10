
from simulation.learning_system.prediction_system import Prediction_System

import pandas as pd

from sklearn import tree

class Room_Predictor():
    """
        Prediction example for a specific room.
        
    """

    def __init__(self,room_name):
        """
            constructor
            
            Args:
                room_name (string): the name of the room this adaptation controller is targeting
        """
        self.room_name = room_name



    def train_model(self, X, y):
        """
            train the model on a provided dataset

             Args:
                X (dataframe): A dataframe containing the training features. The model expects the features "weekday", "hour", and "minute"]
                y (dataframe): A dataframe containing the training labels. The model expects a one-dimensional output consistent with binary classification
        """
        self.model = tree.DecisionTreeClassifier()
        self.model.fit(X.values,y)
        


    def predict_presence(self, time):
        """
            predict the presence for a point in time.
        """
        weekday = time.weekday()
        hour = time.hour
        minute = time.minute 
        prediction = self.model.predict([[weekday, hour, minute]])
        return prediction[0]

       
