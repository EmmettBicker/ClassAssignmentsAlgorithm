import numpy as np
import math
import pandas as pd
from random import randint

def assign(volunteers, students):
    

  # volunteers = {
  #   1 : [0,0,0,1],
  #   2 : [0,1,1,0],
  #   3 : [1,0,0,1],
  #   4 : [1,1,1,1],
  #   5 : [1,0,1,0],
  #   6 : [0,1,0,1],
  #   7 : [0,1,0,0],
  #   8 : [0,1,1,0],
  #   9 : [0,0,0,1],
  #   10 : [1,1,1,1]
  # }

  total_volunteers = len(volunteers)
  number_of_classes = 4

  volunteers = pd.DataFrame(volunteers,index=[[f"Capability for class {i}" for i in range(4) ]])


  # students = (([ ([i] * randint(1,25)) for i in range(4)]))
  
  
  students = pd.DataFrame(students,columns=["Students"])

  # In percent of people who enrolled
  class_popularity = {
    0 : students[students["Students"] == 0].count() / students.count(),
    1 : students[students["Students"] == 1].count() / students.count(),
    2 : students[students["Students"] == 2].count() / students.count(),
    3 : students[students["Students"] == 3].count() / students.count(),
  }

  class_attendance = {
    0 : students[students["Students"] == 0].count(),
    1 : students[students["Students"] == 1].count(),
    2 : students[students["Students"] == 2].count(),
    3 : students[students["Students"] == 3].count()
  }

  desired_volunteer_split = {
    0 : math.ceil(class_popularity[0] * total_volunteers),
    1 : math.ceil(class_popularity[1] * total_volunteers),
    2 : math.ceil(class_popularity[2] * total_volunteers),
    3 : math.ceil(class_popularity[3] * total_volunteers)
  }

  # Cut off volunteers from most popular classes if rounding doens't work well
  while (total_volunteers - sum(desired_volunteer_split.values()) != 0):
    most_popular_class = max(desired_volunteer_split, key=desired_volunteer_split.get)
    desired_volunteer_split[most_popular_class] -= 1



  

  volunteer_capability_percents = volunteers.sum(axis=1) / total_volunteers

  volunteers_by_capability = list(sorted(volunteers.items(),key=lambda x : x[1].sum()))



  volunteer_class_list = {
    0 : [],
    1 : [],
    2 : [],
    3 : []
  }

  # make a list of what volunteers can do

  leftover_volunteers = []
  for volunteer in volunteers_by_capability:
    volunteer_name = volunteer[0]
    min_capability = 1e12
    desired_index = -1

    for idx, capability in enumerate(volunteer[1]):
      if capability == 1 and desired_volunteer_split[idx] != 0:

        if volunteer_capability_percents[capability] < min_capability:
          
          min_capability = volunteer_capability_percents[idx]
          desired_index = idx
      #elif capability == 1 and desired_volunteer_split[idx] == 0:
      # for volunteer in volunteer_class_list[idx]:
          # If any of the teachers in that class can teach another class 
          # that has more student demand than this one, swap the two 

    if desired_index != -1:
      desired_volunteer_split[desired_index] -= 1
      volunteer_class_list[desired_index].append(volunteer_name)
    else:
      leftover_volunteers.append(volunteer_name)

  student_to_teacher_ratios = {
    0 : (class_attendance[0] / len(volunteer_class_list[0]))[0],
    1 : (class_attendance[1] / len(volunteer_class_list[1]))[0],
    2 : (class_attendance[2] / len(volunteer_class_list[2]))[0],
    3 : (class_attendance[3] / len(volunteer_class_list[3]))[0]
  }


  for volunteer in leftover_volunteers:
    max_student_to_teacher_ratio = -1e10
    desired_index = -1
    
    for idx, capability in enumerate(volunteers[volunteer]):
      if capability == 1 and volunteers[volunteer][idx] > max_student_to_teacher_ratio:
        max_student_to_teacher_ratio = student_to_teacher_ratios[idx]
        desired_index = idx
    volunteer_class_list[desired_index].append(volunteer)
    leftover_volunteers.remove(volunteer)
    student_to_teacher_ratios = {
      0 : (class_attendance[0] / len(volunteer_class_list[0]))[0],
      1 : (class_attendance[1] / len(volunteer_class_list[1]))[0],
      2 : (class_attendance[2] / len(volunteer_class_list[2]))[0],
      3 : (class_attendance[3] / len(volunteer_class_list[3]))[0]
    }

  for volunteer in leftover_volunteers:
    for idx, capability in enumerate(volunteers[volunteer]):
      if capability == 1:
        volunteer_class_list[idx].append(volunteer)
        leftover_volunteers.remove(volunteer)

  return volunteer_class_list, student_to_teacher_ratios, leftover_volunteers, class_popularity
  print(student_to_teacher_ratios)
  print(max(student_to_teacher_ratios, key=student_to_teacher_ratios.get))

  print(volunteer_class_list)
  print(leftover_volunteers)
  