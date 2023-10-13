# Student Registration System | Group_Project1

**Author:** Jin YuHan Burgess, Sabrina Harris
**Date:** 28 October 2023

## Introduction

The Student Registration System is designed to manage and prioritize student registration based on their major, year, and registration day. It employs an AVL (Adelson-Velsky and Landis) tree data structure to efficiently manage student registration and maintain a balanced order. This system can handle undergraduate students and auditors.

## Overview
Create an algorithm that takes in a students and order them based off thier prioirty in order to determine who will be admitted into the Fall semester graduate course for Data Science. Enrollment is limited to 25 students and graduate students, undergraduate students, and auditors are eligible to apply for a place in the class. The algorithms will be able to update for students who are added and those who drop the course. 

## Prioritization Logic
1. Graduate students are given priority for enrollment, assuming they register by the end of orientation week.
   
3. Undergraduates are given second priority and amongst undergraduates.
    - priority is determined by whether the student is majoring in CS and/or math, what year they are in, and what day of orientation (1-5 inclusive) they register, in that order.
      
4. Auditors are permitted assuming there remain open seats, and priority is determined by what day of orientation (1-5 inclusive) they apply.
   
6. If any admitted student drops the class before the end of the second week of class, the open position is offered to the most qualified person who was not previously offered a place in the class.

## Key Classes

### `Node`

The `Node` class represents a node in the AVL tree. It contains information about a student's registration and related details, as follows:

- `name`: Student's name
- `major`: Student's major
- `year`: The year the student is in
- `reg_day`: Registration day
- `priority`: Priority value used for comparison and determining order
- `left`: Reference to the left child node
- `right`: Reference to the right child node
- `height`: The height of the node in the tree (used for balancing)

### `AVL_Tree`

The `AVL_Tree` class manages the AVL tree structure and operations. It includes the following key functionalities:

- `tree_height(node)`: Calculates the height of the subtree rooted at the given node.
- Rotation methods (e.g., `left_left_rotation`, `right_right_rotation`, `left_right_rotation`, `right_left_rotation`): Performs rotations to rebalance the tree.
- `insert(parent_node, name, major, year, reg_day, priority)`: Inserts a new student into the AVL tree while maintaining balance.
- `print_tree(node)`: Prints the tree in an order for visualization.

### `stud_registration`

The `stud_registration` class serves as the main application class to manage student registration. It handles student priority calculation and registration based on specific conditions. Key functionalities include:

- `audit_priority(reg_day)`: Calculates the priority level for auditing students based on registration day.
- `undgrad_priority(major, year, reg_day)`: Calculates the priority level for undergraduate students based on major, year, and registration day.
- `register_student(name, major, year, reg_day)`: Registers students based on their major, year, and registration day while assigning priorities.

## Dependencies
The script requires these Python Libraries:

`pandas:` For data manipulation and anaylsis

## Usage

The main part of the code demonstrates the use of the `stud_registration` class for student registration. Here are the steps to use the system:

1. Create an instance of the `stud_registration` class.
2. Use the `register_student` method to add students to the system.
3. The system will handle prioritization and maintain balanced order for student registration.
4. To view the lists of undergraduate and auditor students, use the `print_tree` method on the respective AVL tree instances (`undgrad_list` and `auditor_list`).

```python
if __name__ == "__main__":
    reg_stud = stud_registration()

    # Insert students
    reg_stud.register_student('Alice', 'cs', 3, 3)
    reg_stud.register_student('Bob', 'math', 2, 4)
    reg_stud.register_student('Charlie', 'art', 2, 1)
    reg_stud.register_student('David', 'cs', 3, 2)
    reg_stud.register_student('Eve', 'art', 5, 1)
    reg_stud.register_student('Frank', 'cs', 0, 1)

    print("Undgrad List:")
    reg_stud.undgrad_list.print_tree(reg_stud.undgrad_list.root)

    print("Auditor List:")
    reg_stud.auditor_list.print_tree(reg_stud.auditor_list.root)
```

