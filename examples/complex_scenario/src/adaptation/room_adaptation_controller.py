
from collections import deque

import pandas as pd
from sklearn import tree

from simulation.learning_system.adaptation_controller import Adaptation_Controller

class Room_Adaptation_Controller:
    """
        Example for how a an adaptation controller can be implemented.
        This implementation checks for adaptation need once per week and retrains this model if it's accuracy is smaller than 0.9
    """


    def __init__(self,room_name, room_index, predictor):
        """
            Constructor
            
             Args:
                room_name (string): the name of the room this adaptation controller is targeting
                predictor (Room_Predictor): the model that does prediction for this room.
        """
        self.room_name = room_name
        self.room_index = room_index
        self.predictor = predictor
        self.accuracy_threshold = 0.9
    

    def on_simulation_start(self, X, y):
        """
            Called when simulation is started.
            Establishes the dataset and resents all important variables. 
        """
        self.X_que = deque(X.to_dict(orient="records"))
        self.Y_que = deque(y.to_list())
        self.correct_prediction_count = 0

    

    def on_new_prediction(self, time, y, y_pred):
        """
            Called when new predictions come in.
            Does housekeeping and decudes on adaptations
            Structure follows a rudimentary MAPE feedback loop.
        """
        self.monitor(time,y,y_pred)

        if time.weekday() == 0 and time.hour == 0 and time.minute == 0:
            needs_adaptation = self.analyze(time)
            if needs_adaptation:
                self.plan_and_execute()


    def monitor(self, time, y,y_pred):
        """
            This function adds the monitored information to the dataframe and keeps a consistent dataframe length.
            For consistencies sake we don't add / remove data from the frame but overwrite the elements one at a time, starting with the oldest.
        """
        self.X_que.append({"weekday": time.weekday(), "hour": time.hour, "minute": time.minute})
        self.X_que.popleft()
        self.Y_que.append(int(y))
        self.Y_que.popleft()
        self.correct_prediction_count += y == y_pred
    

        
    def analyze(self, time):
        """
            Checks whether an adaptation is necessary.
            This function triggers an adaptation if the accuracy is consistently below the threshold.

            Args:
                time (datetime): the time of the data point.

            Returns:
                True if an adaptation should take place. False otherwise
        """

        nr_predictions_in_week = 60*24*7
        accuracy = self.correct_prediction_count / nr_predictions_in_week
        self.correct_prediction_count = 0
        
        return self.accuracy_threshold > accuracy


    def plan_and_execute(self):
        """
            trains the model and resets prediction accuracy housekeeping variables
        """
        X = pd.DataFrame(self.X_que)
        Y = pd.DataFrame(list(self.Y_que))
        self.predictor.train_model(X, Y)


       
