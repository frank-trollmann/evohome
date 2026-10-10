
import pandas as pd
from sklearn import tree

from simulation.learning_system.adaptation_controller import Adaptation_Controller

class Room_Adaptation_Controller:
    """
        Example for how a an adaptation controller can be implemented.
        The adaptation controller retrains the model according to the two parameters ADAPTATION_ACCURACY_THRESHOLD and ADAPTATION_DAY_TOLERANCE.

        models are measured against their maximum observed accuracy.
        If they are worse than ADAPTATION_ACCURACY_THRESHOLD at the end of a day, this is counted as evidence to potentially require adaptation
        If the threshold is exceeded on three consecutive days, this triggers adaptation.
    """

    def __init__(self,room_name, predictor):
        """
            constructor
            
             Args:
                room_name (string): the name of the room this adaptation controller is targeting
                predictor (Room_Predictor): the model that does prediction for this room.
        """
        self.room_name = room_name
        self.predictor = predictor
    

    def on_simulation_start(self, X, y):
        """
            Called when simulation is started.
            Establishes the dataset and resents all important variables. 
        """
        self.X = pd.DataFrame.copy(X)
        self.Y = pd.DataFrame.copy(y)
        self.substituted_index = 0

        



    def on_new_prediction(self, time, y, y_pred):
        """
            Called when new predictions come in.
            Does housekeeping and decudes on adaptations
            Structure follows a rudimentary MAPE feedback loop.
        """
        self.monitor(time,y,y_pred)

        if(time.hour == 0 and time.minute == 0):
            needs_adaptation = self.analyze(time)
            if needs_adaptation:
                self.plan_and_execute()


    def monitor(self, time, y,y_pred):
        """
            This function adds the monitored information to the dataframe and keeps a consistent dataframe length.
            For consistencies sake we don't add / remove data from the frame but overwrite the elements one at a time, starting with the oldest.
        """
        x_value = {"weekday": time.weekday(), "hour": time.hour, "minute": time.minute}
        self.X.iloc[self.substituted_index] = x_value
        self.Y.iloc[self.substituted_index] = int(y)
        self.substituted_index = (self.substituted_index + 1) % len(self.X)

    

        
    
    def analyze(self, time):
        """
            Checks whether an adaptation is necessary.
            This function triggers an adaptation if the accuracy is consistently below the threshold.
        """
        if time.weekday() == 0 and time.hour == 0 and time.minute == 0:
            return True
        return False

    def plan_and_execute(self):
        """
            trains the model and resets prediction accuracy housekeeping variables
        """
        print("adapting room ", self.room_name)
        self.predictor.train_model(self.X, self.Y)


       
