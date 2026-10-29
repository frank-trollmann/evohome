
import pygame
from copy import copy, deepcopy
from datetime import timedelta
from collections import deque
from timeit import default_timer as timer

from simulation.learning_system import adaptation_metadata
from simulation.random_generator import Simulation_Random_Generator
from view.main_window import Main_window

class Simulation:
    """
        Main Simulation class.

        A simulation can be configured in several ways:
        - It can be run with or without user interface (parameter display_user_interface)
        - A simulator needs to be attached (set_simulator()) for the simulation to work.
        - An optional data recorder can be attached (set_data_recorder()) for the simulation to record data into a dataset
        - An optional prediction system can be attached (set_prediction_system()) for the simulation to predict presence.
        - An optional adaptation controller can be attached (set_adaptation_controller()) for the simulation to adapt the prediction system.

    """

    def __init__(self, display_user_interface = True, max_simulated_minutes = -1, prediction_delay_in_min = 0, random_seed = None):
        """
            Constructor.

            Args:
                display_user_interface (bool): if true, a Pygame user interface is attached.
                max_simulated_minutes (int): the number of simulation steps before the simulation terminates. 
                prediction_delay_in_min (int): how many minutes ahead the prediction is made. A value of 60 means the simulation predicts for a moment one hour into the future.
                random_seed (int): A random seed can be specified for reproducability.
        """
        self.delta_time = timedelta(minutes= 1)
        self.display_user_interface = display_user_interface
        self.max_simulated_minutes = max_simulated_minutes;

        self.running = False
        self.paused = False

        self.current_time = None
        self.predictions = deque()
        self.prediction_metadata = deque()

        self.prediction_system = None
        self.adaptation_controller = None
        self.data_recorder = None

        self.simulator = None

        self.window = None

        self.tick_count = 0
        self.prediction_delay_in_min = prediction_delay_in_min

        if random_seed is not None:
            Simulation_Random_Generator._generator.seed(random_seed)
    
    def get_current_prediction(self):
        """
            returns the prediction for the current time step.

            Returns:
                list<bool>: predictions for the current time step. None if there is no predictor, or if prediction_delay_in_mins is not exceeded yet.
        """
        if self.tick_count < self.prediction_delay_in_min:
            return None
        if len(self.predictions) == 0:
            return None
        return self.predictions[0]

    def get_current_prediction_metadata(self):
        """
            Returns the metadate of the prediction for the current time step.

            Returns:
                list<Prediction_Metadata>: metadate for the prediction of the current time step. None if there is no predictor, or if prediction_delay_in_mins is not exceeded yet.

        """
        if self.tick_count < self.prediction_delay_in_min:
            return None
        if len(self.prediction_metadata) == 0:
            return None
        return self.prediction_metadata[0]
    
    def pause(self):
        """
            Pauses the simulation after the current tick.
        """
        self.paused = True
    
    def resume(self):
        """
            Resumes the simulation, if paused.
        """
        self.paused = False
    
    def is_paused(self):
        """
            checks whether the simulation is currently paused. 

            Returns:
                bool: true if the simulation is paused.
        """
        return self.paused

    def set_simulator(self, simulator):
        """
            Sets the simulator for determining room occupation.

            Params:
                simulator (Simulator_Base): The simulator.
        """
        self.simulator = simulator

    def set_prediction_system(self,prediction_system):
        """
            Sets the prediction system to predict occupation in all rooms.

            Params:
                prediction_system (Prediction_System): the prediction system.
        """
        self.prediction_system = prediction_system
        self.prediction_system.set_simulation(self)

    def set_adaptation_controller(self, adaptation_controller):
        """
            Sets the adaptation controller to update the prediction system.

            Params:
                adaptation_controller (Adaptation_Controller): the adaptation controller.
        """
        self.adaptation_controller = adaptation_controller
        self.adaptation_controller.set_simulation(self)

    def set_data_recorder(self, data_recorder):
        """
            Sets the data recorder for the simulation. The data recorder will be notified of occupation, and prediction data and record them.

            Params:
                data_recorder (Data_Recorder): the data recorder
        """
        self.data_recorder = data_recorder
        self.data_recorder.set_simulation(self)

    def start(self):
        """
            Starts the simulation.
            The simulation loop runs synchronously in this method. 
            This method will terminate once the simulation is finished.
        """
        if self.simulator is None:
            raise Exception("Trying to simulate without a valid simulator. Did you forget to set a simulator?")

        # initialize simulator
        self.simulator.start_simulation()
        self.rooms = self.simulator.get_rooms()
        self.current_time = self.simulator.get_start_time()
        self.predicted_time = copy(self.current_time) + timedelta(minutes=self.prediction_delay_in_min)

        # show window if needed.
        if self.display_user_interface:
            self.window = Main_window(self)

        # start prediction, recoding and adaptation hooks
        if self.prediction_system is not None:
            self.prediction_system.on_simulation_start()

        if self.adaptation_controller is not None:
            self.adaptation_controller.on_simulation_start()
        
        if self.data_recorder is not None:
            self.data_recorder.on_simulation_start()

        # run simulation
        self.tick_count = 0
        self.running = True
        while self.running:
            if not self.paused:

                if(self.current_time.hour == 0 and self.current_time.minute == 0):
                    print("starting day:", f"{self.current_time.day}.{self.current_time.month}.{self.current_time.year}")

                tick_start_time = timer()
                self.simulator.tick(self.current_time)
                tick_time = timer() - tick_start_time

                prediction_time = 0
                # update prediction forecast
                if self.prediction_system is not None:
                    start_time = timer()
                    self.prediction_system.on_new_datapoint(copy(self.current_time),self.__get_sensor_values())
                    prediction = self.prediction_system.predict_presence(self.predicted_time)
                    prediction_time = timer() - start_time
                    prediction_metadata = self.prediction_system.get_last_prediction_metadata()
                    prediction_metadata.prediction_time = prediction_time
                    self.predictions.append(prediction)
                    self.prediction_metadata.append(prediction_metadata)
                
                # forward information to adaptation controller
                adaptation_time = -1
                adaptation_metadata = None
                if self.adaptation_controller is not None:
                    prediction = self.get_current_prediction()
                    if(prediction is not None):
                        prediction_metadata = self.get_current_prediction_metadata()
                        data_point = self.__get_sensor_values()
                        start_time = timer()
                        self.adaptation_controller.on_new_prediction(copy(self.current_time), data_point, prediction, prediction_metadata)
                        adaptation_time = timer() - start_time
                        adaptation_metadata = self.adaptation_controller.get_last_adaptation_metadata()
                        adaptation_metadata.adaptation_time = adaptation_time

                # update data recorder
                if self.data_recorder is not None:
                    data_point = self.__get_sensor_values()
                    prediction = self.get_current_prediction()
                    prediction_metadata = self.get_current_prediction_metadata()
                    self.data_recorder.on_new_datapoint(copy(self.current_time),data_point, prediction, self.simulator.get_weather_value(), prediction_metadata, adaptation_metadata)

                # update list of predictions
                if(len(self.predictions) > self.prediction_delay_in_min + 1):
                        self.predictions.popleft()
                        self.prediction_metadata.popleft()

                self.current_time = self.current_time + self.delta_time
                self.predicted_time = self.predicted_time + self.delta_time


                #print(f"Times: {tick_time*1000} {prediction_time*1000} {adaptation_time*1000}")

            # update GUI
            if(self.display_user_interface):
                self.window.update_content()
                self.window.handle_events()
                self.window.frame_pause()
                if self.window.end_selected:
                    self.__on_end()
                    self.window = None

            # end condition
            self.tick_count += 1
            if self.max_simulated_minutes > 0 and self.tick_count >= self.max_simulated_minutes:
                self.__on_end()

    def notify_visualization_refresh_needed(self):
        """
            Can be used to notify the simulation of changes that require a user interface refresh.
            Example: adding rooms or transitions requires redrawing the room graph.
        """
        if self.window is not None:
            self.window.refresh_house_background()


    def __on_end(self):
        """
            Ends the simulation.
        """
        if(self.prediction_system != None):
            self.prediction_system.on_simulation_end()

        if self.data_recorder != None:
            self.data_recorder.on_simulation_end()

        if(self.display_user_interface):
                pygame.quit()

        self.running = False

    def __get_sensor_values(self):
        """
            Retrieves the current sensor values for the simulation.
        """
        sensor_values = []
        for room in self.rooms:
            sensor_values.append(bool(room.persons))
        return sensor_values

