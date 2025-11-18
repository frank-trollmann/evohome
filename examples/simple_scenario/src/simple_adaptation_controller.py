
import pandas as pd
from sklearn import tree

from simulation.learning_system.adaptation_controller import Adaptation_Controller

class Simple_Adaptation_Controller(Adaptation_Controller):
    """
        Example for how a an adaptation controller can be implemented.
        This adaptation controller simply retrains the prediction every week.
    """

    def on_simulation_start(self):
        file_name = "examples/simple_scenario/data/recording.pickle"
        data_frame = pd.read_pickle(file_name)
        training_features = ["weekday","hour", "minute"]
        predicted_features = []
        for index in range(len(self.simulation.rooms)):
            predicted_features.append("room_" + str(index))

        # create initial x and y
        self.X = data_frame[training_features]
        self.Y = data_frame[predicted_features]

        self.substituted_index = 0

        
        


    def on_new_prediction(self, time, y, y_pred, prediction_time):
        """
            This function is implemented with a very rudimentary version of the MAPE-K feedback loop where K is implemented by self.X and self.Y
        """

        self.monitor(time,y)
        needs_adaptation = self.analyze(time)
        if needs_adaptation:
            self.plan_and_execute()


    def monitor(self, time, y):
        """
            This function adds the monitored information to the dataframe and keeps a consistent dataframe length.
            For cinsistencies sake we don't add / remove data from the frame but overwrite the elements one at a time, starting with the oldest.
        """
        x_value = {"weekday": time.weekday(), "hour": time.hour, "minute": time.minute}
        self.X.iloc[self.substituted_index] = x_value

        y_value = {"room_" + str(index) : int(y[index]) for index in range(len(y))}
        self.Y.iloc[self.substituted_index] = y_value

        self.substituted_index = (self.substituted_index + 1) % len(self.X)
    
    def analyze(self, time):
        """
            Checks whether an adaptation is necessary.
            This function triggers an adaptation once every week at Monday, 0:00:00, regardless of model performance
        """
        current_time = self.simulation.current_time
        if current_time.weekday() == 0 and current_time.hour == 0 and current_time.minute == 0:
            return True
        return False
    

    def plan_and_execute(self):
        """
            deploys the trained model.
        """
        self.simulation.prediction_system.train_model(self.X, self.Y)
    

       
