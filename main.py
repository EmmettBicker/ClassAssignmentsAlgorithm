import pandas as pd
import numpy as np
import math

from class_assignments import assign


def main():
    data = pd.read_csv("(Phase 4) Class Generation Inputs - Inputs To Program.csv")
    # get all non null names (student names extend further down giving volunteer names nulls)
    volunteer_names = data["Volunteer Name"][~data["Volunteer Name"].isnull()]
    student_preferences = data["Student First Choice"]

    id_to_volunteer = dict(zip(range(len(volunteer_names)), volunteer_names))

    volunteer_capabilites = data["Volunteer Capabilities"][~data["Volunteer Capabilities"].isnull()]
    # use numpy for transposition 
    unique_classes = set()

    # Creating unique class lists by looking at every option a volunteer put down as their capabilities
    [[unique_classes.add(i.strip()) for i in course.strip().split(", ")] for course in list(volunteer_capabilites)]
    # Creating unique class lists by looking at every option a student requested
    [unique_classes.add(class_name) for class_name in student_preferences]
    unique_classes = list(unique_classes)
    unique_classes = sorted(unique_classes, reverse=True)
    

    #unique_classes = ["Intro to Python", "Intermediate Python", "Intro to Java", "Intermediate Java"]
    
    numerical_capabilities = np.array([
        [[int(unique_classes[i] in capability) for capability in volunteer_capabilites] for i in range(len(unique_classes))]
        
    ])


    # print(numerical_capabilities)
    # numerical_capabilities = np.array([
    #     [int("Intro to Python" in capability) for capability in volunteer_capabilites],
    #     [int("Intermediate Python" in capability) for capability in volunteer_capabilites],
    #     [int("Intro to Java" in capability) for capability in volunteer_capabilites],
    #     [int("Intermediate Java" in capability) for capability in volunteer_capabilites]
    # ])
    # print(numerical_capabilities)

    

    # turn transpoed numpy array into a multidimensional array
    numerical_capabilities = list(list(capability) for capability in numerical_capabilities.T)

    # ids to capabilites
    volunteer_ids_to_capabilites = dict(zip(range(len(volunteer_names)), numerical_capabilities))

    # student data collection
    

    preference_to_id = {}

    for i in range(len(unique_classes)):
        preference_to_id[unique_classes[i]] = i 

    student_preferences_dictionary = dict(
        (class_name, sum(student_preferences==class_name)) for class_name in unique_classes
    )

    id_to_preference = {}
    for i in range(len(unique_classes)):
        id_to_preference[i] = [unique_classes[i]]
    
    student_preferences = [preference_to_id[preference] for preference in student_preferences]

    volunteer_class_list, student_to_teacher_ratios, leftover_volunteers, class_popularity = assign(volunteers=volunteer_ids_to_capabilites, 
                                                                                                               students=student_preferences, 
                                                                                                               classes=unique_classes)

    volunteer_to_class = {}
    
    for i in range(len(unique_classes)):
        for volunteer in volunteer_class_list[i]:
            volunteer_to_class[id_to_volunteer[volunteer]] = unique_classes[i]
    # this code turns the numbers in the class lists to the names (omg this code is so bad)
    volunteer_class_list = [[id_to_volunteer[volunteer_class_list[class_num][j]] for j in range(len(volunteer_class_list[class_num]))] for class_num in range(len(unique_classes))]
    student_names = [data["Student First Name"][i].strip() + " " + data["Student Last Name"][i].strip() for i in range(len(data["Student First Name"]))]
    student_ages = list(data["Student Grade"])
    
    students_full = list(zip(student_names,student_preferences,student_ages))

    # Sort by age
    students_full = sorted(students_full, key=lambda x : x[2])
    
    
    
    volunteer_name_to_class_list = dict(zip(volunteer_names, [ [] for _ in range(len(volunteer_names))]))
            

    for student in students_full:
        preference = student[1]
        student = list(student)
        student[2] = "Grade " + str(student[2])
        for volunteer in volunteer_class_list[preference]:
            if len(volunteer_name_to_class_list[volunteer]) < math.ceil(student_to_teacher_ratios[preference]):
                del student[1]
                student = " - ".join(student)
                volunteer_name_to_class_list[volunteer].append(student)
                break
    
    volunteer_names = sorted(volunteer_names, key=lambda name : preference_to_id[volunteer_to_class[name]])
    final_class_assignments = pd.DataFrame(columns=volunteer_names)
    for volunteer in volunteer_names:
        final_class_assignments[volunteer] = pd.Series(volunteer_name_to_class_list[volunteer])
    
    final_class_assignments = final_class_assignments.transpose()
    final_class_assignments.insert(loc=0,
          column="Classes",
          value=[volunteer_to_class[name] for name in volunteer_names])
    
    # Get rows of dataframe where the classes is the first unique class and get all the students
    final_students_per_class = {}
    for class_name in unique_classes:
        temp = final_class_assignments[final_class_assignments["Classes"]==unique_classes[preference_to_id[class_name]]].loc[:,0:][~final_class_assignments.isnull()]
        total_students_in_class = sum(temp.count())
        final_students_per_class[class_name] = total_students_in_class
    
    print(final_students_per_class)

    final_class_assignments.to_csv('assignments.csv')

    with open("analysis.txt","w") as file:
        file.write("Analysis:" + "\n")
        file.write("----------------------------------" + "\n")
        file.write("Total Volunteers: " + str(len(volunteer_names)) + "\n")
        file.write("Total Students: " + str(len(student_names)) + "\n")
        file.write("\n")

        file.write("Class preferences: " + "\n")
        for class_name in unique_classes:
            file.write("    ")
            file.write(str(class_name) + " - " + str(
                round(float(class_popularity[preference_to_id[class_name]])*100,2)) + "% \n")
        file.write('\n')

        file.write("Volunteers per Class: " + "\n")
        for class_name in unique_classes:
            file.write("    ")
            file.write(str(class_name) + " - " + str(
                round(int(len(volunteer_class_list[preference_to_id[class_name]])),2)) + "\n")
        file.write('\n')

        file.write("Students per Class: " + "\n")
        for class_name in unique_classes:
            file.write("    ")
            file.write(str(class_name) + " - " + str(
                # Percents * total students
                final_students_per_class[class_name]) + "\n")
        file.write('\n')

        file.write("Students Left Out Per Class: " + "\n")
        for class_name in unique_classes:
            file.write("    ")
            file.write(str(class_name) + " - " + str(
                # Percents * total students
                final_students_per_class[class_name] - student_preferences_dictionary[class_name]) + "\n")
        file.write('\n')

        file.write("Student to Teacher Ratios: " + "\n")
        for class_name in unique_classes:
            file.write("    ")
            file.write(str(class_name) + " - " + str(
                round(float(student_to_teacher_ratios[preference_to_id[class_name]]),2)) + " : 1 \n")

    
  
main()