import pandas as pd
import numpy as np
from class_assignments import assign


def main():
    data = pd.read_excel("https://docs.google.com/spreadsheets/d/e/2PACX-1vQrrXuEdG9SBMnDcSCEmKhD5CDde27dEvXvJRHEkw46MSyw_6W-74Ia5tpjKRqJDNLQcKZKAyO4qmY9/pub?output=xlsx")
    # get all non null names (student names extend further down giving volunteer names nulls)
    volunteer_names = data["Volunteer Name"][~data["Volunteer Name"].isnull()]

    id_to_volunteer = dict(zip(range(len(volunteer_names)), volunteer_names))

    volunteer_capabilites = data["Volunteer Capabilities"][~data["Volunteer Capabilities"].isnull()]
    # use numpy for transposition 
    numerical_capabilities = np.array([
        [int("Intro to Python" in capability) for capability in volunteer_capabilites],
        [int("Intermediate Python" in capability) for capability in volunteer_capabilites],
        [int("Intro to Java" in capability) for capability in volunteer_capabilites],
        [int("Intermediate Java" in capability) for capability in volunteer_capabilites]
    ])

    # turn transpoed numpy array into a multidimensional array
    numerical_capabilities = list(list(capability) for capability in numerical_capabilities.T)

    # ids to capabilites
    volunteer_ids_to_capabilites = dict(zip(range(len(volunteer_names)), numerical_capabilities))

    # student data collection
    student_preferences = data["Student First Choice"]

    preference_to_id = {
        "Intro to Python" : 0,
        "Intermediate Python" : 1,
        "Intro to Java" : 2,
        "Intermediate Java" : 3
    }
    student_preferences = [preference_to_id[preference] for preference in student_preferences]

    volunteer_class_list, student_to_teacher_ratios, leftover_volunteers, class_popularity = assign(volunteers=volunteer_ids_to_capabilites, students=student_preferences)

    # this code turns the numbers in the class lists to the names (omg this code is so bad)
    volunteer_class_list = [[id_to_volunteer[volunteer_class_list[class_num][j]] for j in range(len(volunteer_class_list[class_num]))] for class_num in range(4)]
    student_names = [data["Student First Name"][i].strip() + " " + data["Student Last Name"][i].strip() for i in range(len(data["Student First Name"]))]
    student_ages = list(data["Student Grade"])
    print(student_ages)
    students_full = list(zip(student_names,student_preferences,student_ages))

    # Sort by age
    students_full = sorted(students_full, key=lambda x : x[2])
    print(student_to_teacher_ratios)

    # Figure out framework for the assignment
    name_to_class = dict(zip([name for name in volunteer_names], [ [] for _ in range(len(volunteer_names))]))
    print(name_to_class)
    
main()