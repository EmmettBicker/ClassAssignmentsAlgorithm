# Class Assignment Generation w/ Google Sheets API

This project automatically sorts teachers and students into classes based off of how many students are interested in each class, and which teachers the students can teach!

The algorithm is pretty simple, I sort the volunteers by their capability in ascending order, so the volunteers that can teach the fewest classes (most restrictive) are first and the volunteers that can teach the most classes are last. For every volunteer, I look at all the classes they're capable to teach and I place the volunteer in the class that the fewest other volunteers can teach and isn't already full. My intution behind this was that if the rarest classes are selected, th