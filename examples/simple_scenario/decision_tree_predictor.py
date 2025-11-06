
from simulation.prediction_system import Prediction_System
from examples.simple_scenario.extended_data_recorder import Extended_Data_Recorder

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

    def on_simulation_start(self):
        print("Decision Tree Predictor: Training Model")

        # load data
        file_name = "examples/simple_scenario/data/recording.pickle"
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
        
        print("Decision Tree Predictor: Training Finished")
        


    def predict_presence(self, time):
        weekday = time.weekday()
        hour = time.hour
        minute = time.minute 
        prediction = self.model.predict([[weekday, hour, minute]])
        return prediction[0]

       
