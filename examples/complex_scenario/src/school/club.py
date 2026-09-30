

from domain_model.obligation import Obligation


class Club :
    """
        This class represents a club.
        A club is always scheduled on a particular day of the week at a particular time in a particular room.

    """

    def __init__(self, name, day, start_time, end_time, location):
        self.name = name
        self.students = []
        self.teacher = None
        self.paused = False


        self.obligation = Obligation(name, 
                                start_time= start_time, 
                                end_time = end_time, 
                                location = location, 
                                weekdays = [day])

    def add_student(self,student):
        """
            add a student to the club
            Also adds the obligation
        """

        if not self.paused:
            student.add_obligation(self.obligation)
        self.students.append(student)


    def remove_student(self, student):
        """
            remove a student from the club
            Also removes the connected obligation
        """
        student.remove_obligation(self.obligation.name)
        if(student in self.students):
            self.students.remove(student)

    def set_teacher(self,teacher):
        """
            sets the teacher to supervise this activity.
            adds / removes obligation from new / old teacher.
            Setting teacher to None is interpreted as there being no supervising teacher.
        """
        if self.teacher is not None:
            self.teacher.remove_obligation(self.obligation.name)
        self.teacher = teacher
        
        if self.teacher is not None and not self.paused:
            self.teacher.add_obligation(self.obligation)

    def unpause(self):
        self.paused = False
        for student in self.students:
            student.add_obligation(self.obligation)
        if self.teacher is not None:
            self.teacher.add_obligation(self.obligation)

    def pause(self):
        self.paused = True
        for student in self.students:
            student.remove_obligation(self.obligation.name)
        if self.teacher is not None:
            self.teacher.remove_obligation(self.obligation.name)

    