from domain_model.changes.scheduled_change import Scheduled_Change


class Student_Population_Change(Scheduled_Change):
    """
        This class represents a change to the student population where a number of students are removed and added.
    """
    def __init__(self, datetime, campus, nr_removed, nr_added):
        """
            Constructor.

            Args:
                datetime (datetime): the date and time when the change should be executed.
                campus (Campus): the campus to add / remove students for
                nr_removed (int): how many students to remove
                nr_added (int): how many students to add
        """
        super().__init__(datetime)
        self.campus = campus
        self.nr_removed = nr_removed
        self.nr_added = nr_added
    
    def execute(self, simulator):
        """
            sets the campus to semester vacation mode
        """
        print("Student Intake change. Current: ", len(self.campus.students), "Removing: ", self.nr_removed, "adding: ", self.nr_added)
        removed_students = self.campus.remove_students(self.nr_removed)
        for student in removed_students: 
            simulator.remove_person(student)

        added_students = self.campus.add_students(self.nr_added)
        for student in added_students:
            simulator.add_person(student)
        print("Number students after intake: ", len(self.campus.students))