
from copy import copy
from datetime import time
import random


from domain_model.house import House
from domain_model.leisure_activity import Leisure_Activity
from domain_model.obligation import Obligation
from domain_model.person import Person
from domain_model.room import Room


from examples.complex_scenario.src.school import school_class
from examples.complex_scenario.src.school.club import Club
from examples.complex_scenario.src.school.school_class import School_Class
import examples.complex_scenario.src.util as util

class Campus (House):
    """
        This class represents the university campus.
        This is a convenience wrapper to reduce the complexity of defining the campus scenario. 
    """

    RESSOURCE_SNACKS = "Snacks"
    RESSOURCE_KICKER = "Kicker"
    RESSOURCE_POOL = "POOL"
    RESSOURCE_AIR_HOCKEY = "Air Hockey"
    RESSOURCE_TV = "TV"


    STUDENT_VACATION_ABSENCE_PROBABILITY = 0.8


    def __init__(self, scenario, nr_students):
        super().__init__()
        self.scenario = scenario

        self.student_nr_counter = 0
        self.principal = None
        self.secretary = None
        self.students = []
        self.teachers = []
        self.classes = {"Class A": School_Class("Class A"), 
                        "Class B": School_Class("Class B"),
                        "Class C": School_Class("Class C"),
                        "Class D": School_Class("Class D")}
        self.clubs = []

        self.secretary_office = None
        self.principal_office = None
        self.dorms = {}
        self.free_dorms = []
        self.classrooms = {}
        self.bathrooms = {}
        self.seating_areas = []
        self.meeting_rooms = []
        self.leisure_rooms = []
        self.cafeteria = None
        self.library =  None
        self.school_yard =  None
        self.sports_field =  None


        self.exit_dorm_a = None
        self.exit_dorm_b_outside = None
        self.exit_dorm_b_library = None
        self.exit_lecture_wing_outside = None
        self.exit_lecture_wing_cafeteria = None
        self.exit_lecture_wing_main_exit = None
        self.exit_cafeteria_outside = None


        self._init_dorm_a()
        self._init_dorm_b()
        self._init_lecture_wing()
        self._init_library_cafeteria()
        self._init_school_yard()

        self._init_activities()
        self._schedule_classes()

        self._init_staff_obligations()
        self._init_staff()
        self._init_obligations() 
        

        for _ in range(nr_students):
            self._add_random_student()



    def set_to_semester_vacation(self):
        """
            sets the campus to semester vacation mode
        """
        self._clear_scheduled_classes()

        for club in self.clubs:
             club.pause()

        for student in self.students:
            dice_roll = random.random()
            if dice_roll < Campus.STUDENT_VACATION_ABSENCE_PROBABILITY:
                 self._set_student_to_absent(student)

        for teacher in self.teachers:
             self._set_teacher_to_absent(teacher)

        self._set_office_staff_to_vacation()

    def set_to_semester_time(self):
        """
            sets the campus to semester mode
        """
        self._schedule_classes()

        for club in self.clubs:
            club.unpause()

        for student in self.students:
            if student.sleep_room is None:
                self._set_student_to_present(student)

        for teacher in self.teachers:
                self._set_teacher_to_present(teacher)

        self._set_office_staff_to_semester_time()

    def remove_students(self, nr_students):
        """
            removes a given number of students. Students are selected randomly
            
            Args:
                nr_students (int): the number of students to be removed
            
            Returns the list of removed students
        """
        removed_students = []
        for i in range(nr_students):
            student = random.choice(self.students)
            removed_students.append(student)
            self._remove_student(student)
        return removed_students

    def add_students(self,nr_students):
        """
            removes a given number of students.
            
            Args:
                nr_students (int): the number of students to be added
            
            Returns the list of added students
        """
        added_students = []
        for i in range(nr_students):
            student = self._add_random_student()
            added_students.append(student)
        return added_students


    def _init_activities(self):
        self.bathroom_activity = Leisure_Activity("Bathroom Break", 
                                                    location_options = list(self.bathrooms.values()), 
                                                    min_duration=10, 
                                                    max_duration=20)

        self.socialize_activity = Leisure_Activity("Socialize",
                                               location_options= self.seating_areas + [self.school_yard],
                                               min_duration=10, 
                                               max_duration=60)

        tv_locations = [room for room in self.rooms.values() if room.ressources_available(set([self.RESSOURCE_TV]))]
        self.watch_tv_activity = Leisure_Activity("Watch TV",
                                                location_options= tv_locations,
                                                required_ressources= [self.RESSOURCE_TV],
                                                min_duration=30, 
                                                max_duration=120)

        pool_locations = [room for room in self.rooms.values() if room.ressources_available(set([self.RESSOURCE_POOL]))]
        self.pool_activity = Leisure_Activity("Play Pool",
                                            location_options= pool_locations,
                                            min_duration=30, 
                                            max_duration=60)

        snack_locations = [room for room in self.rooms.values() if room.ressources_available(set([self.RESSOURCE_SNACKS]))]
        self.snacking_activity = Leisure_Activity("Snacking",
                                                    location_options= snack_locations,
                                                    min_duration=30, 
                                                    max_duration=60)

        kicker_locations = [room for room in self.rooms.values() if room.ressources_available(set([self.RESSOURCE_KICKER]))]
        self.kicker_activity = Leisure_Activity("Kicker",
                                                location_options= kicker_locations,
                                                min_duration=10, 
                                                max_duration=40)

        air_hockey_locations = [room for room in self.rooms.values() if room.ressources_available(set([self.RESSOURCE_AIR_HOCKEY]))]
        self.air_hockey_activity = Leisure_Activity("Air Hockey",
                                                    location_options= air_hockey_locations,
                                                    min_duration=20, 
                                                    max_duration=50)
        
        self.meeting_activity = Leisure_Activity("Meeting",
                                                location_options= self.meeting_rooms,
                                                min_duration=30, 
                                                max_duration=180)

        self.board_gaming_activity = Leisure_Activity("Board Gaming",
                                                        location_options= self.leisure_rooms,
                                                        min_duration=40, 
                                                        max_duration=120)

        study_outside_rooms = []
        study_outside_rooms.extend(self.seating_areas)
        study_outside_rooms.extend(self.leisure_rooms)
        study_outside_rooms.extend(self.meeting_rooms)
        study_outside_rooms.append(self.library)
        study_outside_rooms.append(self.cafeteria)
        study_outside_rooms.append(self.school_yard)
        self.study_outside_activity = Leisure_Activity("Study Outside",
                                            location_options= study_outside_rooms,
                                            min_duration=30, 
                                            max_duration=120)

        self.study_library_activity = Leisure_Activity("Study Library",
                                            location_options= [self.library],
                                            min_duration=60, 
                                            max_duration=180)

        self.basketball_activity = Leisure_Activity("Basket Ball",
                                            location_options= [self.sports_field],
                                            min_duration=60, 
                                            max_duration=180)

        self.cinema_activity = Leisure_Activity("Cinema",
                                                    location_options= None,
                                                    min_duration=120, 
                                                    max_duration=180)
        
        self.shopping_activity = Leisure_Activity("Shopping",
                                                            location_options= None,
                                                            min_duration=60, 
                                                            max_duration=90)

    def _init_staff_obligations(self):
        self.teacher_lunch_obligation = Obligation("Lunch", 
                                                start_time= time(12,00), 
                                                end_time = time(13,00),
                                                location = self.cafeteria,
                                                weekdays = [0,1,2,3,4,5,6,7])

        self.principal_office_obligation_morning = Obligation("Principal Office Morning", 
                                                    start_time= time(9,00), 
                                                    end_time = time(13,00),
                                                    location = self.principal_office,
                                                    weekdays = [0,1,2,3,4,5])
        self.principal_office_obligation_afternoon = Obligation("Principal Office Afternoon", 
                                        start_time= time(14,00), 
                                        end_time = time(18,00),
                                        location = self.principal_office,
                                        weekdays = [0,1,2,3,4,5])

        self.secretary_office_obligation_morning = Obligation("Secretary Office Morning", 
                                                    start_time= time(6,00), 
                                                    end_time = time(13,00),
                                                    location = self.secretary_office,
                                                    weekdays = [0,1,2,3,4,5])
        self.secretary_office_obligation_afternoon = Obligation("Secretary Office Afternoon", 
                                    start_time= time(14,00), 
                                    end_time = time(16,00),
                                    location = self.secretary_office,
                                    weekdays = [0,1,2,3,4,5])

    def _init_obligations(self):

        self.student_lunch_obligation = Obligation("Lunch", 
                                        start_time= time(12,00), 
                                        end_time = time(13,00),
                                        location = self.cafeteria,
                                        weekdays = [0,1,2,3,4,5,6,7])

        #absence obligation, blocking student doing any activities on campus (e.g., during vacation)
        self.absent_obligation = Obligation("Absence", 
                                        start_time= time(0,5), 
                                        end_time = time(23,55),
                                        location = None,
                                        weekdays = [0,1,2,3,4,5,6,7])
        
        self.chess_club = Club("Chess Club",
                                     start_time= time(17,00),
                                     end_time = time(19,00),
                                     location = self.classrooms["Classroom A"],
                                     day = 0)
        self.chess_club.set_teacher(random.choice(self.teachers))
        self.clubs.append(self.chess_club)

        self.roleplay_club = Club("DnD Club",
                                        start_time= time(17,00),
                                        end_time = time(19,00),
                                        location = self.leisure_rooms[0],
                                        day = 1)
        self.clubs.append(self.roleplay_club)
        
        self.study_club = Club("Study Club",
                                        start_time= time(17,00),
                                        end_time = time(19,00),
                                        location = self.library,
                                        day = 2)
        self.clubs.append(self.study_club)
        
        self.basketball_club = Club("Basketball Club",
                                        start_time= time(17,00),
                                        end_time = time(19,00),
                                        location = self.sports_field,
                                        day = 3)
        self.basketball_club.set_teacher(random.choice(self.teachers))
        self.clubs.append(self.basketball_club)
        
        self.cooking_club = Club("Cooking Club",
                                        start_time= time(17,00),
                                        end_time = time(19,00),
                                        location = self.cafeteria,
                                        day = 4)
        self.cooking_club.set_teacher(random.choice(self.teachers))
        self.clubs.append(self.cooking_club)
        
        self.gymnastics_club = Club("Gymnastics Club",
                                        start_time= time(8,00),
                                        end_time = time(10,00),
                                        location = self.cafeteria,
                                        day = 5)
        self.gymnastics_club.set_teacher(random.choice(self.teachers))
        self.clubs.append(self.gymnastics_club)
        
        self.debate_club = Club("Debate Club",
                                        start_time= time(14,00),
                                        end_time = time(16,00),
                                        location = self.classrooms["Classroom D"],
                                        day = 6)
        self.debate_club.set_teacher(random.choice(self.teachers))
        self.clubs.append(self.debate_club)

    def _schedule_classes(self):
        """
            schedules all classes such that each class has one free time slot per day
            Assumption: we do not have less class rooms than classes.
        """
        all_classes = copy(list(self.classes.values()))
        for day in range(5):
            # which of the four blocks is to be left free for which class? indexed by class index.
            free_times = []
            for class_index in range(len(all_classes)):
                free_times.append(random.randint(0,3))
            for time in range(4):
                available_rooms = list(self.classrooms.values())
                for class_index in range(len(all_classes)):
                    if time != free_times[class_index]:
                        room = random.choice(available_rooms)
                        available_rooms.remove(room)
                        all_classes[class_index].set_schedule_item(day, time, room)

    def _clear_scheduled_classes(self):
        """
        clears the scheduled classes (used for setting the school into vacation mode)
        """
        all_classes = copy(list(self.classes.values()))
        for day in range(5):
            # which of the four blocks is to be left free for which class? indexed by class index.
            for time in range(4):
                for class_index in range(len(all_classes)):
                    all_classes[class_index].set_schedule_item(day, time, None)

    def _add_random_student(self):
        self.student_nr_counter += 1
        school_class = self._select_class_for_new_student()

        student = Person(name = f"Student {self.student_nr_counter}" ,
                         ui_color = util.get_random_color(),
                         wake_up_time= util.get_random_time_between(6,0,10,0),
                         sleep_time=util.get_random_time_between(20,0,23,55))
        student.school_class = school_class
        self.students.append(student)
        school_class.add_student(student)
        
        dorm = random.choice(self.free_dorms)
        self.free_dorms.remove(dorm)
        student.sleep_room = dorm
        student.dorm = dorm
        self.scenario.add_person(student)

        # use extroversion and conscientious personality traits to influences leisure activity weights. 
        extroversion = random.random()
        introversion = 1 - extroversion
        conscientiousness = random.random()
        unconscientiousness = 1 - conscientiousness
        activeness = random.random()
        inactiveness = random.random()

        # schedule obligations and clubs
        student.add_obligation(self.student_lunch_obligation)

        student.clubs = []
        if(3* introversion + 2 * inactiveness + 2 * conscientiousness + 4 *random.random() > 6):
            student.clubs.append(self.chess_club)
            self.chess_club.add_student(student)
        if(2* introversion + 2 * conscientiousness + 6 * random.random() > 6):
            student.clubs.append(self.roleplay_club)
            self.roleplay_club.add_student(student)
        if(2* extroversion + 5* conscientiousness + 3*random.random() > 6):
            student.clubs.append(self.study_club)
            self.study_club.add_student(student)
        if(5*activeness + 3*extroversion + 2*random.random() > 6):
            student.clubs.append(self.basketball_club)
            self.basketball_club.add_student(student)  
        if(2*extroversion + 8*random.random() > 6):
            student.clubs.append(self.cooking_club)
            self.cooking_club.add_student(student)
        if(6* activeness + 4* random.random() > 6):
                student.clubs.append(self.gymnastics_club)
                self.gymnastics_club.add_student(student)
        if(4*extroversion + 3*conscientiousness + 4*random.random() > 6):
                student.clubs.append(self.debate_club)
                self.debate_club.add_student(student)


        # schedule leisure activities
        study_dorm_activity = Leisure_Activity("Study in Dorm",
                                                    location_options= [dorm],
                                                    min_duration=60, 
                                                    max_duration=180)
        
        alone_time_activity = Leisure_Activity("Alone Time",
                                                    location_options= [dorm],
                                                    min_duration=30, 
                                                    max_duration=120)

        student.add_leisure_activity(self.bathroom_activity,2)
        student.add_leisure_activity(self.meeting_activity, 4 + 3*extroversion + 3*random.random())
        student.add_leisure_activity(self.socialize_activity,6*extroversion + 4*random.random())
        student.add_leisure_activity(alone_time_activity,8*introversion + 2*random.random())
        student.add_leisure_activity(self.snacking_activity, 3 + 2* unconscientiousness + 5*random.random())
        student.add_leisure_activity(self.watch_tv_activity, 5*unconscientiousness + 5*random.random())
        student.add_leisure_activity(self.pool_activity,4*activeness + 3*introversion + 3*random.random())
        student.add_leisure_activity(self.kicker_activity,4*activeness + 3*extroversion + 3*random.random())
        student.add_leisure_activity(self.air_hockey_activity,4*activeness + 3*extroversion + 3*random.random())
        student.add_leisure_activity(self.air_hockey_activity,5*activeness + 4*extroversion + 1*random.random())
        student.add_leisure_activity(self.basketball_activity,6*activeness + 4*extroversion)
        student.add_leisure_activity(self.board_gaming_activity, 3*inactiveness + 3 * introversion + 4*random.random())

        student.add_leisure_activity(self.study_outside_activity, 4*conscientiousness + 4*extroversion + 2*random.random())
        student.add_leisure_activity(self.study_library_activity, 5*conscientiousness+ 4*introversion + random.random())
        student.add_leisure_activity(study_dorm_activity, 3*conscientiousness + 5*introversion + 2*random.random())

        student.add_leisure_activity(self.cinema_activity,3*introversion + random.random()*3)
        student.add_leisure_activity(self.shopping_activity,3*extroversion + random.random()*5)
        
        return student

    def _remove_student(self,student):
        school_class = student.school_class
        school_class.remove_student(student)

        dorm = student.dorm
        student.sleep_room = None
        self.free_dorms.append(dorm)
        
        clubs = student.clubs
        for club in clubs:
            club.remove_student(student)

        self.students.remove(student)
        self.scenario.remove_person(student)



    def _set_student_to_absent(self, student):
        student.sleep_room = None      

        for club in student.clubs:
             club.remove_student(student)

        student.remove_obligation(self.student_lunch_obligation.name)
        student.add_obligation(self.absent_obligation)

    def _set_student_to_present(self, student):
            student.sleep_room = student.dorm      
    
            for club in student.clubs:
                    club.add_student(student)
    
            student.remove_obligation(self.absent_obligation.name)
            student.add_obligation(self.student_lunch_obligation)

    def _init_staff(self):
        for school_class in self.classes.values():
            self._add_teacher(school_class)
        self._add_office_staff()

    def _add_teacher(self,school_class):
        teacher = Person(name = f"Student {self.student_nr_counter}" ,
                                 ui_color = util.get_random_color(),
                                 wake_up_time= time(7,00),
                                 sleep_time=time(17,00))
        self.scenario.add_person(teacher)
        self.teachers.append(teacher)
        school_class.set_teacher(teacher)


        # obligations
        teacher.add_obligation(self.teacher_lunch_obligation)


        # activities
        teacher_hangout = Leisure_Activity("Teacher Hangout", 
                                                            location_options = [self.staff_room], 
                                                            min_duration=30, 
                                                            max_duration=60)
        teacher.add_leisure_activity(teacher_hangout,8)
        
        teacher_bathroom_activity = Leisure_Activity("Teacher Bathroom", 
                                                                    location_options = [self.bathrooms["Bathroom - Lecture Wing"]], 
                                                                    min_duration=30, 
                                                                    max_duration=60)
        teacher.add_leisure_activity(teacher_bathroom_activity,2)

        snacking_activity = Leisure_Activity("Teacher Snacking",
                                                            location_options= [self.cafeteria],
                                                            min_duration=30, 
                                                            max_duration=60)
        teacher.add_leisure_activity(snacking_activity,2)

    def _set_teacher_to_absent(self, teacher):
    
        teacher.remove_obligation(self.teacher_lunch_obligation.name)
        teacher.add_obligation(self.absent_obligation)
    
    def _set_teacher_to_present(self, teacher):
        teacher.add_obligation(self.teacher_lunch_obligation)
        teacher.remove_obligation(self.absent_obligation.name)
    
    def _add_office_staff(self):
            self.principal = Person(name = "Principal" ,
                                     ui_color = util.get_random_color(),
                                     wake_up_time= time(13,00),
                                     sleep_time=time(14,00))
            self.scenario.add_person(self.principal)

            self.secretary = Person(name = f"Secretary" ,
                                                 ui_color = util.get_random_color(),
                                                 wake_up_time= time(13,00),
                                                 sleep_time=time(14,00))
            self.scenario.add_person(self.secretary)

    
    
            # obligations
            lunch_obligation = Obligation("Lunch", 
                                            start_time= time(13,00), 
                                            end_time = time(14,00),
                                            location = self.cafeteria,
                                            weekdays = [0,1,2,3,4,5])
            self.principal.add_obligation(lunch_obligation)
            self.principal.add_obligation(self.principal_office_obligation_morning)
            self.principal.add_obligation(self.principal_office_obligation_afternoon)

            
            self.secretary.add_obligation(lunch_obligation)
            self.secretary.add_obligation(self.secretary_office_obligation_morning)
            self.secretary.add_obligation(self.secretary_office_obligation_afternoon)

    def _set_office_staff_to_vacation(self):
        self.principal_office_obligation_morning.start_time = time(10,0)
        self.principal_office_obligation_afternoon.end_time = time(15,0)
        self.secretary_office_obligation_morning.start_time = time(9,0)
        self.secretary_office_obligation_afternoon.end_time = time(14,30)

    def _set_office_staff_to_semester_time(self):
        self.principal_office_obligation_morning.start_time = time(9,00)
        self.principal_office_obligation_afternoon.end_time = time(18,00)
        self.secretary_office_obligation_morning.start_time = time(6,0)
        self.secretary_office_obligation_afternoon.end_time = time(16,00)




    def _select_class_for_new_student(self):
        return min(self.classes.values(), key= lambda school_class: len(school_class.students) )

    def _init_dorm_a(self):
        # Floor 1:
        stairs_a_1_up = self._create_room("Stairs A 1 Up", 40, 1530)
        a11 = self._create_dorm("Dorm A11", 200, 1530)
        a12 = self._create_dorm("Dorm A12", 330, 1530)
        a13 = self._create_dorm("Dorm A13", 450, 1530)
        a14 = self._create_dorm("Dorm A14", 590, 1530)
        a15 = self._create_dorm("Dorm A15", 590, 1860)
        a16 = self._create_dorm("Dorm A16", 450, 1860)
        a17 = self._create_dorm("Dorm A17", 330, 1860)
        a18 = self._create_dorm("Dorm A18", 200, 1860)
        bathroom_a_1 = self._create_bathroom("Bathroom A 1", 40, 1860)
        kitchen_a_1 = self._create_room("Kitchen A 1", 190, 1740, ressources=[self.RESSOURCE_SNACKS])
        self.seating_areas.append(kitchen_a_1)
        kicker_a_1 = self._create_room("Kicker A 1", 340, 1740, ressources=[self.RESSOURCE_KICKER])



        hallway_a_1_1 = self._create_connection("Hallway A 1 1", 
                                x= 40, 
                                y = 1650,
                                connected_rooms = [ stairs_a_1_up,bathroom_a_1])

        hallway_a_1_2 = self._create_connection("Hallway A 1 2", 
                                x= 265, 
                                y = 1650,
                                connected_rooms = [hallway_a_1_1, a11, a12, a18, a17, kicker_a_1, kitchen_a_1])
        
        self.exit_dorm_a = self._create_connection("Hallway A 1 3", 
                                        x= 520, 
                                        y = 1700,
                                        connected_rooms = [hallway_a_1_2, a13, a14, a15, a16])


        # Floor 2:
        stairs_a_2_up = self._create_room("Stairs A 2 Up", 40, 910)
        stairs_a_2_down = self._create_room("Stairs A 2 Down", 40, 1220)
        a21 = self._create_dorm("Dorm A21", 200, 910)
        a22 = self._create_dorm("Dorm A22", 330, 910)
        a23 = self._create_dorm("Dorm A23", 450, 910)
        a24 = self._create_dorm("Dorm A24", 590, 910)
        a25 = self._create_dorm("Dorm A25", 590, 1220)
        a26 = self._create_dorm("Dorm A26", 450, 1220)
        a27 = self._create_dorm("Dorm A27", 330, 1220)
        a28 = self._create_dorm("Dorm A28", 200, 1220)
        bathroom_a_2 = self._create_bathroom("Bathroom A 2", 600, 1130)
        pool_a_2 = self._create_room("Pool A 2", 390, 1020, ressources=[self.RESSOURCE_POOL])

        hallway_a_2_1 = self._create_connection("Hallway A 2 1", 
                                        x= 40, 
                                        y = 1130,
                                        connected_rooms = [ stairs_a_2_up,stairs_a_2_down])

        hallway_a_2_2 = self._create_connection("Hallway A 2 2", 
                                                x= 265, 
                                                y = 1130,
                                                connected_rooms = [ hallway_a_2_1, a21, a22, a27, a28, pool_a_2])

        hallway_a_2_3 = self._create_connection("Hallway A 2 3", 
                                                        x= 520, 
                                                        y = 1130,
                                                        connected_rooms = [ hallway_a_2_2, a23, a24, a25, a26, bathroom_a_2])

        self.add_transtion(stairs_a_1_up, stairs_a_2_down)

        
        # Floor 3:
        stairs_a_3_down = self._create_room("Stairs A 3 Down", 40, 680)
        a31 = self._create_dorm("Dorm A31", 40, 300)
        a32 = self._create_dorm("Dorm A32", 200, 300)
        a33 = self._create_dorm("Dorm A33", 330, 300)
        a34 = self._create_dorm("Dorm A34", 450, 300)
        a35 = self._create_dorm("Dorm A35", 590, 300)
        a36 = self._create_dorm("Dorm A36", 590, 630)
        a37 = self._create_dorm("Dorm A37", 450, 630)
        a38 = self._create_dorm("Dorm A38", 330, 630)
        a39 = self._create_dorm("Dorm A39", 200, 630)
        bathroom_a_3 = self._create_bathroom("Bathroom A 3", 600, 520)
        couch_a_3 = self._create_room("Couch A 3", 390, 500, ressources=[self.RESSOURCE_TV])
        self.seating_areas.append(couch_a_3)

        hallway_a_3_1 = self._create_connection("Hallway A 3 1", 
                                                x= 40, 
                                                y = 420,
                                                connected_rooms = [ stairs_a_3_down, a31])

        hallway_a_3_2 = self._create_connection("Hallway A 3 2", 
                                                        x= 265, 
                                                        y = 420,
                                                        connected_rooms = [ hallway_a_3_1, a32, a33, a38, a39, couch_a_3])

        hallway_a_3_3 = self._create_connection("Hallway A 3 3", 
                                                                x= 520, 
                                                                y = 420,
                                                                connected_rooms = [hallway_a_3_2, a34, a35, a36, a37, bathroom_a_3])

        self.add_transtion(stairs_a_2_up, stairs_a_3_down)
        
    def _init_dorm_b(self):
        b1 = self._create_dorm("Dorm B1", 880, 290)
        b2 = self._create_dorm("Dorm B2", 1060, 290)
        b3 = self._create_dorm("Dorm B3", 1120, 290)
        b4 = self._create_dorm("Dorm B4", 1310, 290)
        b5 = self._create_dorm("Dorm B5", 1380, 290)
        b6 = self._create_dorm("Dorm B6", 1510, 290)
        b7 = self._create_dorm("Dorm B7", 1700, 290)
        b8 = self._create_dorm("Dorm B8", 1760, 290)
        b9 = self._create_dorm("Dorm B9", 1960, 290)
        b10 = self._create_dorm("Dorm B10", 2020, 290)
        b11 = self._create_dorm("Dorm B11", 2150, 290)
        b12 = self._create_dorm("Dorm B12", 2340, 290)
        b13 = self._create_dorm("Dorm B13", 2410, 290)
        b14 = self._create_dorm("Dorm B14", 2600, 290)
        b15 = self._create_dorm("Dorm B15", 2660, 290)
        b16 = self._create_dorm("Dorm B16", 1060, 560)
        b17 = self._create_dorm("Dorm B17", 1120, 560)
        b18 = self._create_dorm("Dorm B18", 1380, 560)
        b19 = self._create_dorm("Dorm B19", 1700, 560)
        b20 = self._create_dorm("Dorm B20", 1760, 560)
        b21 = self._create_dorm("Dorm B21", 1960, 560)
        b22 = self._create_dorm("Dorm B22", 2020, 560)
        b23 = self._create_dorm("Dorm B23", 2150, 560)
        b24 = self._create_dorm("Dorm B24", 2410, 560)
        b25 = self._create_dorm("Dorm B25", 2600, 560)
        b26 = self._create_dorm("Dorm B26", 2660, 560)

        bathroom_b_1 = self._create_bathroom("Bathroom B 1", 900, 600)
        bathroom_b_2 = self._create_bathroom("Bathroom B 2", 1530, 600)
        bathroom_b_3 = self._create_bathroom("Bathroom B 3", 2710, 480)

        kitchen_b = self._create_room("Kitchen B", 980, 470, ressources=[self.RESSOURCE_SNACKS])
        self.seating_areas.append(kitchen_b)
        couch_b = self._create_room("Couch B", 1620, 440, ressources=[self.RESSOURCE_TV])
        self.seating_areas.append(couch_b)
        pool_b = self._create_room("Pool B", 1870, 430, ressources=[self.RESSOURCE_POOL])
        air_hockey_b = self._create_room("Air Hockey B", 2510, 460, ressources=[self.RESSOURCE_AIR_HOCKEY])

        self.exit_dorm_b_outside = self._create_room("Exit B 1", 1280, 600)
        self.exit_dorm_b_library = self._create_room("Exit B 2", 2310, 600)


        hallway_b_1 = self._create_connection("Hallway B 1", 
                                                        x= 860, 
                                                        y = 380,
                                                        connected_rooms = [ bathroom_b_1, b1])
        hallway_b_2 = self._create_connection("Hallway B 2", 
                                                        x= 1100, 
                                                        y = 380,
                                                        connected_rooms = [ hallway_b_1, kitchen_b, b2, b3, b16, b17])
        hallway_b_3 = self._create_connection("Hallway B 3", 
                                                        x= 1350, 
                                                        y = 380,
                                                        connected_rooms = [ hallway_b_2, self.exit_dorm_b_outside, b4, b5, b18])
        hallway_b_4 = self._create_connection("Hallway B 4", 
                                                        x= 1510, 
                                                        y = 380,
                                                        connected_rooms = [ hallway_b_3, b6, bathroom_b_2])
        hallway_b_5 = self._create_connection("Hallway B 5", 
                                                        x= 1740, 
                                                        y = 380,
                                                        connected_rooms = [ hallway_b_4, couch_b, pool_b, b7, b8, b19, b20])
        hallway_b_6 = self._create_connection("Hallway B 6", 
                                                        x= 2000, 
                                                        y = 380,
                                                        connected_rooms = [ hallway_b_5, b9, b10, b21, b22])
        hallway_b_7 = self._create_connection("Hallway B 7", 
                                                        x= 2140, 
                                                        y = 380,
                                                        connected_rooms = [ hallway_b_6, b11, b23])

        hallway_b_8 = self._create_connection("Hallway B 8", 
                                                        x= 2380, 
                                                        y = 380,
                                                        connected_rooms = [ hallway_b_7,air_hockey_b, self.exit_dorm_b_library, b12, b13, b24])

        hallway_b_9 = self._create_connection("Hallway B 9", 
                                                        x= 2640, 
                                                        y = 430,
                                                        connected_rooms = [ hallway_b_8, bathroom_b_3, b14, b15, b25, b26])

    def _init_lecture_wing(self):
        class_a = self._create_classroom("Classroom A", 1110, 1780)
        class_b = self._create_classroom("Classroom B", 1660, 1780)
        class_c = self._create_classroom("Classroom C", 2150, 1780)
        class_d = self._create_classroom("Classroom D", 2650, 1780)

        meet_1 = self._create_room("Meet 1", 730, 1450)
        meet_2 = self._create_room("Meet 2", 890, 1450)
        meet_3 = self._create_room("Meet 3", 1040, 1450)
        meet_4 = self._create_room("Meet 4", 1200, 1450)
        self.meeting_rooms.extend([meet_1, meet_2, meet_3, meet_4])

        bathroom = self._create_bathroom("Bathroom - Lecture Wing", 1580, 1450) 

        leisure_1 = self._create_room("Leisure 1", 1710, 1450)
        leisure_2 = self._create_room("Leisure 2", 1980, 1450)
        self.seating_areas.append(leisure_1)
        self.seating_areas.append(leisure_2)
        self.leisure_rooms.append(leisure_1)
        self.leisure_rooms.append(leisure_2)

        self.staff_room = self._create_room("Staff Room", 2280, 1450)

        self.secretary_office = self._create_room("Secretary Office", 2710, 1450)
        self.principal_office = self._create_room("Principal Office", 2540, 1400)
        self.add_transtion(self.secretary_office,self.principal_office)

        couch = self._create_room("Couch - Lecture Wing", 690, 1860)
        self.seating_areas.append(couch)

        self.exit_lecture_wing_outside = self._create_room("Exit 1 - Lecture Wing", 1330, 1450)
        self.exit_lecture_wing_cafeteria = self._create_room("Exit 2 - Lecture Wing", 2400, 1450)
        self.exit_lecture_wing_main_exit = self._create_room("Exit 3 - Lecture Wing", 2900, 1570, is_exit= True)

        hallway_lecture_1 = self._create_connection("Hallway 1 - Lectue Wing", 
                                                                x= 700, 
                                                                y = 1700,
                                                                connected_rooms = [ self.exit_dorm_a, couch])
        hallway_lecture_2 = self._create_connection("Hallway 2 - Lectue Wing", 
                                                                x= 700, 
                                                                y = 1570,
                                                                connected_rooms = [hallway_lecture_1, meet_1])
        hallway_lecture_3 = self._create_connection("Hallway 3 - Lectue Wing", 
                                                                x= 830, 
                                                                y = 1570,
                                                                connected_rooms = [hallway_lecture_2, meet_2])
        hallway_lecture_4 = self._create_connection("Hallway 4 - Lectue Wing", 
                                                                x= 980, 
                                                                y = 1570,
                                                                connected_rooms = [hallway_lecture_3, meet_3])
        hallway_lecture_5 = self._create_connection("Hallway 5 - Lectue Wing", 
                                                                x= 1140, 
                                                                y = 1570,
                                                                connected_rooms = [hallway_lecture_4, meet_4])
        hallway_lecture_6 = self._create_connection("Hallway 6 - Lectue Wing", 
                                                                x= 1330, 
                                                                y = 1570,
                                                                connected_rooms = [hallway_lecture_5, class_a, self.exit_lecture_wing_outside])
        hallway_lecture_7 = self._create_connection("Hallway 7 - Lectue Wing", 
                                                                x= 1690, 
                                                                y = 1570,
                                                                connected_rooms = [hallway_lecture_6, class_b, bathroom, leisure_1])
        hallway_lecture_8 = self._create_connection("Hallway 8 - Lectue Wing", 
                                                                x= 2010, 
                                                                y = 1570,
                                                                connected_rooms = [hallway_lecture_7, leisure_2])
        hallway_lecture_9 = self._create_connection("Hallway 9 - Lectue Wing", 
                                                                x= 2350, 
                                                                y = 1570,
                                                                connected_rooms = [hallway_lecture_8, class_c, self.staff_room, self.exit_lecture_wing_cafeteria])
        hallway_lecture_10 = self._create_connection("Hallway 10 - Lectue Wing", 
                                                                x= 2740, 
                                                                y = 1570,
                                                                connected_rooms = [hallway_lecture_9, class_d, self.secretary_office, self.exit_lecture_wing_main_exit])

    def _init_library_cafeteria(self):
        self.cafeteria = self._create_room("Cafeteria", 2520, 1040, ressources=[self.RESSOURCE_SNACKS])
        self.seating_areas.append(self.cafeteria)
        self.library = self._create_room("Library", 2580, 780)
        
        self.exit_cafeteria_outside= self._create_room("Exit Cafeteria",  2200, 1130)

        hallway_cafeteria_library_1 = self._create_connection("Hallway 1 - Cafeteria", 
                                                                x= 2340, 
                                                                y = 1130,
                                                                connected_rooms = [ self.exit_lecture_wing_cafeteria, self.exit_cafeteria_outside, self.cafeteria])
        hallway_cafeteria_library_2 = self._create_connection("Hallway 2 - Cafeteria", 
                                                                x= 2340, 
                                                                y = 780,
                                                                connected_rooms = [ hallway_cafeteria_library_1, self.exit_dorm_b_library, self.library])

    def _init_school_yard(self):
        self.school_yard = self._create_room("School Yard", 1610, 1030, is_outside=True)
        self.sports_field = self._create_room("Sports Field", 915, 1050, is_outside=True)

        self.add_transtion(self.school_yard, self.sports_field)
        self.add_transtion(self.school_yard, self.exit_dorm_b_outside)
        self.add_transtion(self.school_yard, self.exit_lecture_wing_outside)
        self.add_transtion(self.school_yard, self.exit_cafeteria_outside)

    def _create_dorm(self, name, x,y):
        """
            Create a dorm room and register it.
        """
        dorm = Room(name, x, y)
        self.add_room(dorm)
        self.dorms[name] = dorm
        self.free_dorms.append(dorm)
        return dorm

    def _create_classroom(self, name, x,y):
            """
                Create a dorm room and register it.
            """
            room = Room(name, x, y)
            self.add_room(room)
            self.classrooms[name] = room
            return room

    def _create_room(self,name,x,y,ressources = [], is_outside = False, is_exit = False):
        """
            Create a bathroom 
        """
        room = Room(name, x, y, ressources= ressources, is_outside= is_outside, is_exit= is_exit)
        self.add_room(room)
        return room

    def _create_bathroom(self,name,x,y):
            """
                Create a bathroom 
            """
            room = Room(name, x, y)
            self.add_room(room)
            self.bathrooms[name] = room
            return room

    def _create_connection(self,name,x,y,connected_rooms):
        connection = self._create_room(name,x,y)
        for room in connected_rooms:
            self.add_transtion(connection,room)

        return connection

