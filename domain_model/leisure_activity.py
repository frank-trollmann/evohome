
import random


class Leisure_Activity:
    """
        This class represents a leisure activity and associated preferences.
        Leisure activities will be selected randomly according to their weight whenever a simulated person has free time. 
    """
    def __init__(self, name, location_options = None, weekdays = None, min_duration = 1, max_duration = -1, required_ressources = []):
        """
            Constructor.

            Args:
                name (string): the name of the activity.
                location_options (List<Room>): a list of possible locations to choose from. If this is None, the activity is interpreted to happen outside the simulated house
                weight (int): the weight of the activity. Activities with greater weight are more likely to be chosen.
                weekdays (int[]): the weekdays where the obligation happens. 0 = Monday, 6 = Sunday. None means every day.
                min_duration (int): the minimum duration of the activity in minutes.
                max_duration (int): the maximum duration of the activity in minutes. -1 means no maximum.
                required_ressources (List<String>): the ressources required to perform this activity.

        """
        self.name = name
        self.location_options = location_options
        self.weekdays = weekdays
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.required_ressources = set(required_ressources)

    def is_available(self,date):
        """
            Checks whether the activity is currently available
            
            Args:
                date (datetime): the date to execute the activity on.

            Returns:
                bool: True if the date is a day of the week where this obligation happens.
        """
        weekday = date.weekday()
        if self.weekdays is not None and weekday not in self.weekdays:
            return False

        if not self.__valid_location_exists() :
            return False
        
        return True


    def get_location(self):
        """
            returns the location for this activity.
            Chooses an appropriate location according to the required ressources if no location is set.
        """

        # case A: return None if no location options are set
        if self.location_options is None:
            return None

        # case B: choose randomly among all location options
        valid_locations = []
        for location in self.location_options:
            if location.ressources_available(self.required_ressources):
                valid_locations.append(location)

        if len(valid_locations) > 0:
            return random.choice(valid_locations)
        else:
            return None

    
    def calculate_duration(self):
        """
            Calculates a random duration of this activity. 
            The duration will be between self.min_duration and self.max_duration.
            If self.max_duration is not set, this will return -1 (to be interpreted as running indefinitely.)
        """
        if self.max_duration <=0:
            return -1
        min_duration = max(self.min_duration,1)
        return random.randint(min_duration, self.max_duration)
    
    def start_activity(self, location):
        """
            Called when starting the activity.
            Does busywork, such as blocking required ressources
        """
        if location is not None:
            location.block_ressources(self.required_ressources)

    def end_activity(self, location):
        """
            Called when ending the activity.
            Does busywork, such as releasing required ressources
        """
        if location is not None:
            location.release_ressources(self.required_ressources)


    def __valid_location_exists(self):
        """
            checks if a valid location for this activity exists.
            If a location is set, it is checked for ressource availability.
            If the location is not set, all locations are checked for ressource availability
        """
        # case A: no options set is interpreted as outside, which is always valid
        if self.location_options is None:
            return True

        # case B: options set: check that there is at least one option with the required ressources
        for room in self.location_options:
            if room.ressources_available(self.required_ressources):
                return True
        return False
