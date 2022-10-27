# Class Assignment Generation w/ Google Sheets

This project automatically sorts teachers and students into classes based off of students' first choice of class, and volunteer capabilities.

In order to use the algorithm, copy and paste your inputs into [https://docs.google.com/spreadsheets/d/1hhejbcEfYhPKThzSN3yg0JwOySxaif1rJNzkm-JwAoY/edit#gid=880690583](this) spreadsheet. All you have to do is copy and paste your information into the corresponding columns, download the python files, and run main.py! If you do this, the class assignments will be downloaded as a csv file for you to import into google sheets (in google sheets click file --> import). 

# Algorithm 

I sort the volunteers by their capability in ascending order, so the volunteers that can teach the fewest classes (most restrictive) are first and the volunteers that can teach the most classes are last. For every volunteer, I look at all the classes they're capable to teach and I place the volunteer in the class that the fewest other volunteers can teach and isn't already full. In the future I plan to update the algorithm so if a volunteer can teach every class, then they will be placed in the class that needs the most students, however this algorithm has been working well empirically.
