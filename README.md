# Group_Project1

## Overview
Create an algorithm that takes in a students and order them based off thier prioirty in order to determine who will be admitted into the Fall semester graduate course for Data Science. Enrollment is limited to 25 students and graduate students, undergraduate students, and auditors are eligible to apply for a place in the class. The algorithms will be able to update for students who are added and those who drop the course. 

## Prioritization Logic
1. Graduate students are given priority for enrollment, assuming they register by the end of orientation week.
   
3. Undergraduates are given second priority and amongst undergraduates.
    - priority is determined by whether the student is majoring in CS and/or math, what year they are in, and what day of orientation (1-5 inclusive) they register, in that order.
      
4. Auditors are permitted assuming there remain open seats, and priority is determined by what day of orientation (1-5 inclusive) they apply.
   
6. If any admitted student drops the class before the end of the second week of class, the open position is offered to the most qualified person who was not previously offered a place in the class.

## Dependencies
The script requires these Python Libraries:

`pandas:` For data manipulation and anaylsis

## Features
**Max Heap:** `build_heap()`, `max_heap()` implements the data structure on the variables.

**Student Prioitization:** `compare_tuple_list()` is used to determine the priority of each student.

_Auxiliary Prioitization:_ `num_major()` and `reg_Date()` used within the `compare_tuple_list()`

**Update Heap:** `insert_heap()` and `delete_heap()` used to handle students who are applying for the course and those who are dropping the course. 

