

class Simulator_Base:

    def start_simulation(self):
        """
            This function is called when the simulation is started.
            It should reset the simulator so a new simulation can start.
        """
        pass

    def get_room_by_name(self, name):
        """
            Retrieves a room by name.
            
            :param name: the name of the room
            :return: the room with the given name
        """
        return None
    
    def get_rooms(self):
        """
            Retrieves all rooms as a list.
            :return: a list of rooms
        """
        return []
    
    def get_transitions(self):
        """
            Retrieves all transitions. 
            If there are no transitions to retrieve the default value of this function can be used.
            Expected format of transitions: A dictionary from start room name to target room.
            
            :return: a dictionary of transitions
        """
        return {}
    
    def get_start_time(self):
        """
            Retrieves the start time of the simulation.
        
            :return: the start time
        """
        return None
    
    def tick(self, current_time):
        """
            A simulation tick. Should adjust the simulated content to the provided time.
        
            :param current_time: the current time of the simulation
        """
        pass

    def get_weather_value(self):
        """
            Retrieves the current weather value.
        
            :return: the current weather value
        """
        return 0

    def get_background_image(self):
        """
            Retrieves the background image for the simulation.

            :return: the background image
        """
        return None