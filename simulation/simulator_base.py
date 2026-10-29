

class Simulator_Base:


    def start_simulation(self):
        """
            This function is called when the simulation is started.
            It should reset the simulator so a new simulation can start.
        """
        pass

    def get_room_by_name(self, name):
        """
            retrieves the room by name.

            Args:
                name (string) the name of the room

            Returns:
                Room: the room
        """
        return None
    
    def get_rooms(self):
        """
            Retrieves all rooms.

            Returns:
                list<Room>: all rooms
        """
        return []
    
    def get_transitions(self):
        """
            Retrieves all transitions.

            Returns:
                dictionary: A dictionary representation of transitions with source name (string) as key and target room (Room) as value
        """
        return {}
    
    def get_start_time(self):
        """
            Retrieves the start time of the scenario.

            Returns:
                datetime: the starting time and date
        """
        return None
    
    def tick(self, current_time):
        """
            One tick in the simulation. 
            Simulates one minute in the scenario and sets presence of persons in rooms accordingly. 

            Args:
                current_time (datetime) the current time.

        """
        pass

    def get_weather_value(self):
        """
            retrieves the weather value

            Returns:
                float: the suitability of the current weather for outside activities.
        """
        return 0

    def get_background_image(self):
        """
            Retrieves the background image of the scenario.

            Returns: 
                string: the url of the background image
        """
        return None

    def notify_visualization_refresh_needed(self):
            """
                This function can be used in the simulation to notify that an update to the visualization is needed.
                Can, for example, be used to let the visualization know that the background image / room needs to be redrawn.
            """
            pass