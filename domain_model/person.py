
from domain_model.obligation import Obligation


class Person:
    """
        This class represents a person living in the house.
    """
    def __init__(self, name, ui_color, wake_up_time = None, sleep_time = None):
        """
            Constructor.
            Args:
                name (string): the name of the person.
                ui_color (string): the color used to represent this person in the user interface.
                wake_up_time (time): the time the person naturally wakes up.
                sleep_time (time): the time the person naturally goes to sleep.
        """
        self.name = name
        self.room = None
        self.ui_color = ui_color

        self.wake_up_time = wake_up_time
        self.sleep_time = sleep_time
        self.sleep_room = None
        
        self.obligations = []
        self.leisure_activities = []

    
    def move_to_room(self,new_room):
        """
            Moves the person to a new room.
            Deregisters the person from the previous room.

            Args:
                new_room (Room): the room to move to.
        """
        if self.room != None:
            self.room.persons.remove(self)
        self.room = new_room
        if new_room != None:
            new_room.persons.append(self)

    def add_obligation(self, obligation):
        """
            Adds an obligation to the person.
            
            Args:
                name (string): the name of the obligation.
                start_time (time): the start time of the obligation.
                end_time (time): the end time of the obligation.
                location (Room): the location where the obligation happens. None means the location happens outside of the house.
                weekdays (int[]): the weekdays where the obligation happens. 0 = Monday, 6 = Sunday. None means every day.
        """
        self.obligations.append(obligation)

    def add_leisure_activity(self,activity, priority):
        """
            Adds a leisure activity to the person.

            Args:
                activity (Leisure_Activity): the leisure activity to add.
                priority (int): the priority of the leisure activity. Higher priorities mean the activity will be chosen with higher probability.
        """
        self.leisure_activities.append((activity,priority))


    def remove_obligation(self, obligation_name):
        """
            Removes an obligation from the person

            Args:
                name (string): the name of the obligation to remove.
        """
        if not isinstance(obligation_name, str):
            raise Exception(f"Trying to remove a room without a valid name. Expected name of type string, found {obligation_name.type}.")


        self.obligations = [obligation for obligation in self.obligations if obligation.name != obligation_name]

    def remove_leisure_activity(self, activity_name):
        """
            Removes a leisure activity from the person.

            Args:
                name (string): the name of the leisure activity to remove.
        """
        self.leisure_activities = [activity for activity in self.leisure_activities if activity[0].name != activity_name]

    def get_leisure_activity_priority(self,activity_name):
        """
            retrieves the priority of a leisure activity
        """
        for activity_tuple in self.leisure_activities:
            if(activity_tuple[0].name == activity_name):
                return activity_tuple[1]
        raise Exception(f"Trying to retrieve priority for unkown activity.")

    def change_leisure_activity_priority(self,activity_name, new_priority):
        """
            Changes the priority of a leisure activity.
            Args:
                name (string): the name of the leisure activity to remove.

        """
        self.leisure_activities = [Person.__update_activity_priority_with_name(activity_tuple,activity_name,new_priority) for activity_tuple in self.leisure_activities]


    def __update_activity_priority_with_name(activity_tuple, the_name, new_priority):
            if(activity_tuple[0].name == the_name):
                return (activity_tuple[0],new_priority)
            return activity_tuple
