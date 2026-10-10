from operator import is_

from datetime import datetime
from datetime import time
from domain_model.scenario import Scenario_Configuration
from examples.complex_scenario.src.changes.immediate_study_priority_change import Immediate_Study_Priority_Change
from examples.complex_scenario.src.changes.gradual_study_priority_change import Gradual_Study_Priority_Change
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
    for year in range(YEAR_1, YEAR_1 + YEARS):
        
        summer_semester_study_priority_increase = Gradual_Study_Priority_Change(datetime(year = year, month = 4, day = 2),
                                                                         duration= 60, campus = campus, day_delta= 0.1)
        summer_break_start = Semester_Vacation_Start_Change(datetime(year = year, month = 7, day = 1, hour = 0, minute = 0), campus)
        summer_break_study_priority_decrease = Immediate_Study_Priority_Change(datetime(year = year, month = 7, day = 1), campus = campus, delta = -6)

        winter_semester_start = Semester_Vacation_End_Change(datetime(year = year, month = 10, day = 1, hour = 0, minute = 0), campus)
        winter_semester_study_priority_increase = Gradual_Study_Priority_Change(datetime(year = year, month = 10, day = 2),
                                                                                 duration= 60, campus = campus, day_delta= 0.1)
        winter_break_start = Semester_Vacation_Start_Change(datetime(year = year + 1, month = 2, day = 1), campus)
        summer_break_study_priority_decrease = Immediate_Study_Priority_Change(datetime(year = year + 1, month = 2, day = 1), campus = campus, delta = -6)

        summer_semester_start = Semester_Vacation_End_Change(datetime(year = year + 1, month = 4, day = 1, hour = 0, minute = 0), campus)
        
        year_factor = year - YEAR_1
        nr_added_students = 10 if year_factor < 3 else 0
        nr_changed_students = min(30,10 + 5*year_factor)
        
        student_intake_change =  Student_Population_Change(datetime(year = year + 1, month = 3, day = 15, hour = 0, minute = 0), campus, 
                                                           nr_removed= nr_changed_students,
                                                           nr_added=nr_changed_students + nr_added_students)


        scenario.changes.append(summer_semester_study_priority_increase)
        scenario.changes.append(summer_break_start)
        scenario.changes.append(summer_break_study_priority_decrease)
        scenario.changes.append(winter_semester_start)
        scenario.changes.append(winter_semester_study_priority_increase)
        scenario.changes.append(winter_break_start)
        scenario.changes.append(summer_semester_start)
        scenario.changes.append(student_intake_change)




    open_dorm_b_change = Open_Dorm_B_Change(datetime(year = YEAR_1, month = 9, day = 1, hour = 0, minute = 0), campus)
    scenario.changes.append(open_dorm_b_change)

    return scenario



