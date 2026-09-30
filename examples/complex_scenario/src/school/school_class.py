
from datetime import time

from domain_model.obligation import Obligation


class School_Class :
    """
        This class represents a class in the university and it's schedule

        The schedule is built as two-dimensional array over room names. schedule[i][j] refers to the ith day and the jth lesson block. None denotes there is no lesson.
    
    """

    LESSON_START_TIMES = [time(8,15), time(10,15), time(13,15), time(15,15)]
    LESSON_END_TIMES = [time(9,45), time(11,45), time(14,45), time(16,45)]

    def __init__(self, name):
        self.name = name
        self.students = []
        self.teacher = None
        self.schedule = [ [None for i in range(4)] for j in range(5)]
        self.lesson_obligations = []

    def set_schedule_item(self, day,time,room):
        """
            sets the schedule 
            automatically adds obligations for the schedule to all students that are currently registered.
            Setting a room of None is interpreted as there being no lesson. 
            Old obligations are cleaned up, if they exist.
        """
        self.schedule[day][time] = room
        lesson_name = f"Lesson {day},{time}"

        # cleanup old obligations
        self.lesson_obligations = [obligation for obligation in self.lesson_obligations if obligation.name != lesson_name]
        for student in self.students:
            student.remove_obligation(lesson_name)
        if(self.teacher is not None):
                        self.teacher.remove_obligation(lesson_name)


        # add new obligations if this is a valid lesson
        if(room is not None):
            lesson_obligation = Obligation(lesson_name, 
                                                    start_time= School_Class.LESSON_START_TIMES[time], 
                                                    end_time = School_Class.LESSON_END_TIMES[time],
                                                    location = room, 
                                                    weekdays = [day])
            self.lesson_obligations.append(lesson_obligation)

            for student in self.students:
                student.add_obligation(lesson_obligation)

            if(self.teacher is not None):
                self.teacher.add_obligation(lesson_obligation)

    def add_student(self, student):
        """
            adds a student to the class.
            lessons are added automatically as obligations
        """
        self.students.append(student)
        for lesson_obligation in self.lesson_obligations:
            student.add_obligation(lesson_obligation)

    def remove_student(self,student):
        """
            removes a student from the class.
            lesson obligations are cleaned up as well.
        """
        self.students.remove(student)
        for lesson_obligation in self.lesson_obligations:
            student.remove_obligation(lesson_obligation.name)

    def set_teacher(self, teacher):
        """
        sets the teacher of the class.
        Setting the teacher to None is interpreted as removing the teacher.
        Lessen obligations are added to the teacher and removed from the previous teacher.
        """
        # remove obligations from previous teacher
        if self.teacher is not None:
            for lesson_obligation in self.lesson_obligations:
                self.teacher.remove_obligation(lesson_obligation.name)

        # set new teacher, add obligations
        self.teacher = teacher
        if self.teacher is not None:
             for lesson_obligation in self.lesson_obligations:
                self.teacher.add_obligation(lesson_obligation)


