

from domain_model.obligation import Obligation


class Club :
    """
        This class represents a club.

        A club will be scheduled as obligation on a particular day of the week at a particular time in a particular room.

    """

    def __init__(self, name, day, start_time, end_time, location):
        """
            constructor.

            params:
                name (string): the name of the club
                day (int): the index of the weekday of the club (0 = Monday)
                start_time (datetime.time): the beginning of the club obligation
                end_time (datetime.time): the end of the club obligation
                location (Room): the room the club takes place in.
        """
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
            add a student to the club.
            Also adds the obligation.

            params: 
                student (Person): the student to add
        """
        if not self.paused:
            student.add_obligation(self.obligation)
        self.students.append(student)


    def remove_student(self, student):
        """
            Remove a student from the club.
            Also removes the connected obligation.

            params: 
                student (Person): the student to remove
        """
        student.remove_obligation(self.obligation.name)
        if(student in self.students):
            self.students.remove(student)

    def set_teacher(self,teacher):
        """
            Sets the teacher to supervise this activity.
            adds / removes obligation from new / old teacher.
            Setting teacher to None is interpreted as there being no supervising teacher.

            params: 
                teacher (Person): the teacher
        """
        if self.teacher is not None:
            self.teacher.remove_obligation(self.obligation.name)
        self.teacher = teacher
        
        if self.teacher is not None and not self.paused:
            self.teacher.add_obligation(self.obligation)

    def unpause(self):
        """
            Unpause the club after semester vacation.
        """
        self.paused = False
        for student in self.students:
            student.add_obligation(self.obligation)
        if self.teacher is not None:
            self.teacher.add_obligation(self.obligation)

    def pause(self):
        """
            Pause the club at the beginning of semester vacation.
        """
        self.paused = True
        for student in self.students:
            student.remove_obligation(self.obligation.name)
        if self.teacher is not None:
            self.teacher.remove_obligation(self.obligation.name)

    