from operator import is_
from domain_model.changes.leisure_activity_add import Leisure_Activity_Add_Change
from domain_model.changes.leisure_activity_remove_change import Leisure_Activity_Remove_Change
from domain_model.changes.move_in_change import Move_In_Change
from domain_model.changes.obligation_add_change import Obligation_Add_Change
from domain_model.changes.obligation_remove_change import Obligation_Remove_Change
from domain_model.leisure_activity import Leisure_Activity
from domain_model.obligation import Obligation
from domain_model.scenario import Scenario_Configuration
from domain_model.changes.move_out_change import Move_Out_Change
from domain_model.house import House
from domain_model.room import Room
from domain_model.person import Person

from datetime import datetime
from datetime import time

from examples.complex_scenario.src.changes.open_dorm_b_change import Open_Dorm_B_Change
from examples.complex_scenario.src.changes.semester_vacation_end_change import Semester_Vacation_End_Change
from examples.complex_scenario.src.changes.smester_vacation_start_change import Semester_Vacation_Start_Change
from examples.complex_scenario.src.changes.student_population_change import Student_Population_Change
from examples.complex_scenario.src.school.campus import Campus 


def create_complex_scenario():
    scenario = Scenario_Configuration()
    scenario.background_image = "examples/complex_scenario/images/campus.png"

    YEARS = 5
    YEAR_1 = 2020

    campus = Campus(scenario= scenario, nr_students= 20)
    scenario.house = campus
    scenario.startTime = datetime(year = YEAR_1, month = 4, day = 1, hour = 0, minute = 0)

    # build schedule:
        #   duration: 5 years.
        #   Semester times: 
        #       Summer Semester: 01.4. - 01.07.
        #       Summer Break: 01.07. - 01.10.
        #       Winter Semester: 01.10. - 01.02.
        #       Winter break: 01.02. - 01.04.
        #   student numbers:
        #        Year 1: 20
        #        Year 2: 30
        #        Year 3: 40
        #        Year 4: 50
        #        Year 5: 50
    for year in range(YEARS):
        summer_break_start = Semester_Vacation_Start_Change(datetime(year = YEAR_1 + year, month = 7, day = 1, hour = 0, minute = 0), campus)
        winter_semester_start = Semester_Vacation_End_Change(datetime(year = YEAR_1 + year, month = 10, day = 1, hour = 0, minute = 0), campus)
        winter_break_start = Semester_Vacation_Start_Change(datetime(year = YEAR_1 + year + 1, month = 2, day = 1, hour = 0, minute = 0), campus)
        summer_semester_start = Semester_Vacation_End_Change(datetime(year = YEAR_1 + year + 1, month = 4, day = 1, hour = 0, minute = 0), campus)
        
        nr_added_students = 10 if year < 3 else 0
        nr_changed_students = min(30,10 + 5*year)
        
        student_intake_change =  Student_Population_Change(datetime(year = YEAR_1 + year + 1, month = 3, day = 15, hour = 0, minute = 0), campus, 
                                                           nr_removed= nr_changed_students,
                                                           nr_added=nr_changed_students + nr_added_students)

        scenario.changes.append(summer_break_start)
        scenario.changes.append(winter_semester_start)
        scenario.changes.append(winter_break_start)
        scenario.changes.append(summer_semester_start)
        scenario.changes.append(student_intake_change)

    open_dorm_b_change = Open_Dorm_B_Change(datetime(year = YEAR_1, month = 9, day = 1, hour = 0, minute = 0), campus)
    scenario.changes.append(open_dorm_b_change)

    


    return scenario



