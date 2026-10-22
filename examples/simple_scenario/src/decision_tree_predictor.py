
from simulation.learning_system.prediction_system import Prediction_System

import pandas as pd

from sklearn import tree

class Decision_Tree_Predictor(Prediction_System):
    """
        Example for how a prediction system for dataset creation can be implemented.

        The prediction system here is based on a decision tree that predicts the occupancy of all rooms concurrently based on the following input features:
        - weekday: the day of the week.
        - hour: the hour the data point occurred in.
        - minute: the inute the data point occurred in.
    """

    def on_simulation_start(self):
        """
            called when the simulation is started
        """
        print("Decision Tree Predictor: Training Model")

        file_name = "examples/simple_scenario/data/recording.pickle"
        data_frame = pd.read_pickle(file_name)
        training_features = ["weekday","hour", "minute"]
        predicted_features = [] 
        for index in range(len(self.simulation.rooms)):
            predicted_features.append("room_" + str(index))
        X = data_frame[training_features]
        y = data_frame[predicted_features]

        self.train_model(X, y)

    def train_model(self, X, y):
        """
            trains the model.

            params:
                X (Pandas.Dataframe): the input features of the model.
                y (Pandas.Dataframe): the training labels
        """
        self.model = tree.DecisionTreeClassifier()
        self.model.fit(X.values,y)
        print("Decision Tree Predictor: Training Finished")
        


    def predict_presence(self, time):
        """
            Predicts presence for one point in time.

            params: 
                time (Datetime): the time for which the model is predicting
            
            returns:
                The prediction for all rooms as a list of predictions, indexed by room number.
        """
        weekday = time.weekday()
        hour = time.hour
        minute = time.minute 
        prediction = self.model.predict([[weekday, hour, minute]])
        return prediction[0]

       
