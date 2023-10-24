
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random

# class Node deals with the information about the relation and information that each node contains 
class Node:
    def __init__(self, name, major, year, reg_day, priority):
        self.name = name # student's name
        self.major = major # major of the student
        self.year = year # the year the student is in
        self.reg_day = reg_day # day of registration 
        self.priority = priority # used in comparsion based analysis for developing priority 

        # when inputing a node there is no child attached 
        self.left = None 
        self.right = None
        self.height = 1 # will be used to help determine rebalancing 

# class AVL_Tree contains information about the structure of AVL_Tree and how to maintain it
# such as the rotation, insertion, and deletion form the tree
class AVL_Tree:
    def __init__(self):
        self.root = None # initially, the tree is empty because we have not put in any new students 

    # determines the tree height of each subtree, helps to determine if the subtree needs to be rotated and in which direction
    def tree_height(self, node):
        if node is None:
            return 0
        left_height = self.tree_height(node.left) # getting the height of the left subtree
        right_height = self.tree_height(node.right) # getting the height of the right subtree
        return max(left_height, right_height) + 1 # return the subtree which has the largest depth (adding 1 since we start our count at 0)
    
    def left_left_rotation(self, node):
        if node is not None and node.right is not None:
            new_parent = node.right # setting the right child as the pivot/new parent
            temp_var = new_parent.left # temparary variable that will be reattached when tree has been rotated
            new_parent.left = node # setting parent node as left child
            node.right = temp_var # since the node is going to be smaller than the temp var, it is going to be placed as right child

            # since we repositioned the parent node and the right child's position, we need to update the height of each
            node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1 
            new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

            # return the new_parent for recalculation to see if the tree is now balanced
            return new_parent
        else:
            return node
        
    def right_right_rotation(self, node):
        if node is not None and node.left is not None:
            new_parent = node.left # setting the left child as the pivot/new parent
            temp_var = new_parent.right # temparary variable that will be reattached when tree has been rotated
            new_parent.right = node # setting parent node as right child
            node.left = temp_var # since the node is going to be bigger than the temp var, it is going to be placed as left child

            # since we repositioned the parent node and the right child's position, we need to update the height of each
            node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1
            new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

            # return the new_parent for recalculation to see if the tree is now balanced
            return new_parent
        else:
            return node

    def left_right_rotation(self, node):
        node.left = self.left_left_rotation(node.left)
        return self.right_right_rotation(node)

    def right_left_rotation(self, node):
        node.right = self.right_right_rotation(node.right)
        return self.left_left_rotation(node)
 
    # inserting a new student into the AVL tree
    def insert(self, parent_node, name, major, year, reg_day, priority):
        # set the student to the root node if it is going to be ther first thing in the list 
        if parent_node is None:
            # in here we care using the node class to create the root node
            return Node(name, major, year, reg_day, priority)  

        # We are inserting the following students based on their priority value
        # the new student has a lower priority value than the students already in the tree
        if priority < parent_node.priority:
            parent_node.left = self.insert(parent_node.left, name, major, year, reg_day, priority)
            
        # the new student has a higher priority value than the students already in the tree
        else:
            parent_node.right = self.insert(parent_node.right, name, major, year, reg_day, priority)

        # once we add the new node we need to update the height of our tree that will be used to determine 
        # balance of our new tree
        parent_node.height = max(self.tree_height(parent_node.left), self.tree_height(parent_node.right)) + 1
       
        # if the balance is greater than 1 or smaller than -1 (so 2 or -2) means we are no longer balanced 
        # thus we need to rotate the nodes to rebalance the tree such that it is between -1>= x =<1
        balance = self.tree_height(parent_node.left) - self.tree_height(parent_node.right)
        
        # there is a string of left child that outweighs how many right child there is in the subtree
        if balance > 1:
            if priority < parent_node.left.priority:
                return self.right_right_rotation(parent_node)
            else:
                return self.left_right_rotation(parent_node)
            
        # there is a string of right child that outweighs how many left child there is in the subtree
        if balance < -1:
            if priority > parent_node.right.priority:
                return self.left_left_rotation(parent_node)
            else:
                return self.right_left_rotation(parent_node)

        return parent_node
    
    # finding the lowest priority node in a given subarray that will be used in 
    # the delete_node function
    def find_min(self, node):
        if node is None:
            return None
        
        # only looking for left child node since they will contain the smaller priority
        while node.left is not None:
            node= node.left
        return node
    
    # deleting students from tree
    def delete_node(self, node, identifier):
        if node is None: # making sure nodes exists for traversal
            return node
        if identifier < node.identifier: # going through left subtree if identifier is less than identifier of the parent node
            node.left = self.delete_node(node.left, identifier)
        elif identifier > node.identifier:
            node.right = self.delete_node(node.right, identifier) # going through right subtree if identifier is greater than identifier of the parent node
        else: # student that we want to delete is found
            # looking to see where the child exist to see which node needs to be swapped with the one that is being removed 
            if node.left is None: 
                return node.right
            elif node.right is None:
                return node.left
            temp = self.find_min(node.right) # getting the left most child of the right child and putting it into its position
            # swaping the two nodes
            node.name, node.major, node.year, node.reg_day, node.priority, node.identifier = temp.name, temp.major, temp.year, temp.reg_day, temp.priority, temp.identifier
            node.right = self.delete_node(node.right, temp.identifier) # removing the node
            node.height = 1 + max(self.tree_height(node.left), self.tree_height(node.right)) # adjusting hight
        return node
    
    # setting unique identifier to nodes so we can traverse tree to delete
    def set_identifier(self, node, N, name_to_identifier):
        if node:
            N= self.set_identifier(node.right, N, name_to_identifier) # getting higest priority student 
            node.identifier = N # setting N which is number of nodes in tree to the node
            name_to_identifier[node.name] = N # adding the asssocation between name and identifer to the dictionary
            N = N - 1 
            N = self.set_identifier(node.left, N, name_to_identifier) # getting lower priority student 
        return N

    # appending into a list, the students from the avl_ tree in descending order
    def print_tree(self, node, admitted_students, max_students):

        if node and len(admitted_students) < max_students: # making sure node exists and that we have not reached limit of list
                self.print_tree(node.right, admitted_students,max_students) # getting the right most child (student with higher priority)
                if len(admitted_students) < max_students: # making sure that we are not at limit of list

                    # appending the information of the student node to the admitted list 
                    admitted_students.append([node.name, node.major, 
                                        node.year, 
                                        node.reg_day, 
                                        node.priority,
                                        ])
                self.print_tree(node.left, admitted_students,max_students) # getting the right most child (student with lesser priority)


class stud_registration:
    def __init__(self):
        self.registration_list = AVL_Tree() # prioritization structure of students

        
    # updates the student_dict when a new student is added to the tree


# Student Priority Code
# Code by Sabrina Harris
################################################################################################################################################
    def student_priority(self, major, year, reg_day):
        level = 0 #reset the level for each function call
        if year == 0: #for auditors
            level = level + (.5-(.1*(reg_day))) # level will equal 0.5 for registrations before orientation week, 0.4 for registrations on the first day, etc.
          
        elif year <5: # for undergraduate students
            if major == 'cs' or major == 'math' or major == 'ds':
                level = level+10 # adds 10 to the level for cs or math majors,
            level = level + year # adds 1,2,3, or 4 to the level based on the year.
            level = level +(.5-(.1*(reg_day))) #+0.5 for students registered before the orientation week, same as for auditors.
            
        else:
            level = 15 #for graduate students, level will automatically be 15.
        return level
    
################################################################################################################################################

    # adding new student to the AVL tree so long as they registered within the orientation period
    def register_student(self, name, year, reg_day, major):
        if int(reg_day) < 6:
            priority = self.student_priority(major, year, reg_day) # caluclte their priority
            self.registration_list.root = self.registration_list.insert(self.registration_list.root, name, major, year, reg_day, priority)
            
    # we are removing students based on the dictionary list. I am not updating tree because
    # I am running under the assumption that the class has already started and we already of a waitlist which is captured 
    # in the dictionary
    def remove_student(self, identifier):
        self.registration_list.root = self.registration_list.delete_node(self.registration_list.root, identifier)

    # creates a dataframe that returns the 25 admitted students 
    def get_student_dataframe(self, max_students = 25):
        admitted_students = [] # list of admitted students 
        # calls this function to iterate through AVL tree and list students in descending order
        self.registration_list.print_tree(self.registration_list.root, admitted_students, max_students)

        # getting column for each data frame
        columns = ['Name', 'Major', 'Year', 'Reg Day', 'Priority'] # column names

        # return dataframe 
        return pd.DataFrame(admitted_students, columns=columns)
    
    
# Code by Jin YuHan Burgess

if __name__ == "__main__":
    reg_stud = stud_registration()

    random.seed(101) # set.seed for testing 

    # List of possible majors
    majors = ['cs', 'math', 'other', 'ds']

    # Function to generate a random student
    def generate_random_student(indx):
        name = f"student{indx}" # Random student name
        year = random.randint(1, 6) # Random year (greater than 0)
        if year == 0:
            major = 'none' # these are auditors
        elif year > 4:
            major = 'ds' # data science is the major so those in graduate program are on this track
        else:
            major = random.choice(majors) # Random major
        reg_day = random.randint(0, 10) # Random registration day (greater than or equal to 0)

        return name, year, reg_day, major


    # Generate a list of random students
    num_students = 50 # Change this to the number of students you want
    random_students = [generate_random_student(indx) for indx in range(num_students)] # under score in for_ in... represents that the loop variable is not needed


    # Print the generated students
    for student in random_students:
        reg_stud.register_student(student[0], student[1], student[2], student[3])
    
    name_to_identifier = {} # creating dictionary between unique identifier and student name (unique identifier is based on the location it is within the avl_tree)

    # once all the insertions are done, we set unique identifiers to each student. Students with highest priority are considered right most child and will have a higher number
    # identification and vice versa for lowest priority students 
    x = reg_stud.registration_list.set_identifier(reg_stud.registration_list.root, int(num_students), name_to_identifier) 


    admitted = reg_stud.get_student_dataframe()
    print(admitted)

    random.seed(101)

    x = admitted.sample(n = 3, replace = False)
    print(x)


    random.seed(101)
    for indx in range(len(x)):
        stud = x._get_value(indx, 0, takeable = True) # gets student name from the sample 
        identifier = name_to_identifier[stud] # finds the identifer that is attached to the student
        reg_stud.remove_student(identifier) # remove student based of their identifier
                
    # return updated dataframe
    admitted = reg_stud.get_student_dataframe()
    print(admitted)

# Code by Jin YuHan Burgess

# Code by Jin YuHan Burgess
# This line of code clearly shows students who register within the orientation are admitted while those who do not sign up within the orientation period are not admitted. I set both students as the highest priority of Graduate student where one registered within the orientation while the other did not. 
    reg_stud.register_student('student0', 6, 6,'ds') 
    reg_stud.register_student('student01', 6, 0,'ds')

    admitted = reg_stud.get_student_dataframe()
    print(admitted)

# Code by Jin YuHan Burgess



































import numpy as np
import matplotlib as plt
import pandas as pd
import random


# class Node deals with the information about the relation and information that each node contains 
class Node:
    def __init__(self, name, major, year, reg_day, priority):
        self.name = name # student's name
        self.major = major # major of the student
        self.year = year # the year the student is in
        self.reg_day = reg_day # day of registration 
        self.priority = priority # used in comparsion based analysis for developing priority 

        # when inputing a node there is no child attached 
        self.left = None 
        self.right = None
        self.height = 1 # will be used to help determine rebalancing 

# class AVL_Tree contains information about the structure of AVL_Tree and how to maintain it
# such as the rotation, insertion, and deletion form the tree
class AVL_Tree:
    def __init__(self):
        self.root = None # initially, the tree is empty because we have not put in any new students 

    # determines the tree height of each subtree, helps to determine if the subtree needs to be rotated and in which direction
    def tree_height(self, node):
        if node is None:
            return 0
        left_height = self.tree_height(node.left) # getting the height of the left subtree
        right_height = self.tree_height(node.right) # getting the height of the right subtree
        return max(left_height, right_height) + 1 # return the subtree which has the largest depth (adding 1 since we start our count at 0)
    
    def left_left_rotation(self, node):
        if node is not None and node.right is not None:
            new_parent = node.right # setting the right child as the pivot/new parent
            temp_var = new_parent.left # temparary variable that will be reattached when tree has been rotated
            new_parent.left = node # setting parent node as left child
            node.right = temp_var # since the node is going to be smaller than the temp var, it is going to be placed as right child

            # since we repositioned the parent node and the right child's position, we need to update the height of each
            node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1 
            new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

            # return the new_parent for recalculation to see if the tree is now balanced
            return new_parent
        else:
            return node
        
    def right_right_rotation(self, node):
        if node is not None and node.left is not None:
            new_parent = node.left # setting the left child as the pivot/new parent
            temp_var = new_parent.right # temparary variable that will be reattached when tree has been rotated
            new_parent.right = node # setting parent node as right child
            node.left = temp_var # since the node is going to be bigger than the temp var, it is going to be placed as left child

            # since we repositioned the parent node and the right child's position, we need to update the height of each
            node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1
            new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

            # return the new_parent for recalculation to see if the tree is now balanced
            return new_parent
        else:
            return node

    def left_right_rotation(self, node):
        node.left = self.left_left_rotation(node.left)
        return self.right_right_rotation(node)

    def right_left_rotation(self, node):
        node.right = self.right_right_rotation(node.right)
        return self.left_left_rotation(node)
 
    # inserting a new student into the AVL tree
    def insert(self, parent_node, name, major, year, reg_day, priority):
        # set the student to the root node if it is going to be ther first thing in the list 
        if parent_node is None:
            # in here we care using the node class to create the root node
            return Node(name, major, year, reg_day, priority)  

        # We are inserting the following students based on their priority value
        # the new student has a lower priority value than the students already in the tree
        if priority < parent_node.priority:
            parent_node.left = self.insert(parent_node.left, name, major, year, reg_day, priority)
            
        # the new student has a higher priority value than the students already in the tree
        else:
            parent_node.right = self.insert(parent_node.right, name, major, year, reg_day, priority)

        # once we add the new node we need to update the height of our tree that will be used to determine 
        # balance of our new tree
        parent_node.height = max(self.tree_height(parent_node.left), self.tree_height(parent_node.right)) + 1
       
        # if the balance is greater than 1 or smaller than -1 (so 2 or -2) means we are no longer balanced 
        # thus we need to rotate the nodes to rebalance the tree such that it is between -1>= x =<1
        balance = self.tree_height(parent_node.left) - self.tree_height(parent_node.right)
        
        # there is a string of left child that outweighs how many right child there is in the subtree
        if balance > 1:
            if priority < parent_node.left.priority:
                return self.right_right_rotation(parent_node)
            else:
                return self.left_right_rotation(parent_node)
            
        # there is a string of right child that outweighs how many left child there is in the subtree
        if balance < -1:
            if priority > parent_node.right.priority:
                return self.left_left_rotation(parent_node)
            else:
                return self.right_left_rotation(parent_node)

        return parent_node
    
    # finding the lowest priority node in a given subarray that will be used in 
    # the delete_node function
    def find_min(self, node):
        if node is None:
            return None
        
        # only looking for left child node since they will contain the smaller priority
        while node.left is not None:
            node= node.left
        return node
    
    # deleting students from tree
    def delete_node(self, node, identifier):
        if node is None: # making sure nodes exists for traversal
            return node
        if identifier < node.identifier: # going through left subtree if identifier is less than identifier of the parent node
            node.left = self.delete_node(node.left, identifier)
        elif identifier > node.identifier:
            node.right = self.delete_node(node.right, identifier) # going through right subtree if identifier is greater than identifier of the parent node
        else: # student that we want to delete is found
            # looking to see where the child exist to see which node needs to be swapped with the one that is being removed 
            if node.left is None: 
                return node.right
            elif node.right is None:
                return node.left
            temp = self.find_min(node.right) # getting the left most child of the right child and putting it into its position
            # swaping the two nodes
            node.name, node.major, node.year, node.reg_day, node.priority, node.identifier = temp.name, temp.major, temp.year, temp.reg_day, temp.priority, temp.identifier
            node.right = self.delete_node(node.right, temp.identifier) # removing the node
            node.height = 1 + max(self.tree_height(node.left), self.tree_height(node.right)) # adjusting hight
        return node
    
    # setting unique identifier to nodes so we can traverse tree to delete
    def set_identifier(self, node, N, name_to_identifier):
        if node:
            N= self.set_identifier(node.right, N, name_to_identifier) # getting higest priority student 
            node.identifier = N # setting N which is number of nodes in tree to the node
            name_to_identifier[node.name] = N # adding the asssocation between name and identifer to the dictionary
            N = N - 1 
            N = self.set_identifier(node.left, N, name_to_identifier) # getting lower priority student 
        return N

    # appending into a list, the students from the avl_ tree in descending order
    def print_tree(self, node, admitted_students, max_students):

        if node and len(admitted_students) < max_students: # making sure node exists and that we have not reached limit of list
                self.print_tree(node.right, admitted_students,max_students) # getting the right most child (student with higher priority)
                if len(admitted_students) < max_students: # making sure that we are not at limit of list

                    # appending the information of the student node to the admitted list 
                    admitted_students.append([node.name, node.major, 
                                        node.year, 
                                        node.reg_day, 
                                        node.priority,
                                        ])
                self.print_tree(node.left, admitted_students,max_students) # getting the right most child (student with lesser priority)


class stud_registration:
    def __init__(self):
        self.registration_list = AVL_Tree() # prioritization structure of students

        
    # updates the student_dict when a new student is added to the tree


# Student Priority Code
# Code by Sabrina Harris
################################################################################################################################################
    def student_priority(self, major, year, reg_day):
        level = 0 #reset the level for each function call
        if year == 0: #for auditors
            level = level + (.5-(.1*(reg_day))) # level will equal 0.5 for registrations before orientation week, 0.4 for registrations on the first day, etc.
          
        elif year <5: # for undergraduate students
            if major == 'cs' or major == 'math' or major == 'ds':
                level = level+10 # adds 10 to the level for cs or math majors,
            level = level + year # adds 1,2,3, or 4 to the level based on the year.
            level = level +(.5-(.1*(reg_day))) #+0.5 for students registered before the orientation week, same as for auditors.
            
        else:
            level = 15 #for graduate students, level will automatically be 15.
        return level
    
################################################################################################################################################

    # adding new student to the AVL tree so long as they registered within the orientation period
    def register_student(self, name, year, reg_day, major):
        if int(reg_day) < 6:
            priority = self.student_priority(major, year, reg_day) # caluclte their priority
            self.registration_list.root = self.registration_list.insert(self.registration_list.root, name, major, year, reg_day, priority)
            
    # we are removing students based on the dictionary list. I am not updating tree because
    # I am running under the assumption that the class has already started and we already of a waitlist which is captured 
    # in the dictionary
    def remove_student(self, name, identifier):
        self.registration_list.root = self.registration_list.delete_node(self.registration_list.root, identifier)

    # creates a dataframe that returns the 25 admitted students 
    def get_student_dataframe(self, max_students = 25):
        admitted_students = [] # list of admitted students 
        # calls this function to iterate through AVL tree and list students in descending order
        self.registration_list.print_tree(self.registration_list.root, admitted_students, max_students)

        # getting column for each data frame
        columns = ['Name', 'Major', 'Year', 'Reg Day', 'Priority'] # column names

        # return dataframe 
        return pd.DataFrame(admitted_students, columns=columns)
    
if __name__ == "__main__":
    reg_stud = stud_registration()

    random.seed(101) # set.seed for testing 

    # List of possible majors
    majors = ['cs', 'math', 'other', 'ds']

    # Function to generate a random student
    def generate_random_student(indx):
        name = f"student{indx}" # Random student name
        year = random.randint(1, 6) # Random year (greater than 0)
        if year == 0:
            major = 'none' # these are auditors
        elif year > 4:
            major = 'ds' # data science is the major so those in graduate program are on this track
        else:
            major = random.choice(majors) # Random major
        reg_day = random.randint(0, 10) # Random registration day (greater than or equal to 0)

        return name, year, reg_day, major
    

    def time_insertion(num_students):
            random_students = [generate_random_student(indx) for indx in range(num_students)]
            for student in random_students:
                reg_stud.register_student(student[0], student[1], student[2], student[3])

    num_students_range = range(1, 100, 1)
    RT_result = []

    for num_students in num_students_range:
        execution_time = timeit.timeit("time_insertion(num_students)", globals=globals(), number=1)
        RT_result.append(execution_time)
    name_to_identifier = {} # creating dictionary between unique identifier and student name (unique identifier is based on the location it is within the avl_tree)

    # once all the insertions are done, we set unique identifiers to each student. Students with highest priority are considered right most child and will have a higher number
    # identification and vice versa for lowest priority students 
    x = reg_stud.registration_list.set_identifier(reg_stud.registration_list.root, int(num_students), name_to_identifier) 


    admitted = reg_stud.get_student_dataframe()
    print(admitted)

# Code by Jin YuHan Burgess
# infomration used in timeit function https://note.nkmk.me/en/python-timeit-measure/#:~:text=timeit()%20as%20a%20string,()%20as%20the%20globals%20argument.


# if __name__ == "__main__":
#     reg_stud = stud_registration()

#     random.seed(101) # set.seed for testing 

#     # List of possible majors
#     majors = ['cs', 'math', 'other', 'ds']

#     # Function to generate a random student
#     def generate_random_student(indx):
#         name = f"student{indx}" # Random student name
#         year = random.randint(1, 6) # Random year (greater than 0)
#         if year == 0:
#             major = 'none' # these are auditors
#         elif year > 4:
#             major = 'ds' # data science is the major so those in graduate program are on this track
#         else:
#             major = random.choice(majors) # Random major
#         reg_day = random.randint(0, 10) # Random registration day (greater than or equal to 0)

#         return name, year, reg_day, major


#     # Generate a list of random students
#     num_students = 50 # Change this to the number of students you want
#     random_students = [generate_random_student(indx) for indx in range(num_students)] # under score in for_ in... represents that the loop variable is not needed


#     # Print the generated students
#     for student in random_students:
#         reg_stud.register_student(student[0], student[1], student[2], student[3])
    
#     # comparing to show that students that register after orientation day are not counted 
#     reg_stud.register_student('student0', 6, 6,'ds') 
#     reg_stud.register_student('student01', 6, 0,'ds')


#     name_to_identifier = {} # creating dictionary between unique identifier and student name (unique identifier is based on the location it is within the avl_tree)

#     # once all the insertions are done, we set unique identifiers to each student. Students with highest priority are considered right most child and will have a higher number
#     # identification and vice versa for lowest priority students 
#     x = reg_stud.registration_list.set_identifier(reg_stud.registration_list.root, int(num_students), name_to_identifier) 


    # admitted = reg_stud.get_student_dataframe()
    # print(admitted)
    # stud = 'student37'
    # x = admitted.sample()
    
    # print(x)
    # if stud in name_to_identifier:
    #     identifier = name_to_identifier[stud]
    #     reg_stud.remove_student(stud, identifier)

            
    # admitted = reg_stud.get_student_dataframe()
    # print(admitted)

# Code by Jin YuHan Burgess

# class Node deals with the information about the relation and information that each node contains 
class Node:
    def __init__(self, name, major, year, reg_day, priority):
        self.name = name # student's name
        self.major = major # major of the student
        self.year = year # the year the student is in
        self.reg_day = reg_day # day of registration 
        self.priority = priority # used in comparsion based analysis for developing priority 

        # when inputing a node there is no child attached 
        self.left = None 
        self.right = None
        self.height = 1 # will be used to help determine rebalancing 

# class AVL_Tree contains information about the structure of AVL_Tree and how to maintain it
# such as the rotation, insertion, and deletion form the tree
class AVL_Tree:
    def __init__(self):
        self.root = None # initially, the tree is empty because we have not put in any new students 

    # determines the tree height of each subtree, helps to determine if the subtree needs to be rotated and in which direction
    def tree_height(self, node):
        if node is None:
            return 0
        left_height = self.tree_height(node.left) # getting the height of the left subtree
        right_height = self.tree_height(node.right) # getting the height of the right subtree
        return max(left_height, right_height) + 1 # return the subtree which has the largest depth (adding 1 since we start our count at 0)
    
    def left_left_rotation(self, node):
        if node is not None and node.right is not None:
            new_parent = node.right # setting the right child as the pivot/new parent
            temp_var = new_parent.left # temparary variable that will be reattached when tree has been rotated
            new_parent.left = node # setting parent node as left child
            node.right = temp_var # since the node is going to be smaller than the temp var, it is going to be placed as right child

            # since we repositioned the parent node and the right child's position, we need to update the height of each
            node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1 
            new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

            # return the new_parent for recalculation to see if the tree is now balanced
            return new_parent
        else:
            return node
        
    def right_right_rotation(self, node):
        if node is not None and node.left is not None:
            new_parent = node.left # setting the left child as the pivot/new parent
            temp_var = new_parent.right # temparary variable that will be reattached when tree has been rotated
            new_parent.right = node # setting parent node as right child
            node.left = temp_var # since the node is going to be bigger than the temp var, it is going to be placed as left child

            # since we repositioned the parent node and the right child's position, we need to update the height of each
            node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1
            new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

            # return the new_parent for recalculation to see if the tree is now balanced
            return new_parent
        else:
            return node

    def left_right_rotation(self, node):
        node.left = self.left_left_rotation(node.left)
        return self.right_right_rotation(node)

    def right_left_rotation(self, node):
        node.right = self.right_right_rotation(node.right)
        return self.left_left_rotation(node)
 
    # inserting a new student into the AVL tree
    def insert(self, parent_node, name, major, year, reg_day, priority):
        # set the student to the root node if it is going to be ther first thing in the list 
        if parent_node is None:
            # in here we care using the node class to create the root node
            return Node(name, major, year, reg_day, priority)  

        # We are inserting the following students based on their priority value
        # the new student has a lower priority value than the students already in the tree
        if priority < parent_node.priority:
            parent_node.left = self.insert(parent_node.left, name, major, year, reg_day, priority)
            
        # the new student has a higher priority value than the students already in the tree
        else:
            parent_node.right = self.insert(parent_node.right, name, major, year, reg_day, priority)

        # once we add the new node we need to update the height of our tree that will be used to determine 
        # balance of our new tree
        parent_node.height = max(self.tree_height(parent_node.left), self.tree_height(parent_node.right)) + 1
       
        # if the balance is greater than 1 or smaller than -1 (so 2 or -2) means we are no longer balanced 
        # thus we need to rotate the nodes to rebalance the tree such that it is between -1>= x =<1
        balance = self.tree_height(parent_node.left) - self.tree_height(parent_node.right)
        
        # there is a string of left child that outweighs how many right child there is in the subtree
        if balance > 1:
            if priority < parent_node.left.priority:
                return self.right_right_rotation(parent_node)
            else:
                return self.left_right_rotation(parent_node)
            
        # there is a string of right child that outweighs how many left child there is in the subtree
        if balance < -1:
            if priority > parent_node.right.priority:
                return self.left_left_rotation(parent_node)
            else:
                return self.right_left_rotation(parent_node)

        return parent_node
    
    # finding the lowest priority node in a given subarray that will be used in 
    # the delete_node function
    def find_min(self, node):
        if node is None:
            return None
        
        # only looking for left child node since they will contain the smaller priority
        while node.left is not None:
            node= node.left
        return node
    
    # deleting students from tree
    def delete_node(self, node, identifier):
        if node is None: # making sure nodes exists for traversal
            return node
        if identifier < node.identifier: # going through left subtree if identifier is less than identifier of the parent node
            node.left = self.delete_node(node.left, identifier)
        elif identifier > node.identifier:
            node.right = self.delete_node(node.right, identifier) # going through right subtree if identifier is greater than identifier of the parent node
        else: # student that we want to delete is found
            # looking to see where the child exist to see which node needs to be swapped with the one that is being removed 
            if node.left is None: 
                return node.right
            elif node.right is None:
                return node.left
            temp = self.find_min(node.right) # getting the left most child of the right child and putting it into its position
            # swaping the two nodes
            node.name, node.major, node.year, node.reg_day, node.priority, node.identifier = temp.name, temp.major, temp.year, temp.reg_day, temp.priority, temp.identifier
            node.right = self.delete_node(node.right, temp.identifier) # removing the node
            node.height = 1 + max(self.tree_height(node.left), self.tree_height(node.right)) # adjusting hight
        return node
    
    # setting unique identifier to nodes so we can traverse tree to delete
    def set_identifier(self, node, N, name_to_identifier):
        if node:
            N= self.set_identifier(node.right, N, name_to_identifier) # getting higest priority student 
            node.identifier = N # setting N which is number of nodes in tree to the node
            name_to_identifier[node.name] = N # adding the asssocation between name and identifer to the dictionary
            N = N - 1 
            N = self.set_identifier(node.left, N, name_to_identifier) # getting lower priority student 
        return N

    # appending into a list, the students from the avl_ tree in descending order
    def print_tree(self, node, admitted_students, max_students):

        if node and len(admitted_students) < max_students: # making sure node exists and that we have not reached limit of list
                self.print_tree(node.right, admitted_students,max_students) # getting the right most child (student with higher priority)
                if len(admitted_students) < max_students: # making sure that we are not at limit of list

                    # appending the information of the student node to the admitted list 
                    admitted_students.append([node.name, node.major, 
                                        node.year, 
                                        node.reg_day, 
                                        node.priority,
                                        ])
                self.print_tree(node.left, admitted_students,max_students) # getting the right most child (student with lesser priority)


class stud_registration:
    def __init__(self):
        self.registration_list = AVL_Tree() # prioritization structure of students

        
    # updates the student_dict when a new student is added to the tree

    def student_priority(self, major, year, reg_day):
        level = 0 #reset the level for each function call
        if year == 0: #for auditors
            level = level + (.5-(.1*(reg_day))) # level will equal 0.5 for registrations before orientation week, 0.4 for registrations on the first day, etc.
          
        elif year <5: # for undergraduate students
            if major == 'cs' or major == 'math' or major == 'ds':
                level = level+10 # adds 10 to the level for cs or math majors,
            level = level + year # adds 1,2,3, or 4 to the level based on the year.
            level = level +(.5-(.1*(reg_day))) #+0.5 for students registered before the orientation week, same as for auditors.
            
        else:
            level = 15 #for graduate students, level will automatically be 15.
        return level

    # adding new student to the AVL tree so long as they registered within the orientation period
    def register_student(self, name, year, reg_day, major):
        if int(reg_day) < 6:
            priority = self.student_priority(major, year, reg_day) # caluclte their priority
            self.registration_list.root = self.registration_list.insert(self.registration_list.root, name, major, year, reg_day, priority)
            
    # we are removing students based on the dictionary list. I am not updating tree because
    # I am running under the assumption that the class has already started and we already of a waitlist which is captured 
    # in the dictionary
    def remove_student(self, name, identifier):
        self.registration_list.root = self.registration_list.delete_node(self.registration_list.root, identifier)

    # creates a dataframe that returns the 25 admitted students 
    def get_student_dataframe(self, max_students = 25):
        admitted_students = [] # list of admitted students 
        # calls this function to iterate through AVL tree and list students in descending order
        self.registration_list.print_tree(self.registration_list.root, admitted_students, max_students)

        # getting column for each data frame
        columns = ['Name', 'Major', 'Year', 'Reg Day', 'Priority'] # column names

        # return dataframe 
        return pd.DataFrame(admitted_students, columns=columns)
    

if __name__ == "__main__":
    reg_stud = stud_registration()

    random.seed(101) # set.seed for testing 

    # List of possible majors
    majors = ['cs', 'math', 'other', 'ds']

    # Function to generate a random student
    def generate_random_student():
        name = f"student{random.randint(1, 100)}" # Random student name
        year = random.randint(1, 6) # Random year (greater than 0)
        if year == 0:
            major = 'none' # these are auditors
        elif year > 4:
            major = 'ds' # data science is the major so those in graduate program are on this track
        else:
            major = random.choice(majors) # Random major
        reg_day = random.randint(0, 10) # Random registration day (greater than or equal to 0)

        return name, year, reg_day, major


    # Generate a list of random students
    num_students = 50 # Change this to the number of students you want
    random_students = [generate_random_student() for _ in range(num_students)] # under score in for_ in... represents that the loop variable is not needed


    # Print the generated students
    for student in random_students:
        reg_stud.register_student(student[0], student[1], student[2], student[3])
    
    # comparing to show that students that register after orientation day are not counted 
    reg_stud.register_student('student0', 6, 6,'ds') 
    reg_stud.register_student('student01', 6, 0,'ds')


    name_to_identifier = {} # creating dictionary between unique identifier and student name (unique identifier is based on the location it is within the avl_tree)

    # once all the insertions are done, we set unique identifiers to each student. Students with highest priority are considered right most child and will have a higher number
    # identification and vice versa for lowest priority students 
    x = reg_stud.registration_list.set_identifier(reg_stud.registration_list.root, int(num_students), name_to_identifier) 


    admitted = reg_stud.get_student_dataframe()
    # print(admitted)
    stud = 'student7'

    if stud in name_to_identifier:
        identifier = name_to_identifier[stud]
        reg_stud.remove_student(stud, identifier)

            
    admitted = reg_stud.get_student_dataframe()
    print(admitted)


    ################################################################################################################################

import numpy as np
import matplotlib as plt
import pandas as pd
import random

# class Node deals with the information about the relation and information that each node contains 
class Node:
    def __init__(self, name, major, year, reg_day, priority):
        self.name = name # student's name
        self.major = major # major of the student
        self.year = year # the year the student is in
        self.reg_day = reg_day # day of registration 
        self.priority = priority # used in comparsion based analysis for developing priority 

        # when inputing a node there is no child attached 
        self.left = None 
        self.right = None
        self.height = 1 # will be used to help determine rebalancing 

# class AVL_Tree contains information about the structure of AVL_Tree and how to maintain it
# such as the rotation, insertion, and deletion form the tree
class AVL_Tree:
    def __init__(self):
        self.root = None # initially, the tree is empty because we have not put in any new students 

    # determines the tree height of each subtree, helps to determine if the subtree needs to be rotated and in which direction
    def tree_height(self, node):
        if node is None:
            return 0
        left_height = self.tree_height(node.left) # getting the height of the left subtree
        right_height = self.tree_height(node.right) # getting the height of the right subtree
        return max(left_height, right_height) + 1 # return the subtree which has the largest depth (adding 1 since we start our count at 0)
    
    def left_left_rotation(self, node):
        if node is not None and node.right is not None:
            new_parent = node.right # setting the right child as the pivot/new parent
            temp_var = new_parent.left # temparary variable that will be reattached when tree has been rotated
            new_parent.left = node # setting parent node as left child
            node.right = temp_var # since the node is going to be smaller than the temp var, it is going to be placed as right child

            # since we repositioned the parent node and the right child's position, we need to update the height of each
            node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1 
            new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

            # return the new_parent for recalculation to see if the tree is now balanced
            return new_parent
        else:
            return node
        
    def right_right_rotation(self, node):
        if node is not None and node.left is not None:
            new_parent = node.left # setting the left child as the pivot/new parent
            temp_var = new_parent.right # temparary variable that will be reattached when tree has been rotated
            new_parent.right = node # setting parent node as right child
            node.left = temp_var # since the node is going to be bigger than the temp var, it is going to be placed as left child

            # since we repositioned the parent node and the right child's position, we need to update the height of each
            node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1
            new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

            # return the new_parent for recalculation to see if the tree is now balanced
            return new_parent
        else:
            return node

    def left_right_rotation(self, node):
        node.left = self.left_left_rotation(node.left)
        return self.right_right_rotation(node)

    def right_left_rotation(self, node):
        node.right = self.right_right_rotation(node.right)
        return self.left_left_rotation(node)
 
    # inserting a new student into the AVL tree
    def insert(self, parent_node, name, major, year, reg_day, priority):
        # set the student to the root node if it is going to be ther first thing in the list 
        if parent_node is None:
            # in here we care using the node class to create the root node
            return Node(name, major, year, reg_day, priority)  

        # We are inserting the following students based on their priority value
        # the new student has a lower priority value than the students already in the tree
        if priority < parent_node.priority:
            parent_node.left = self.insert(parent_node.left, name, major, year, reg_day, priority)
            
        # the new student has a higher priority value than the students already in the tree
        else:
            parent_node.right = self.insert(parent_node.right, name, major, year, reg_day, priority)

        # once we add the new node we need to update the height of our tree that will be used to determine 
        # balance of our new tree
        parent_node.height = max(self.tree_height(parent_node.left), self.tree_height(parent_node.right)) + 1
       
        # if the balance is greater than 1 or smaller than -1 (so 2 or -2) means we are no longer balanced 
        # thus we need to rotate the nodes to rebalance the tree such that it is between -1>= x =<1
        balance = self.tree_height(parent_node.left) - self.tree_height(parent_node.right)
        
        # there is a string of left child that outweighs how many right child there is in the subtree
        if balance > 1:
            if priority < parent_node.left.priority:
                return self.right_right_rotation(parent_node)
            else:
                return self.left_right_rotation(parent_node)
            
        # there is a string of right child that outweighs how many left child there is in the subtree
        if balance < -1:
            if priority > parent_node.right.priority:
                return self.left_left_rotation(parent_node)
            else:
                return self.right_left_rotation(parent_node)

        return parent_node
    
        def find_min(self, node):
            if node is None:
                return None
            while node.left is not None:
                node= node.left
            return node
    
    def delete_node(self, node, identifier):
        if node is None:
            return node
        if identifier < node.identifier:
            node.left = self.delete_node(node.left, identifier)
        elif identifier > node.identifier:
            node.right = self.delete_node(node.right, identifier)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._find_min(node.right)
            node.name, node.major, node.year, node.reg_day, node.priority, node.identifier = temp.name, temp.major, temp.year, temp.reg_day, temp.priority, temp.identifier
            node.right = self.delete_node(node.right, temp.identifier)
            node.height = 1 + max(self.tree_height(node.left), self.tree_height(node.right))
        return node
    
    def set_identifier(self, node, N, name_to_identifier):
        if node:
            N= self.set_identifier(node.right, N, name_to_identifier)
            node.identifier = N 
            name_to_identifier[node.name] = N
            N = N - 1
            N = self.set_identifier(node.left, N, name_to_identifier)
        return N

    def print_tree(self, node, admitted_students, max_students):
        if node and len(admitted_students) < max_students:
                self.print_tree(node.right, admitted_students,max_students)
                if len(admitted_students) < max_students:
                    admitted_students.append([node.name, node.major, 
                                        node.year, 
                                        node.reg_day, 
                                        node.priority,
                                        ])
                # print(node.name, node.major, node.year, node.reg_day, node.priority, node.identifier)
                self.print_tree(node.left, admitted_students,max_students)

class stud_registration:
    def __init__(self):
        self.registration_list = AVL_Tree() # prioritization structure of students
        self.student_dict = {}  # Dictionary to store student information
        
    # updates the student_dict when a new student is added to the tree
    def update_student_dict(self):
        self.student_dict = {}  # Clear the dictionary
        
        self._update_student_dict(self.registration_list.root) # update dictionary based on new student

    # this is different because _update_student is intended for internal use in relation to update_student_dict
    # it should only be accessed within the classs it exists 
    def _update_student_dict(self, node):
        if node:
            # the set up of:
            # node.right
            # self.studnt_dict[node.name]
            # node.left
            # ensures that the dictionary will be ordered in a descending manner
            self._update_student_dict(node.right) 

            # Update the student_dict with the student's information
            self.student_dict[node.name] = {
                'major': node.major,
                'year': node.year,
                'reg_day': node.reg_day,
                'priority': node.priority
            }

            self._update_student_dict(node.left)

    def student_priority(self, major, year, reg_day):
        level = 0 #reset the level for each function call
        if year == 0: #for auditors
            level = level + (.5-(.1*(reg_day))) # level will equal 0.5 for registrations before orientation week, 0.4 for registrations on the first day, etc.
          
        elif year <5: # for undergraduate students
            if major == 'cs' or major == 'math':
                level = level+10 # adds 10 to the level for cs or math majors,
            level = level + year # adds 1,2,3, or 4 to the level based on the year.
            level = level +(.5-(.1*(reg_day))) #+0.5 for students registered before the orientation week, same as for auditors.
            
        else:
            level = 15 #for graduate students, level will automatically be 15.
        return level

    # adding new student to the AVL tree so long as they registered within the orientation period
    def register_student(self, name, year, reg_day, major):
        if int(reg_day) < 6:
            priority = self.student_priority(major, year, reg_day) # caluclte their priority
            self.registration_list.root = self.registration_list.insert(self.registration_list.root, name, major, year, reg_day, priority)
            
    # we are removing students based on the dictionary list. I am not updating tree because
    # I am running under the assumption that the class has already started and we already of a waitlist which is captured 
    # in the dictionary
    def remove_student(self, name, identifier):
        self.registration_list.root = self.registration_list.delete_node(self.registration_list.root, identifier)

    
    def get_student_dataframe(self, max_students = 25):
        admitted_students = []
        self.registration_list.print_tree(self.registration_list.root, admitted_students, max_students)

        # getting column for each data frame
        columns = ['Name', 'Major', 'Year', 'Reg Day', 'Priority']

        # return dataframe 
        return pd.DataFrame(admitted_students, columns=columns)
    

if __name__ == "__main__":
    reg_stud = stud_registration()

    random.seed(101)

    # List of possible majors
    majors = ['cs', 'math', 'other']

    # Function to generate a random student
    def generate_random_student():
        name = f"student{random.randint(1, 100)}" # Random student name
        year = random.randint(1, 6) # Random year (greater than 0)
        if year == 0:
            major = 'none'
        elif year > 4:
            major = 'data science'
        else:
            major = random.choice(majors) # Random major
        reg_day = random.randint(0, 10) # Random registration day (greater than or equal to 0)

        return name, year, reg_day, major


    # Generate a list of random students
    num_students = 50 # Change this to the number of students you want
    random_students = [generate_random_student() for _ in range(num_students)] # under score in for_ in... represents that the loop variable is not needed


    # Print the generated students
    for student in random_students:
        reg_stud.register_student(student[0], student[1], student[2], student[3])
    
    reg_stud.register_student('student0', 6, 6,'ds') # showing that those without 
    reg_stud.register_student('student0', 6, 0,'ds')

    name_to_identifier = {}
    x = reg_stud.registration_list.set_identifier(reg_stud.registration_list.root, int(num_students), name_to_identifier)
    stud = 'student99'
    if stud in name_to_identifier:
        identifier = name_to_identifier[stud]
        reg_stud.remove_student(stud, identifier)

          
    admitted = reg_stud.get_student_dataframe()
    print(admitted)

########################################################################################################################################

# class Node deals with the information about the relation and information that each node contains 
class Node:
    def __init__(self, name, major, year, reg_day, priority):
        self.name = name # student's name
        self.major = major # major of the student
        self.year = year # the year the student is in
        self.reg_day = reg_day # day of registration 
        self.priority = priority # used in comparsion based analysis for developing priority 

        # when inputing a node there is no child attached 
        self.left = None 
        self.right = None
        self.height = 1 # will be used to help determine rebalancing 

# class AVL_Tree contains information about the structure of AVL_Tree and how to maintain it
# such as the rotation, insertion, and deletion form the tree
class AVL_Tree:
    def __init__(self):
        self.root = None # initially, the tree is empty because we have not put in any new students 

    # determines the tree height of each subtree, helps to determine if the subtree needs to be rotated and in which direction
    def tree_height(self, node):
        if node is None:
            return 0
        left_height = self.tree_height(node.left) # getting the height of the left subtree
        right_height = self.tree_height(node.right) # getting the height of the right subtree
        return max(left_height, right_height) + 1 # return the subtree which has the largest depth (adding 1 since we start our count at 0)
    
    def left_left_rotation(self, node):
        if node is not None and node.right is not None:
            new_parent = node.right # setting the right child as the pivot/new parent
            temp_var = new_parent.left # temparary variable that will be reattached when tree has been rotated
            new_parent.left = node # setting parent node as left child
            node.right = temp_var # since the node is going to be smaller than the temp var, it is going to be placed as right child

            # since we repositioned the parent node and the right child's position, we need to update the height of each
            node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1 
            new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

            # return the new_parent for recalculation to see if the tree is now balanced
            return new_parent
        else:
            return node
        
    def right_right_rotation(self, node):
        if node is not None and node.left is not None:
            new_parent = node.left # setting the left child as the pivot/new parent
            temp_var = new_parent.right # temparary variable that will be reattached when tree has been rotated
            new_parent.right = node # setting parent node as right child
            node.left = temp_var # since the node is going to be bigger than the temp var, it is going to be placed as left child

            # since we repositioned the parent node and the right child's position, we need to update the height of each
            node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1
            new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

            # return the new_parent for recalculation to see if the tree is now balanced
            return new_parent
        else:
            return node

    def left_right_rotation(self, node):
        node.left = self.left_left_rotation(node.left)
        return self.right_right_rotation(node)

    def right_left_rotation(self, node):
        node.right = self.right_right_rotation(node.right)
        return self.left_left_rotation(node)
 
    # inserting a new student into the AVL tree
    def insert(self, parent_node, name, major, year, reg_day, priority):
        # set the student to the root node if it is going to be ther first thing in the list 
        if parent_node is None:
            # in here we care using the node class to create the root node
            return Node(name, major, year, reg_day, priority)  

        # We are inserting the following students based on their priority value
        # the new student has a lower priority value than the students already in the tree
        if priority < parent_node.priority:
            parent_node.left = self.insert(parent_node.left, name, major, year, reg_day, priority)
            
        # the new student has a higher priority value than the students already in the tree
        else:
            parent_node.right = self.insert(parent_node.right, name, major, year, reg_day, priority)

        # once we add the new node we need to update the height of our tree that will be used to determine 
        # balance of our new tree
        parent_node.height = max(self.tree_height(parent_node.left), self.tree_height(parent_node.right)) + 1
       
        # if the balance is greater than 1 or smaller than -1 (so 2 or -2) means we are no longer balanced 
        # thus we need to rotate the nodes to rebalance the tree such that it is between -1>= x =<1
        balance = self.tree_height(parent_node.left) - self.tree_height(parent_node.right)
        
        # there is a string of left child that outweighs how many right child there is in the subtree
        if balance > 1:
            if priority < parent_node.left.priority:
                return self.right_right_rotation(parent_node)
            else:
                return self.left_right_rotation(parent_node)
            
        # there is a string of right child that outweighs how many left child there is in the subtree
        if balance < -1:
            if priority > parent_node.right.priority:
                return self.left_left_rotation(parent_node)
            else:
                return self.right_left_rotation(parent_node)

        return parent_node
    
    def delete_node(self, node, identifier):
        if node is None:
            return node
        if identifier < node.identifier:
            node.left = self.delete_node(node.left, identifier)
        elif identifier > node.identifier:
            node.right = self.delete_node(node.right, identifier)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._find_min(node.right)
            node.name, node.major, node.year, node.reg_day, node.priority, node.identifier = temp.name, temp.major, temp.year, temp.reg_day, temp.priority, temp.identifier
            node.right = self.delete_node(node.right, temp.identifier)
            node.height = 1 + max(self.tree_height(node.left), self.tree_height(node.right))
        return node
    
    def set_identifier(self, node, N, name_to_identifier):
        if node:
            N= self.set_identifier(node.right, N, name_to_identifier)
            node.identifier = N 
            name_to_identifier[node.name] = N
            N = N - 1
            N = self.set_identifier(node.left, N, name_to_identifier)
        return N

    def print_tree(self, node, admitted):
        if node:
            self.print_tree(node.right)
            print(node.name, node.major, node.year, node.reg_day, node.priority, node.identifier)
            self.print_tree(node.left)

class stud_registration:
    def __init__(self):
        self.registration_list = AVL_Tree() # prioritization structure of students
        self.student_dict = {}  # Dictionary to store student information
        
    # updates the student_dict when a new student is added to the tree
    def update_student_dict(self):
        self.student_dict = {}  # Clear the dictionary
        
        self._update_student_dict(self.registration_list.root) # update dictionary based on new student

    # this is different because _update_student is intended for internal use in relation to update_student_dict
    # it should only be accessed within the classs it exists 
    def _update_student_dict(self, node):
        if node:
            # the set up of:
            # node.right
            # self.studnt_dict[node.name]
            # node.left
            # ensures that the dictionary will be ordered in a descending manner
            self._update_student_dict(node.right) 

            # Update the student_dict with the student's information
            self.student_dict[node.name] = {
                'major': node.major,
                'year': node.year,
                'reg_day': node.reg_day,
                'priority': node.priority
            }

            self._update_student_dict(node.left)

    def student_priority(self, major, year, reg_day):
        level = 0 #reset the level for each function call
        if year == 0: #for auditors
            level = level + (.5-(.1*(reg_day))) # level will equal 0.5 for registrations before orientation week, 0.4 for registrations on the first day, etc.
          
        elif year <5: # for undergraduate students
            if major == 'cs' or major == 'math':
                level = level+10 # adds 10 to the level for cs or math majors,
            level = level + year # adds 1,2,3, or 4 to the level based on the year.
            level = level +(.5-(.1*(reg_day))) #+0.5 for students registered before the orientation week, same as for auditors.
            
        else:
            level = 15 #for graduate students, level will automatically be 15.
        return level

    # adding new student to the AVL tree so long as they registered within the orientation period
    def register_student(self, name, year, reg_day, major):
        if int(reg_day) < 6:
            priority = self.student_priority(major, year, reg_day) # caluclte their priority
            self.registration_list.root = self.registration_list.insert(self.registration_list.root, name, major, year, reg_day, priority)
            
    # we are removing students based on the dictionary list. I am not updating tree because
    # I am running under the assumption that the class has already started and we already of a waitlist which is captured 
    # in the dictionary
    def remove_student(self, name, identifier):
        self.registration_list.root = self.registration_list.delete_node(self.registration_list.root, identifier)

    
    def get_student_dataframe(self, max_students=25):
        admitted_students = [] # building dataframe to visually represent students who are admided
        # count = 0 # only go through the top 25 in dictionary
        
        #     # adding student to dictionary
        #     admitted_students.append([name, student_info['major'], 
        #                          student_info['year'], 
        #                          student_info['reg_day'], 
        #                          student_info['priority']])
        #     count += 1

            # When there are 25 admitted students, we stop 
            # if count >= max_students:
            #     break

        # getting column for each data frame
        columns = ['Name', 'Major', 'Year', 'Reg Day', 'Priority']

        # return dataframe 
        return pd.DataFrame(admitted_students, columns=columns)
    

if __name__ == "__main__":
    reg_stud = stud_registration()

    random.seed(101)

    # List of possible majors
    majors = ['cs', 'math', 'other']

    # Function to generate a random student
    def generate_random_student():
        name = f"student{random.randint(1, 100)}" # Random student name
        year = random.randint(1, 6) # Random year (greater than 0)
        if year == 0:
            major = 'none'
        elif year > 4:
            major = 'data science'
        else:
            major = random.choice(majors) # Random major
        reg_day = random.randint(0, 10) # Random registration day (greater than or equal to 0)

        return name, year, reg_day, major


    # Generate a list of random students
    num_students = 50 # Change this to the number of students you want
    random_students = [generate_random_student() for _ in range(num_students)] # under score in for_ in... represents that the loop variable is not needed


    # Print the generated students
    for student in random_students:
        reg_stud.register_student(student[0], student[1], student[2], student[3])
    
    name_to_identifier = {}
    x = reg_stud.registration_list.set_identifier(reg_stud.registration_list.root, int(num_students), name_to_identifier)
    stud = 'student99'
    if stud in name_to_identifier:
        identifier = name_to_identifier[stud]
        reg_stud.remove_student(stud, identifier)

          
    admitted = reg_stud.get_student_dataframe(reg_stud.registration_list.root)
    print(admitted)

  ########################################################################################################################################
    
# class Node deals with the information about the relation and information that each node contains 
class Node:
    def __init__(self, name, major, year, reg_day, priority):
        self.name = name # student's name
        self.major = major # major of the student
        self.year = year # the year the student is in
        self.reg_day = reg_day # day of registration 
        self.priority = priority # used in comparsion based analysis for developing priority 

        # when inputing a node there is no child attached 
        self.left = None 
        self.right = None
        self.height = 1 # will be used to help determine rebalancing 

# class AVL_Tree contains information about the structure of AVL_Tree and how to maintain it
# such as the rotation, insertion, and deletion form the tree
class AVL_Tree:
    def __init__(self):
        self.root = None # initially, the tree is empty because we have not put in any new students 

    # determines the tree height of each subtree, helps to determine if the subtree needs to be rotated and in which direction
    def tree_height(self, node):
        if node is None:
            return 0
        left_height = self.tree_height(node.left) # getting the height of the left subtree
        right_height = self.tree_height(node.right) # getting the height of the right subtree
        return max(left_height, right_height) + 1 # return the subtree which has the largest depth (adding 1 since we start our count at 0)
    
    def left_left_rotation(self, node):
        if node is not None and node.right is not None:
            new_parent = node.right # setting the right child as the pivot/new parent
            temp_var = new_parent.left # temparary variable that will be reattached when tree has been rotated
            new_parent.left = node # setting parent node as left child
            node.right = temp_var # since the node is going to be smaller than the temp var, it is going to be placed as right child

            # since we repositioned the parent node and the right child's position, we need to update the height of each
            node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1 
            new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

            # return the new_parent for recalculation to see if the tree is now balanced
            return new_parent
        else:
            return node
        
    def right_right_rotation(self, node):
        if node is not None and node.left is not None:
            new_parent = node.left # setting the left child as the pivot/new parent
            temp_var = new_parent.right # temparary variable that will be reattached when tree has been rotated
            new_parent.right = node # setting parent node as right child
            node.left = temp_var # since the node is going to be bigger than the temp var, it is going to be placed as left child

            # since we repositioned the parent node and the right child's position, we need to update the height of each
            node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1
            new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

            # return the new_parent for recalculation to see if the tree is now balanced
            return new_parent
        else:
            return node

    def left_right_rotation(self, node):
        node.left = self.left_left_rotation(node.left)
        return self.right_right_rotation(node)

    def right_left_rotation(self, node):
        node.right = self.right_right_rotation(node.right)
        return self.left_left_rotation(node)
 
    # inserting a new student into the AVL tree
    def insert(self, parent_node, name, major, year, reg_day, priority):
        # set the student to the root node if it is going to be ther first thing in the list 
        if parent_node is None:
            # in here we care using the node class to create the root node
            return Node(name, major, year, reg_day, priority)  

        # We are inserting the following students based on their priority value
        # the new student has a lower priority value than the students already in the tree
        if priority < parent_node.priority:
            parent_node.left = self.insert(parent_node.left, name, major, year, reg_day, priority)
            
        # the new student has a higher priority value than the students already in the tree
        else:
            parent_node.right = self.insert(parent_node.right, name, major, year, reg_day, priority)

        # once we add the new node we need to update the height of our tree that will be used to determine 
        # balance of our new tree
        parent_node.height = max(self.tree_height(parent_node.left), self.tree_height(parent_node.right)) + 1
       
        # if the balance is greater than 1 or smaller than -1 (so 2 or -2) means we are no longer balanced 
        # thus we need to rotate the nodes to rebalance the tree such that it is between -1>= x =<1
        balance = self.tree_height(parent_node.left) - self.tree_height(parent_node.right)
        
        # there is a string of left child that outweighs how many right child there is in the subtree
        if balance > 1:
            if priority < parent_node.left.priority:
                return self.right_right_rotation(parent_node)
            else:
                return self.left_right_rotation(parent_node)
            
        # there is a string of right child that outweighs how many left child there is in the subtree
        if balance < -1:
            if priority > parent_node.right.priority:
                return self.left_left_rotation(parent_node)
            else:
                return self.right_left_rotation(parent_node)

        return parent_node
    
    def order_tree(self, node, waitlist):
        if node:
            waitlist = self.order_tree(node.right, waitlist)
            waitlist.append([node.name, node.major, node.year, node.reg_day, node.priority])
            waitlist = self.order_tree(node.left,waitlist)
        return waitlist


class stud_registration:
    def __init__(self):
        self.registration_list = AVL_Tree() # prioritization structure of students
        self.student_dict = {}  # Dictionary to store student information
        
    # updates the student_dict when a new student is added to the tree
    def update_student_dict(self):
        self.student_dict = {}  # Clear the dictionary
        self._update_student_dict(self.registration_list.root) # update dictionary based on new student

    # this is different because _update_student is intended for internal use in relation to update_student_dict
    # it should only be accessed within the classs it exists 
    def _update_student_dict(self, node):
        if node:
            # the set up of:
            # node.right
            # self.studnt_dict[node.name]
            # node.left
            # ensures that the dictionary will be ordered in a descending manner
            self._update_student_dict(node.right) 

            # Update the student_dict with the student's information
            self.student_dict[node.name] = {
                'major': node.major,
                'year': node.year,
                'reg_day': node.reg_day,
                'priority': node.priority
            }

            self._update_student_dict(node.left)

    def student_priority(self, major, year, reg_day):
        level = 0 #reset the level for each function call
        if year == 0: #for auditors
            level = level + (.5-(.1*(reg_day))) # level will equal 0.5 for registrations before orientation week, 0.4 for registrations on the first day, etc.
          
        elif year <5: # for undergraduate students
            if major == 'cs' or major == 'math':
                level = level+10 # adds 10 to the level for cs or math majors,
            level = level + year # adds 1,2,3, or 4 to the level based on the year.
            level = level +(.5-(.1*(reg_day))) #+0.5 for students registered before the orientation week, same as for auditors.
            
        else:
            level = 15 #for graduate students, level will automatically be 15.
        return level

    # adding new student to the AVL tree so long as they registered within the orientation period
    def register_student(self, name, year, reg_day, major):
        if int(reg_day) < 6:
            priority = self.student_priority(major, year, reg_day) # caluclte their priority
            self.registration_list.root = self.registration_list.insert(self.registration_list.root, name, major, year, reg_day, priority)
            
            self.update_student_dict()  # Update the student_dict
       
    # we are removing students based on the dictionary list. I am not updating tree because
    # I am running under the assumption that the class has already started and we already of a waitlist which is captured 
    # in the dictionary
    def remove_student(self, name):
        if name in self.student_dict:
            del self.student_dict[name] # delete item when key matches name

    # # returns the dictionary of students
    # def get_student_dict(self):
    #     return self.student_dict
    
    def get_student_dataframe(self, max_students=25):
        admitted_students = [] # building dataframe to visually represent students who are admided
        count = 0 # only go through the top 25 in dictionary
        for name, student_info in self.student_dict.items():
            # adding student to dictionary
            admitted_students.append([name, student_info['major'], 
                                 student_info['year'], 
                                 student_info['reg_day'], 
                                 student_info['priority']])
            count += 1

            # When there are 25 admitted students, we stop 
            if count >= max_students:
                break

        # getting column for each data frame
        columns = ['Name', 'Major', 'Year', 'Reg Day', 'Priority']

        # return dataframe 
        return pd.DataFrame(admitted_students, columns=columns)



if __name__ == "__main__":
    reg_stud = stud_registration()

    random.seed(101)

    # List of possible majors
    majors = ['cs', 'math', 'other']

    # Function to generate a random student
    def generate_random_student():
        name = f"student{random.randint(1, 100)}" # Random student name
        year = random.randint(1, 6) # Random year (greater than 0)
        if year == 0:
            major = 'none'
        elif year > 4:
            major = 'data science'
        else:
            major = random.choice(majors) # Random major
        reg_day = random.randint(0, 10) # Random registration day (greater than or equal to 0)

        return name, year, reg_day, major


    # Generate a list of random students
    num_students = 5 # Change this to the number of students you want
    random_students = [generate_random_student() for _ in range(num_students)] # under score in for_ in... represents that the loop variable is not needed


    # Print the generated students
    for student in random_students:
        reg_stud.register_student(student[0], student[1], student[2], student[3])

    new_waitlist = {}
    for student_name, student_info in waitlist:
        new_waitlist[student_name] = (student_info['major'], student_info['year'], student_info['reg_day'], student_info['priority'])
    print(new_waitlist)


########################################################################################################################################


# class Node deals with the information about the relation and information that each node contains 
class Node:
    def __init__(self, name, major, year, reg_day, priority):
        self.name = name # student's name
        self.major = major # major of the student
        self.year = year # the year the student is in
        self.reg_day = reg_day # day of registration 
        self.priority = priority # used in comparsion based analysis for developing priority 

        # when inputing a node there is no child attached 
        self.left = None 
        self.right = None
        self.height = 1 # will be used to help determine rebalancing 

# class AVL_Tree contains information about the structure of AVL_Tree and how to maintain it
# such as the rotation, insertion, and deletion form the tree
class AVL_Tree:
    def __init__(self):
        self.root = None # initially, the tree is empty because we have not put in any new students 

    # determines the tree height of each subtree, helps to determine if the subtree needs to be rotated and in which direction
    def tree_height(self, node):
        if node is None:
            return 0
        left_height = self.tree_height(node.left) # getting the height of the left subtree
        right_height = self.tree_height(node.right) # getting the height of the right subtree
        return max(left_height, right_height) + 1 # return the subtree which has the largest depth (adding 1 since we start our count at 0)
    
    def left_left_rotation(self, node):
        if node is not None and node.right is not None:
            new_parent = node.right # setting the right child as the pivot/new parent
            temp_var = new_parent.left # temparary variable that will be reattached when tree has been rotated
            new_parent.left = node # setting parent node as left child
            node.right = temp_var # since the node is going to be smaller than the temp var, it is going to be placed as right child

            # since we repositioned the parent node and the right child's position, we need to update the height of each
            node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1 
            new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

            # return the new_parent for recalculation to see if the tree is now balanced
            return new_parent
        else:
            return node
        
    def right_right_rotation(self, node):
        if node is not None and node.left is not None:
            new_parent = node.left # setting the left child as the pivot/new parent
            temp_var = new_parent.right # temparary variable that will be reattached when tree has been rotated
            new_parent.right = node # setting parent node as right child
            node.left = temp_var # since the node is going to be bigger than the temp var, it is going to be placed as left child

            # since we repositioned the parent node and the right child's position, we need to update the height of each
            node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1
            new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

            # return the new_parent for recalculation to see if the tree is now balanced
            return new_parent
        else:
            return node

    def left_right_rotation(self, node):
        node.left = self.left_left_rotation(node.left)
        return self.right_right_rotation(node)

    def right_left_rotation(self, node):
        node.right = self.right_right_rotation(node.right)
        return self.left_left_rotation(node)
 
    # inserting a new student into the AVL tree
    def insert(self, parent_node, name, major, year, reg_day, priority):
        # set the student to the root node if it is going to be ther first thing in the list 
        if parent_node is None:
            # in here we care using the node class to create the root node
            return Node(name, major, year, reg_day, priority)  

        # We are inserting the following students based on their priority value
        # the new student has a lower priority value than the students already in the tree
        if priority < parent_node.priority:
            parent_node.left = self.insert(parent_node.left, name, major, year, reg_day, priority)
            
        # the new student has a higher priority value than the students already in the tree
        else:
            parent_node.right = self.insert(parent_node.right, name, major, year, reg_day, priority)

        # once we add the new node we need to update the height of our tree that will be used to determine 
        # balance of our new tree
        parent_node.height = max(self.tree_height(parent_node.left), self.tree_height(parent_node.right)) + 1
       
        # if the balance is greater than 1 or smaller than -1 (so 2 or -2) means we are no longer balanced 
        # thus we need to rotate the nodes to rebalance the tree such that it is between -1>= x =<1
        balance = self.tree_height(parent_node.left) - self.tree_height(parent_node.right)
        
        # there is a string of left child that outweighs how many right child there is in the subtree
        if balance > 1:
            if priority < parent_node.left.priority:
                return self.right_right_rotation(parent_node)
            else:
                return self.left_right_rotation(parent_node)
            
        # there is a string of right child that outweighs how many left child there is in the subtree
        if balance < -1:
            if priority > parent_node.right.priority:
                return self.left_left_rotation(parent_node)
            else:
                return self.right_left_rotation(parent_node)

        return parent_node
    
    def order_tree(self, node, waitlist):
        if node:
            waitlist = self.order_tree(node.right, waitlist)
            waitlist.append([node.name, node.major, node.year, node.reg_day, node.priority])
            waitlist = self.order_tree(node.left,waitlist)
        return waitlist



class stud_registration:
    def __init__(self):
        self.registration_list = AVL_Tree() # prioritization structure of students
        self.student_dict = {}  # Dictionary to store student information
        
    # updates the student_dict when a new student is added to the tree
    def update_student_dict(self):
        self.student_dict = {}  # Clear the dictionary
        self._update_student_dict(self.registration_list.root) # update dictionary based on new student

    # this is different because _update_student is intended for internal use in relation to update_student_dict
    # it should only be accessed within the classs it exists 
    def _update_student_dict(self, node):
        if node:
            # the set up of:
            # node.right
            # self.studnt_dict[node.name]
            # node.left
            # ensures that the dictionary will be ordered in a descending manner
            self._update_student_dict(node.right) 

            # Update the student_dict with the student's information
            self.student_dict[node.name] = {
                'major': node.major,
                'year': node.year,
                'reg_day': node.reg_day,
                'priority': node.priority
            }

            self._update_student_dict(node.left)

    def student_priority(self, major, year, reg_day):
        level = 0 #reset the level for each function call
        if year == 0: #for auditors
            level = level + (.5-(.1*(reg_day))) # level will equal 0.5 for registrations before orientation week, 0.4 for registrations on the first day, etc.
          
        elif year <5: # for undergraduate students
            if major == 'cs' or major == 'math':
                level = level+10 # adds 10 to the level for cs or math majors,
            level = level + year # adds 1,2,3, or 4 to the level based on the year.
            level = level +(.5-(.1*(reg_day))) #+0.5 for students registered before the orientation week, same as for auditors.
            
        else:
            level = 15 #for graduate students, level will automatically be 15.
        return level

    # adding new student to the AVL tree so long as they registered within the orientation period
    def register_student(self, name, year, reg_day, major):
        if int(reg_day) < 6:
            priority = self.student_priority(major, year, reg_day) # caluclte their priority
            self.registration_list.root = self.registration_list.insert(self.registration_list.root, name, major, year, reg_day, priority)
            
            self.update_student_dict()  # Update the student_dict
       
    # we are removing students based on the dictionary list. I am not updating tree because
    # I am running under the assumption that the class has already started and we already of a waitlist which is captured 
    # in the dictionary
    def remove_student(self, name):
        if name in self.student_dict:
            del self.student_dict[name] # delete item when key matches name

    # # returns the dictionary of students
    # def get_student_dict(self):
    #     return self.student_dict
    
    def get_student_dataframe(self, max_students=25):
        admitted_students = [] # building dataframe to visually represent students who are admided
        count = 0 # only go through the top 25 in dictionary
        for name, student_info in self.student_dict.items():
            # adding student to dictionary
            admitted_students.append([name, student_info['major'], 
                                 student_info['year'], 
                                 student_info['reg_day'], 
                                 student_info['priority']])
            count += 1

            # When there are 25 admitted students, we stop 
            if count >= max_students:
                break

        # getting column for each data frame
        columns = ['Name', 'Major', 'Year', 'Reg Day', 'Priority']

        # return dataframe 
        return pd.DataFrame(admitted_students, columns=columns)



if __name__ == "__main__":
    reg_stud = stud_registration()


    random.seed(101)


    # List of possible majors
    majors = ['cs', 'math', 'other']

    # Function to generate a random student
    def generate_random_student():
        name = f"student{random.randint(1, 100)}" # Random student name
        year = random.randint(1, 6) # Random year (greater than 0)
        if year == 0:
            major = 'none'
        elif year > 4:
            major = 'data science'
        else:
            major = random.choice(majors) # Random major
        reg_day = random.randint(0, 10) # Random registration day (greater than or equal to 0)

        return name, year, reg_day, major


    # Generate a list of random students
    num_students = 50 # Change this to the number of students you want
    random_students = [generate_random_student() for _ in range(num_students)] # under score in for_ in... represents that the loop variable is not needed


    # Print the generated students
    for student in random_students:
        reg_stud.register_student(student[0], student[1], student[2], student[3])
        
    # reg_stud.registration_list.print_tree(reg_stud.registration_list.root)
    # print(reg_stud.get_student_dict())
    # # reg_stud.remove_student('7')
    # admitted = reg_stud.get_student_dict()
    # print(admitted)

    waitlist = reg_stud.registration_list.order_tree(reg_stud.registration_list.root, [])
    print(waitlist)


########################################################################################################################################

# class Node deals with the information about the relation and information that each node contains 
class Node:
    def __init__(self, name, major, year, reg_day, priority):
        self.name = name # student's name
        self.major = major # major of the student
        self.year = year # the year the student is in
        self.reg_day = reg_day # day of registration 
        self.priority = priority # used in comparsion based analysis for developing priority 

        # when inputing a node there is no child attached 
        self.left = None 
        self.right = None
        self.height = 1 # will be used to help determine rebalancing 

# class AVL_Tree contains information about the structure of AVL_Tree and how to maintain it
# such as the rotation, insertion, and deletion form the tree
class AVL_Tree:
    def __init__(self):
        self.root = None # initially, the tree is empty because we have not put in any new students 

    # determines the tree height of each subtree, helps to determine if the subtree needs to be rotated and in which direction
    def tree_height(self, node):
        if node is None:
            return 0
        left_height = self.tree_height(node.left) # getting the height of the left subtree
        right_height = self.tree_height(node.right) # getting the height of the right subtree
        return max(left_height, right_height) + 1 # return the subtree which has the largest depth (adding 1 since we start our count at 0)
    
    def left_left_rotation(self, node):
        new_parent = node.right # setting the right child as the pivot/new parent
        temp_var = new_parent.left # temparary variable that will be reattached when tree has been rotated
        new_parent.left = node # setting parent node as left child
        node.right = temp_var # since the node is going to be smaller than the temp var, it is going to be placed as right child

        # since we repositioned the parent node and the right child's position, we need to update the height of each
        node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1 
        new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

        # return the new_parent for recalculation to see if the tree is now balanced
        return new_parent
    
    def right_right_rotation(self, node):
        new_parent = node.left # setting the left child as the pivot/new parent
        temp_var = new_parent.right # temparary variable that will be reattached when tree has been rotated
        new_parent.right = node # setting parent node as right child
        node.left = temp_var # since the node is going to be bigger than the temp var, it is going to be placed as left child

        # since we repositioned the parent node and the right child's position, we need to update the height of each
        node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1
        new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

        # return the new_parent for recalculation to see if the tree is now balanced
        return new_parent

    def left_right_rotation(self, node):
        node.left = self.left_left_rotation(node.left)
        return self.right_right_rotation(node)

    def right_left_rotation(self, node):
        node.right = self.right_right_rotation(node.right)
        return self.left_left_rotation(node)
 
    # inserting a new student into the AVL tree
    def insert(self, parent_node, name, major, year, reg_day, priority):
        # set the student to the root node if it is going to be ther first thing in the list 
        if parent_node is None:
            # in here we care using the node class to create the root node
            return Node(name, major, year, reg_day, priority)  

        # We are inserting the following students based on their priority value
        # the new student has a lower priority value than the students already in the tree
        if priority < parent_node.priority:
            parent_node.left = self.insert(parent_node.left, name, major, year, reg_day, priority)
            
        # the new student has a higher priority value than the students already in the tree
        else:
            parent_node.right = self.insert(parent_node.right, name, major, year, reg_day, priority)

        # once we add the new node we need to update the height of our tree that will be used to determine 
        # balance of our new tree
        parent_node.height = max(self.tree_height(parent_node.left), self.tree_height(parent_node.right)) + 1
       
        # if the balance is greater than 1 or smaller than -1 (so 2 or -2) means we are no longer balanced 
        # thus we need to rotate the nodes to rebalance the tree such that it is between -1>= x =<1
        balance = self.tree_height(parent_node.left) - self.tree_height(parent_node.right)
        
        # there is a string of left child that outweighs how many right child there is in the subtree
        if balance > 1:
            if priority < parent_node.left.priority:
                return self.right_right_rotation(parent_node)
            else:
                return self.left_right_rotation(parent_node)
            
        # there is a string of right child that outweighs how many left child there is in the subtree
        if balance < -1:
            if priority > parent_node.right.priority:
                return self.left_left_rotation(parent_node)
            else:
                return self.right_left_rotation(parent_node)

        return parent_node
    



class stud_registration:
    def __init__(self):
        self.registration_list = AVL_Tree() # prioritization structure of students
        self.student_dict = {}  # Dictionary to store student information
        
    # updates the student_dict when a new student is added to the tree
    def update_student_dict(self):
        self.student_dict = {}  # Clear the dictionary
        self._update_student_dict(self.registration_list.root) # update dictionary based on new student

    # this is different because _update_student is intended for internal use in relation to update_student_dict
    # it should only be accessed within the classs it exists 
    def _update_student_dict(self, node):
        if node:
            # the set up of:
            # node.right
            # self.studnt_dict[node.name]
            # node.left
            # ensures that the dictionary will be ordered in a descending manner
            self._update_student_dict(node.right) 

            # Update the student_dict with the student's information
            self.student_dict[node.name] = {
                'major': node.major,
                'year': node.year,
                'reg_day': node.reg_day,
                'priority': node.priority
            }

            self._update_student_dict(node.left)

    def student_priority(self, major, year, reg_day):
        level = 0 #reset the level for each function call
        if year == 0: #for auditors
            level = level + (.5-(.1*(reg_day))) # level will equal 0.5 for registrations before orientation week, 0.4 for registrations on the first day, etc.
          
        elif year <5: # for undergraduate students
            if major == 'cs' or major == 'math':
                level = level+10 # adds 10 to the level for cs or math majors,
            level = level + year # adds 1,2,3, or 4 to the level based on the year.
            level = level +(.5-(.1*(reg_day))) #+0.5 for students registered before the orientation week, same as for auditors.
            
        else:
            level = 15 #for graduate students, level will automatically be 15.
        return level

    # adding new student to the AVL tree so long as they registered within the orientation period
    def register_student(self, name, year, reg_day, major):
        if int(reg_day) < 6:
            priority = self.student_priority(major, year, reg_day) # caluclte their priority
            self.registration_list.root = self.registration_list.insert(self.registration_list.root, name, major, year, reg_day, priority)
            self.update_student_dict()  # Update the student_dict
       
    # we are removing students based on the dictionary list. I am not updating tree because
    # I am running under the assumption that the class has already started and we already of a waitlist which is captured 
    # in the dictionary
    def remove_student(self, name):
        if name in self.student_dict:
            del self.student_dict[name] # delete item when key matches name

    # # returns the dictionary of students
    # def get_student_dict(self):
    #     return self.student_dict
    
    def get_student_dataframe(self, max_students=25):
        admitted_students = [] # building dataframe to visually represent students who are admided
        count = 0 # only go through the top 25 in dictionary
        for name, student_info in self.student_dict.items():
            # adding student to dictionary
            admitted_students.append([name, student_info['major'], 
                                 student_info['year'], 
                                 student_info['reg_day'], 
                                 student_info['priority']])
            count += 1

            # When there are 25 admitted students, we stop 
            if count >= max_students:
                break

        # getting column for each data frame
        columns = ['Name', 'Major', 'Year', 'Reg Day', 'Priority']

        # return dataframe 
        return pd.DataFrame(admitted_students, columns=columns)



if __name__ == "__main__":
    reg_stud = stud_registration()


    random.seed(101)


    # List of possible majors
    majors = ['cs', 'math', 'other']

    # Function to generate a random student
    def generate_random_student():
        name = f"student{random.randint(1, 100)}" # Random student name
        year = random.randint(1, 6) # Random year (greater than 0)
        if year == 0:
            major = 'none'
        elif year > 4:
            major = 'data science'
        else:
            major = random.choice(majors) # Random major
        reg_day = random.randint(0, 10) # Random registration day (greater than or equal to 0)

        return name, year, reg_day, major


    # Generate a list of random students
    num_students = 50 # Change this to the number of students you want
    random_students = [generate_random_student() for _ in range(num_students)] # under score in for_ in... represents that the loop variable is not needed


    # Print the generated students
    for student in random_students:
        reg_stud.register_student(student[0], student[1], student[2], student[3])
        
    # reg_stud.registration_list.print_tree(reg_stud.registration_list.root)
    print(reg_stud.get_student_dict())
    # # reg_stud.remove_student('7')
    # admitted = reg_stud.get_student_dict()
    # print(admitted)

#############################################################################################################################

import numpy as np
import matplotlib as plt
import pandas as pd

# class Node deals with the information about the relation and information that each node contains 
class Node:
    def __init__(self, name, major, year, reg_day, priority):
        self.name = name # student's name
        self.major = major # major of the student
        self.year = year # the year the student is in
        self.reg_day = reg_day # day of registration 
        self.priority = priority # used in comparsion based analysis for developing priority 

        # when inputing a node there is no child attached 
        self.left = None 
        self.right = None
        self.height = 1 # will be used to help determine rebalancing 

# class AVL_Tree contains information about the structure of AVL_Tree and how to maintain it
# such as the rotation, insertion, and deletion form the tree
class AVL_Tree:
    def __init__(self):
        self.root = None # initially, the tree is empty because we have not put in any new students 

    # determines the tree height of each subtree, helps to determine if the subtree needs to be rotated and in which direction
    def tree_height(self, node):
        if node is None:
            return 0
        left_height = self.tree_height(node.left) # getting the height of the left subtree
        right_height = self.tree_height(node.right) # getting the height of the right subtree
        return max(left_height, right_height) + 1 # return the subtree which has the largest depth (adding 1 since we start our count at 0)
    
    def left_left_rotation(self, node):
        new_parent = node.right # setting the right child as the pivot/new parent
        temp_var = new_parent.left # temparary variable that will be reattached when tree has been rotated
        new_parent.left = node # setting parent node as left child
        node.right = temp_var # since the node is going to be smaller than the temp var, it is going to be placed as right child

        # since we repositioned the parent node and the right child's position, we need to update the height of each
        node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1 
        new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

        # return the new_parent for recalculation to see if the tree is now balanced
        return new_parent
    
    def right_right_rotation(self, node):
        new_parent = node.left # setting the left child as the pivot/new parent
        temp_var = new_parent.right # temparary variable that will be reattached when tree has been rotated
        new_parent.right = node # setting parent node as right child
        node.left = temp_var # since the node is going to be bigger than the temp var, it is going to be placed as left child

        # since we repositioned the parent node and the right child's position, we need to update the height of each
        node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1
        new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

        # return the new_parent for recalculation to see if the tree is now balanced
        return new_parent

    def left_right_rotation(self, node):
        node.left = self.left_left_rotation(node.left)
        return self.right_right_rotation(node)

    def right_left_rotation(self, node):
        node.right = self.right_right_rotation(node.right)
        return self.left_left_rotation(node)
 
    # inserting a new student into the AVL tree
    def insert(self, parent_node, name, major, year, reg_day, priority):
        # set the student to the root node if it is going to be ther first thing in the list 
        if parent_node is None:
            # in here we care using the node class to create the root node
            return Node(name, major, year, reg_day, priority)  

        # We are inserting the following students based on their priority value
        # the new student has a lower priority value than the students already in the tree
        if priority < parent_node.priority:
            parent_node.left = self.insert(parent_node.left, name, major, year, reg_day, priority)
            
        # the new student has a higher priority value than the students already in the tree
        else:
            parent_node.right = self.insert(parent_node.right, name, major, year, reg_day, priority)

        # once we add the new node we need to update the height of our tree that will be used to determine 
        # balance of our new tree
        parent_node.height = max(self.tree_height(parent_node.left), self.tree_height(parent_node.right)) + 1
       
        # if the balance is greater than 1 or smaller than -1 (so 2 or -2) means we are no longer balanced 
        # thus we need to rotate the nodes to rebalance the tree such that it is between -1>= x =<1
        balance = self.tree_height(parent_node.left) - self.tree_height(parent_node.right)
        
        # there is a string of left child that outweighs how many right child there is in the subtree
        if balance > 1:
            if priority < parent_node.left.priority:
                return self.right_right_rotation(parent_node)
            else:
                return self.left_right_rotation(parent_node)
            
        # there is a string of right child that outweighs how many left child there is in the subtree
        if balance < -1:
            if priority > parent_node.right.priority:
                return self.left_left_rotation(parent_node)
            else:
                return self.right_left_rotation(parent_node)

        return parent_node


class stud_registration:
    def __init__(self):
        self.registraion_list = AVL_Tree() # prioritization structure of students
        self.student_dict = {}  # Dictionary to store student information

    # updates the student_dict when a new student is added to the tree
    def update_student_dict(self):
        self.student_dict = {}  # Clear the dictionary
        self._update_student_dict(self.registraion_list.root) # update dictionary based on new student

    # this is different because _update_student is intended for internal use in relation to update_student_dict
    # it should only be accessed within the classs it exists 
    def _update_student_dict(self, node):
        if node:
            # the set up of:
            # node.right
            # self.studnt_dict[node.name]
            # node.left
            # ensures that the dictionary will be ordered in a descending manner
            self._update_student_dict(node.right) 

            # Update the student_dict with the student's information
            self.student_dict[node.name] = {
                'major': node.major,
                'year': node.year,
                'reg_day': node.reg_day,
                'priority': node.priority
            }

            self._update_student_dict(node.left)

    def student_priority(self, major, year, reg_day):
        level = 0 #reset the level for each function call
        if year == 0: #for auditors
            level = level + (.5-(.1*(reg_day))) # level will equal 0.5 for registrations before orientation week, 0.4 for registrations on the first day, etc.
          
        elif year <5: # for undergraduate students
            if major == 'cs' or major == 'math':
                level = level+10 # adds 10 to the level for cs or math majors,
            level = level + year # adds 1,2,3, or 4 to the level based on the year.
            level = level +(.5-(.1*(reg_day))) #+0.5 for students registered before the orientation week, same as for auditors.
            
        else:
            level = 15 #for graduate students, level will automatically be 15.
        return level

    # adding new student to the AVL tree so long as they registered within the orientation period
    def register_student(self, name, major, year, reg_day):
        if int(reg_day) < 6:
            priority = self.student_priority(major, year, reg_day) # caluclte their priority
            self.registraion_list.root = self.registraion_list.insert(self.registraion_list.root, name, major, year, reg_day, priority)
            self.update_student_dict()  # Update the student_dict

    # we are removing students based on the dictionary list. I am not updating tree because
    # I am running under the assumption that the class has already started and we already of a waitlist which is captured 
    # in the dictionary
    def remove_student(self, name):
        if name in self.student_dict:
            del self.student_dict[name] # delete item when key matches name

    # # returns the dictionary of students
    # def get_student_dict(self):
    #     return self.student_dict
    
    def get_student_dataframe(self, max_students=25):
        admitted_students = [] # building dataframe to visually represent students who are admided
        count = 0 # only go through the top 25 in dictionary
        for name, student_info in self.student_dict.items():
            # adding student to dictionary
            admitted_students.append([name, student_info['major'], 
                                 student_info['year'], 
                                 student_info['reg_day'], 
                                 student_info['priority']])
            count += 1

            # When there are 25 admitted students, we stop 
            if count >= max_students:
                break

        # getting column for each data frame
        columns = ['Name', 'Major', 'Year', 'Reg Day', 'Priority']

        # return dataframe 
        return pd.DataFrame(admitted_students, columns=columns)



if __name__ == "__main__":
    reg_stud = stud_registration()

    # Insert students
    reg_stud.register_student('Alice', 'cs', 3, 3)
    reg_stud.register_student('Bob', 'math', 2, 4)
    reg_stud.register_student('Charlie', 'art', 2, 1)
    reg_stud.register_student('David', 'cs', 3, 2)
    reg_stud.register_student('Eve', 'art',  5, 1)
    reg_stud.register_student('Frank', 'cs',  0, 1)

    reg_stud.remove_student('Eve')

    students = reg_stud.get_student_dataframe()
    print(students)
   
##################################################################################################

# class Node deals with the information about the relation and information that each node contains 
class Node:
    def __init__(self, name, major, year, reg_day, priority):
        self.name = name # student's name
        self.major = major # major of the student
        self.year = year # the year the student is in
        self.reg_day = reg_day # day of registration 
        self.priority = priority # used in comparsion based analysis for developing priority 

        # when inputing a node there is no child attached 
        self.left = None 
        self.right = None
        self.height = 1 # will be used to help determine rebalancing 

# class AVL_Tree contains information about the structure of AVL_Tree and how to maintain it
# such as the rotation, insertion, and deletion form the tree
class AVL_Tree:
    def __init__(self):
        self.root = None # initially, the tree is empty because we have not put in any new students 

    # determines the tree height of each subtree, helps to determine if the subtree needs to be rotated and in which direction
    def tree_height(self, node):
        if node is None:
            return 0
        left_height = self.tree_height(node.left) # getting the height of the left subtree
        right_height = self.tree_height(node.right) # getting the height of the right subtree
        return max(left_height, right_height) + 1 # return the subtree which has the largest depth (adding 1 since we start our count at 0)
    
    def left_left_rotation(self, node):
        new_parent = node.right # setting the right child as the pivot/new parent
        temp_var = new_parent.left # temparary variable that will be reattached when tree has been rotated
        new_parent.left = node # setting parent node as left child
        node.right = temp_var # since the node is going to be smaller than the temp var, it is going to be placed as right child

        # since we repositioned the parent node and the right child's position, we need to update the height of each
        node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1 
        new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

        # return the new_parent for recalculation to see if the tree is now balanced
        return new_parent
    
    def right_right_rotation(self, node):
        new_parent = node.left # setting the left child as the pivot/new parent
        temp_var = new_parent.right # temparary variable that will be reattached when tree has been rotated
        new_parent.right = node # setting parent node as right child
        node.left = temp_var # since the node is going to be bigger than the temp var, it is going to be placed as left child

        # since we repositioned the parent node and the right child's position, we need to update the height of each
        node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1
        new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

        # return the new_parent for recalculation to see if the tree is now balanced
        return new_parent

    def left_right_rotation(self, node):
        node.left = self.left_left_rotation(node.left)
        return self.right_right_rotation(node)

    def right_left_rotation(self, node):
        node.right = self.right_right_rotation(node.right)
        return self.left_left_rotation(node)
 
    # inserting a new student into the AVL tree
    def insert(self, parent_node, name, major, year, reg_day, priority):
        # set the student to the root node if it is going to be ther first thing in the list 
        if parent_node is None:
            # in here we care using the node class to create the root node
            return Node(name, major, year, reg_day, priority)  

        # We are inserting the following students based on their priority value
        # the new student has a lower priority value than the students already in the tree
        if priority < parent_node.priority:
            parent_node.left = self.insert(parent_node.left, name, major, year, reg_day, priority)
            
        # the new student has a higher priority value than the students already in the tree
        else:
            parent_node.right = self.insert(parent_node.right, name, major, year, reg_day, priority)

        # once we add the new node we need to update the height of our tree that will be used to determine 
        # balance of our new tree
        parent_node.height = max(self.tree_height(parent_node.left), self.tree_height(parent_node.right)) + 1
       
        # if the balance is greater than 1 or smaller than -1 (so 2 or -2) means we are no longer balanced 
        # thus we need to rotate the nodes to rebalance the tree such that it is between -1>= x =<1
        balance = self.tree_height(parent_node.left) - self.tree_height(parent_node.right)
        
        # there is a string of left child that outweighs how many right child there is in the subtree
        if balance > 1:
            if priority < parent_node.left.priority:
                return self.right_right_rotation(parent_node)
            else:
                return self.left_right_rotation(parent_node)
            
        # there is a string of right child that outweighs how many left child there is in the subtree
        if balance < -1:
            if priority > parent_node.right.priority:
                return self.left_left_rotation(parent_node)
            else:
                return self.right_left_rotation(parent_node)

        return parent_node
        
    def print_tree(self, node):
        if node:
            self.print_tree(node.right)
            print(node.name, node.major, node.year, node.reg_day, node.priority)
            self.print_tree(node.left)

class stud_registration:
    def __init__(self):
        self.registraion_list = AVL_Tree()
        self.student_dict = {}  # Dictionary to store student information

    def update_student_dict(self):
        self.student_dict = {}  # Clear the dictionary
        self._update_student_dict(self.registraion_list.root)

    def _update_student_dict(self, node):
        if node:
            self._update_student_dict(node.right)

            # Update the student_dict with the student's information
            self.student_dict[node.name] = {
                'major': node.major,
                'year': node.year,
                'reg_day': node.reg_day,
                'priority': node.priority
            }

            self._update_student_dict(node.left)

    def student_priority(self, major, year, reg_day):
        level = 0 #reset the level for each function call
        if year == 0: #for auditors
            level = level + (.5-(.1*(reg_day))) # level will equal 0.5 for registrations before orientation week, 0.4 for registrations on the first day, etc.
          
        elif year <5: # for undergraduate students
            if major == 'cs' or major == 'math':
                level = level+10 # adds 10 to the level for cs or math majors,
            level = level + year # adds 1,2,3, or 4 to the level based on the year.
            level = level +(.5-(.1*(reg_day))) #+0.5 for students registered before the orientation week, same as for auditors.
            
        else:
            level = 15 #for graduate students, level will automatically be 15.
        return level


    def register_student(self, name, major, year, reg_day):
        if int(reg_day) < 6:
            priority = self.student_priority(major, year, reg_day)
            self.registraion_list.root = self.registraion_list.insert(self.registraion_list.root, name, major, year, reg_day, priority)
            self.update_student_dict()  # Update the student_dict

    def remove_student(self, name):
        if name in self.student_dict:
            del self.student_dict[name]

    def get_student_dict(self):
        return self.student_dict

if __name__ == "__main__":
    reg_stud = stud_registration()

    # Insert students
    reg_stud.register_student('Alice', 'cs', 3, 3)
    reg_stud.register_student('Bob', 'math', 2, 4)
    reg_stud.register_student('Charlie', 'art', 2, 1)
    reg_stud.register_student('David', 'cs', 3, 2)
    reg_stud.register_student('Eve', 'art',  5, 1)
    reg_stud.register_student('Frank', 'cs',  0, 1)

    reg_stud.remove_student('Eve')

    student_dict = reg_stud.get_student_dict()
    for name, student_info in student_dict.items():
        print(f"Name: {name}, Major: {student_info['major']}, Year: {student_info['year']}, Reg Day: {student_info['reg_day']}, Priority: {student_info['priority']}")

##################################################################################################

# class Node deals with the information about the relation and information that each node contains
class Node:
    def __init__(self, name, major, year, reg_day, priority):
        self.name = name # student's name
        self.major = major # major of the student
        self.year = year # the year the student is in
        self.reg_day = reg_day # day of registration
        self.priority = priority # used in comparsion based analysis for developing priority

        # when inputing a node there is no child attached
        self.left = None
        self.right = None
        self.height = 1 # will be used to help determine rebalancing


# class AVL_Tree contains information about the structure of AVL_Tree and how to maintain it
# such as the rotation, insertion, and deletion form the tree
class AVL_Tree:
    def __init__(self):
        self.root = None # initially, the tree is empty because we have not put in any new students
        self.name_to_node = {} # Dictionary to map names to nodes
        # determines the tree height of each subtree, helps to determine if the subtree needs to be rotated and in which direction
    def tree_height(self, node):
        if node is None:
            return 0
        left_height = self.tree_height(node.left) # getting the height of the left subtree
        right_height = self.tree_height(node.right) # getting the height of the right subtree
        return max(left_height, right_height) + 1 # return the subtree which has the largest depth (adding 1 since we start our count at 0)


    def left_left_rotation(self, node):
        new_parent = node.right # setting the right child as the pivot/new parent
        temp_var = new_parent.left # temparary variable that will be reattached when tree has been rotated
        new_parent.left = node # setting parent node as left child
        node.right = temp_var # since the node is going to be smaller than the temp var, it is going to be placed as right child


        # since we repositioned the parent node and the right child's position, we need to update the height of each
        node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1
        new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

        # return the new_parent for recalculation to see if the tree is now balanced
        return new_parent
    
    def right_right_rotation(self, node):
        new_parent = node.left # setting the left child as the pivot/new parent
        temp_var = new_parent.right # temparary variable that will be reattached when tree has been rotated
        new_parent.right = node # setting parent node as right child
        node.left = temp_var # since the node is going to be bigger than the temp var, it is going to be placed as left child

        # since we repositioned the parent node and the right child's position, we need to update the height of each
        node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1
        new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

        # return the new_parent for recalculation to see if the tree is now balanced
        return new_parent


    def left_right_rotation(self, node):
        node.left = self.left_left_rotation(node.left)
        return self.right_right_rotation(node)


    def right_left_rotation(self, node):
        node.right = self.right_right_rotation(node.right)
        return self.left_left_rotation(node)
        # inserting a new student into the AVL tree
    def insert(self, parent_node, name, major, year, reg_day, priority):
        # set the student to the root node if it is going to be ther first thing in the list
        if parent_node is None:
        # in here we care using the node class to create the root node
            new_node = Node(name, major, year, reg_day, priority)
            self.name_to_node[name] = new_node # Add to the dictionary
            return new_node

        # We are inserting the following students based on their priority value
        # the new student has a lower priority value than the students already in the tree
        if priority < parent_node.priority:
            parent_node.left = self.insert(parent_node.left, name, major, year, reg_day, priority)
        # the new student has a higher priority value than the students already in the tree
        else:
            parent_node.right = self.insert(parent_node.right, name, major, year, reg_day, priority)


        # once we add the new node we need to update the height of our tree that will be used to determine
        # balance of our new tree
        parent_node.height = max(self.tree_height(parent_node.left), self.tree_height(parent_node.right)) + 1
        # if the balance is greater than 1 or smaller than -1 (so 2 or -2) means we are no longer balanced
        # thus we need to rotate the nodes to rebalance the tree such that it is between -1>= x =<1
        balance = self.tree_height(parent_node.left) - self.tree_height(parent_node.right)
        # there is a string of left child that outweighs how many right child there is in the subtree
        if balance > 1:
            if priority < parent_node.left.priority:
                return self.right_right_rotation(parent_node)
            else:
                return self.left_right_rotation(parent_node)
        # there is a string of right child that outweighs how many left child there is in the subtree
        if balance < -1:
            if priority > parent_node.right.priority:
                return self.left_left_rotation(parent_node)
            else:
                return self.right_left_rotation(parent_node)


        return parent_node


    def min_value_node(self, node):
        if node is None or node.left is None:
            return node
        return self.min_value_node(node.left)
    
    def delete(self, parent_node, name, priority):
        if parent_node is None:
            return None
        if parent_node.priority > priority:
            parent_node.right = self.delete(parent_node.left, name, priority)
        elif parent_node.priority < priority:
            parent_node.left = self.delete(parent_node.left, name, priority)
        else:
            if parent_node.name != name:


            # when node with matching name is found
                if parent_node.left is None:
                    return parent_node.right
                elif parent_node.right is None:
                    return parent_node.left
                
            # Node with two children, get the in-order successor
            temp = self.min_value_node(parent_node.right)
            parent_node.name = temp.name
            parent_node.major = temp.major
            parent_node.year = temp.year
            parent_node.reg_day = temp.reg_day
            parent_node.priority = temp.priority
            parent_node.right = self.delete(parent_node.right, temp.name, temp.priority)




        parent_node.height = max(self.tree_height(parent_node.left), self.tree_height(parent_node.right)) + 1
        # if the balance is greater than 1 or smaller than -1 (so 2 or -2) means we are no longer balanced
        # thus we need to rotate the nodes to rebalance the tree such that it is between -1>= x =<1
        balance = self.tree_height(parent_node.left) - self.tree_height(parent_node.right)
        # there is a string of left child that outweighs how many right child there is in the subtree
        if balance > 1:
            if priority < parent_node.left.priority:
                return self.right_right_rotation(parent_node)
            else:
                return self.left_right_rotation(parent_node)
        # there is a string of right child that outweighs how many left child there is in the subtree
        if balance < -1:
            if priority > parent_node.right.priority:
                return self.left_left_rotation(parent_node)
            else:
                return self.right_left_rotation(parent_node)


    def delete_by_name(self, name, priority):
        if name in self.name_to_node:
            node = self.name_to_node[name] # Get the node from the dictionary
            self.root = self.delete(self.root, name, node.priority)
            self.name_to_node[name] # Remove from the dictionary

    def get_all_students(self):
        admitted_students = {}
        self.collect_students(self.root, admitted_students)
        return admitted_students


    def collect_students(self, node, admitted_students):
        if node is None:
            return
        self.collect_students(node.left, admitted_students)
        admitted_students[node.name] = (node.major, node.year, node.reg_day, node.priority)
        self.collect_students(node.right, admitted_students)


    def print_name_to_node(self):
        for name, node in self.name_to_node.items():
            print(f"Name: {name}, Priority: {node.priority}")


    def print_tree(self, node):
        if node:
            self.print_tree(node.right)
            self.name_to_node[node.name] = (node.major, node.year, node.reg_day, node.priority)
            self.print_tree(node.left)


class stud_registration:
    def __init__(self):
        self.registraion_list = AVL_Tree()


    def student_priority(self, major, year, reg_day):
        level = 0 #reset the level for each function call
        if year == 0: #for auditors
            level = level + (.5-(.1*(reg_day))) # level will equal 0.5 for registrations before orientation week, 0.4 for registrations on the first day, etc.
          
        elif year <5: # for undergraduate students
            if major == 'cs' or major == 'math':
                level = level+10 # adds 10 to the level for cs or math majors,
            level = level + year # adds 1,2,3, or 4 to the level based on the year.
            level = level +(.5-(.1*(reg_day))) #+0.5 for students registered before the orientation week, same as for auditors.
            
        else:
            level = 15 #for graduate students, level will automatically be 15.
        return level


    def register_student(self, name, major, year, reg_day):
        if int(reg_day) < 6:
            priority = self.student_priority(major, year, reg_day)
            self.registraion_list.root = self.registraion_list.insert(self.registraion_list.root, name, major, year, reg_day, priority)


    def remove_student(self, name, major, year, reg_day):
        priority = self.student_priority(major, year, reg_day)
        self.registraion_list.delete_by_name(name, priority)




if __name__ == "__main__":
    reg_stud = stud_registration()


    # Insert students
    reg_stud.register_student('Alice', 'cs', 3, 3)
    reg_stud.register_student('Bob', 'math', 2, 4)
    reg_stud.register_student('Charlie','art', 2, 1)
    reg_stud.register_student('David', 'cs', 3, 2)
    reg_stud.register_student('Eve', 'art', 5, 1)
    reg_stud.register_student('Frank', 'cs', 0, 1)
    reg_stud.remove_student('Alice', 'cs', 3, 3)


    print("Registration List:")
    all_students = reg_stud.registraion_list.get_all_students()
    print(all_students)


    reg_stud.registraion_list.print_tree(reg_stud.registraion_list.root)

##################################################################################################

# class Node deals with the information about the relation and information that each node contains 
class Node:
    def __init__(self, name, major, year, reg_day, priority):
        self.name = name # student's name
        self.major = major # major of the student
        self.year = year # the year the student is in
        self.reg_day = reg_day # day of registration 
        self.priority = priority # used in comparsion based analysis for developing priority 

        # when inputing a node there is no child attached 
        self.left = None 
        self.right = None
        self.height = 1 # will be used to help determine rebalancing 

# class AVL_Tree contains information about the structure of AVL_Tree and how to maintain it
# such as the rotation, insertion, and deletion form the tree
class AVL_Tree:
    def __init__(self):
        self.root = None # initially, the tree is empty because we have not put in any new students 

    # determines the tree height of each subtree, helps to determine if the subtree needs to be rotated and in which direction
    def tree_height(self, node):
        if node is None:
            return 0
        left_height = self.tree_height(node.left) # getting the height of the left subtree
        right_height = self.tree_height(node.right) # getting the height of the right subtree
        return max(left_height, right_height) + 1 # return the subtree which has the largest depth (adding 1 since we start our count at 0)
    
    def left_left_rotation(self, node):
        new_parent = node.right # setting the right child as the pivot/new parent
        temp_var = new_parent.left # temparary variable that will be reattached when tree has been rotated
        new_parent.left = node # setting parent node as left child
        node.right = temp_var # since the node is going to be smaller than the temp var, it is going to be placed as right child

        # since we repositioned the parent node and the right child's position, we need to update the height of each
        node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1 
        new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

        # return the new_parent for recalculation to see if the tree is now balanced
        return new_parent
    
    def right_right_rotation(self, node):
        new_parent = node.left # setting the left child as the pivot/new parent
        temp_var = new_parent.right # temparary variable that will be reattached when tree has been rotated
        new_parent.right = node # setting parent node as right child
        node.left = temp_var # since the node is going to be bigger than the temp var, it is going to be placed as left child

        # since we repositioned the parent node and the right child's position, we need to update the height of each
        node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1
        new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

        # return the new_parent for recalculation to see if the tree is now balanced
        return new_parent

    def left_right_rotation(self, node):
        node.left = self.left_left_rotation(node.left)
        return self.right_right_rotation(node)

    def right_left_rotation(self, node):
        node.right = self.right_right_rotation(node.right)
        return self.left_left_rotation(node)
 
    # inserting a new student into the AVL tree
    def insert(self, parent_node, name, major, year, reg_day, priority):
        # set the student to the root node if it is going to be ther first thing in the list 
        if parent_node is None:
            # in here we care using the node class to create the root node
            return Node(name, major, year, reg_day, priority)  

        # We are inserting the following students based on their priority value
        # the new student has a lower priority value than the students already in the tree
        if priority < parent_node.priority:
            parent_node.left = self.insert(parent_node.left, name, major, year, reg_day, priority)
            
        # the new student has a higher priority value than the students already in the tree
        else:
            parent_node.right = self.insert(parent_node.right, name, major, year, reg_day, priority)

        # once we add the new node we need to update the height of our tree that will be used to determine 
        # balance of our new tree
        parent_node.height = max(self.tree_height(parent_node.left), self.tree_height(parent_node.right)) + 1
       
        # if the balance is greater than 1 or smaller than -1 (so 2 or -2) means we are no longer balanced 
        # thus we need to rotate the nodes to rebalance the tree such that it is between -1>= x =<1
        balance = self.tree_height(parent_node.left) - self.tree_height(parent_node.right)
        
        # there is a string of left child that outweighs how many right child there is in the subtree
        if balance > 1:
            if priority < parent_node.left.priority:
                return self.right_right_rotation(parent_node)
            else:
                return self.left_right_rotation(parent_node)
            
        # there is a string of right child that outweighs how many left child there is in the subtree
        if balance < -1:
            if priority > parent_node.right.priority:
                return self.left_left_rotation(parent_node)
            else:
                return self.right_left_rotation(parent_node)

        return parent_node
        
    def print_tree(self, node):
        if node:
            self.print_tree(node.right)
            print(node.name, node.major, node.year, node.reg_day, node.priority)
            self.print_tree(node.left)

class stud_registration:
    def __init__(self):
        self.registraion_list = AVL_Tree()


    def student_priority(self, major, year, reg_day):
        level = 0 #reset the level for each function call
        if year == 0: #for auditors
            level = level + (.5-(.1*(reg_day))) # level will equal 0.5 for registrations before orientation week, 0.4 for registrations on the first day, etc.
          
        elif year <5: # for undergraduate students
            if major == 'cs' or major == 'math':
                level = level+10 # adds 10 to the level for cs or math majors,
            level = level + year # adds 1,2,3, or 4 to the level based on the year.
            level = level +(.5-(.1*(reg_day))) #+0.5 for students registered before the orientation week, same as for auditors.
            
        else:
            level = 15 #for graduate students, level will automatically be 15.
        return level


    def register_student(self, name, major, year, reg_day):
        if int(reg_day) < 6:
            priority = self.student_priority(major, year, reg_day)
            self.registraion_list.root = self.registraion_list.insert(self.registraion_list.root, name, major, year, reg_day, priority)

if __name__ == "__main__":
    reg_stud = stud_registration()

    # Insert students
    reg_stud.register_student('Alice', 'cs', 3, 3)
    reg_stud.register_student('Bob', 'math', 2, 4)
    reg_stud.register_student('Charlie', 'art', 2, 1)
    reg_stud.register_student('David', 'cs', 3, 2)
    reg_stud.register_student('Eve', 'art',  5, 1)
    reg_stud.register_student('Frank', 'cs',  0, 1)

    print("Registration List:")
    reg_stud.registraion_list.print_tree(reg_stud.registraion_list.root)


 ##################################################################################################
# class Node deals with the information about the relation and information that each node contains 
class Node:
    def __init__(self, name, major, year, reg_day, priority):
        self.name = name # student's name
        self.major = major # major of the student
        self.year = year # the year the student is in
        self.reg_day = reg_day # day of registration 
        self.priority = priority # used in comparsion based analysis for developing priority 

        # when inputing a node there is no child attached 
        self.left = None 
        self.right = None
        self.height = 1 # will be used to help determine rebalancing 

# class AVL_Tree contains information about the structure of AVL_Tree and how to maintain it
# such as the rotation, insertion, and deletion form the tree
class AVL_Tree:
    def __init__(self):
        self.root = None # initially, the tree is empty because we have not put in any new students 

    # determines the tree height of each subtree, helps to determine if the subtree needs to be rotated and in which direction
    def tree_height(self, node):
        if node is None:
            return 0
        left_height = self.tree_height(node.left) # getting the height of the left subtree
        right_height = self.tree_height(node.right) # getting the height of the right subtree
        return max(left_height, right_height) + 1 # return the subtree which has the largest depth (adding 1 since we start our count at 0)
    
    def left_left_rotation(self, node):
        new_parent = node.right # setting the right child as the pivot/new parent
        temp_var = new_parent.left # temparary variable that will be reattached when tree has been rotated
        new_parent.left = node # setting parent node as left child
        node.right = temp_var # since the node is going to be smaller than the temp var, it is going to be placed as right child

        # since we repositioned the parent node and the right child's position, we need to update the height of each
        node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1 
        new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

        # return the new_parent for recalculation to see if the tree is now balanced
        return new_parent
    
    def right_right_rotation(self, node):
        new_parent = node.left # setting the left child as the pivot/new parent
        temp_var = new_parent.right # temparary variable that will be reattached when tree has been rotated
        new_parent.right = node # setting parent node as right child
        node.left = temp_var # since the node is going to be bigger than the temp var, it is going to be placed as left child

        # since we repositioned the parent node and the right child's position, we need to update the height of each
        node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1
        new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

        # return the new_parent for recalculation to see if the tree is now balanced
        return new_parent

    def left_right_rotation(self, node):
        node.left = self.left_left_rotation(node.left)
        return self.right_right_rotation(node)

    def right_left_rotation(self, node):
        node.right = self.right_right_rotation(node.right)
        return self.left_left_rotation(node)
 
    # inserting a new student into the AVL tree
    def insert(self, parent_node, name, major, year, reg_day, priority):
        # set the student to the root node if it is going to be ther first thing in the list 
        if parent_node is None:
            # in here we care using the node class to create the root node
            return Node(name, major, year, reg_day, priority)  

        # We are inserting the following students based on their priority value
        # the new student has a lower priority value than the students already in the tree
        if priority < parent_node.priority:
            parent_node.left = self.insert(parent_node.left, name, major, year, reg_day, priority)
            
        # the new student has a higher priority value than the students already in the tree
        else:
            parent_node.right = self.insert(parent_node.right, name, major, year, reg_day, priority)

        # once we add the new node we need to update the height of our tree that will be used to determine 
        # balance of our new tree
        parent_node.height = max(self.tree_height(parent_node.left), self.tree_height(parent_node.right)) + 1
       
        # if the balance is greater than 1 or smaller than -1 (so 2 or -2) means we are no longer balanced 
        # thus we need to rotate the nodes to rebalance the tree such that it is between -1>= x =<1
        balance = self.tree_height(parent_node.left) - self.tree_height(parent_node.right)
        
        # there is a string of left child that outweighs how many right child there is in the subtree
        if balance > 1:
            if priority < parent_node.left.priority:
                return self.right_right_rotation(parent_node)
            else:
                return self.left_right_rotation(parent_node)
            
        # there is a string of right child that outweighs how many left child there is in the subtree
        if balance < -1:
            if priority > parent_node.right.priority:
                return self.left_left_rotation(parent_node)
            else:
                return self.right_left_rotation(parent_node)

        return parent_node
        
    def print_tree(self, node):
        if node:
            self.print_tree(node.right)
            print(node.name, node.major, node.year, node.reg_day, node.priority)
            self.print_tree(node.left)

class stud_registration:
    def __init__(self):
        self.grad_list = {}
        self.undgrad_list = AVL_Tree()
        self.auditor_list = AVL_Tree()
        self.waitlist = {}

    def audit_priority(self,reg_day): 
        level = 0 #reset the level for each function call
        level = level + (.5-(.1*(reg_day))) # level will equal 0.5 for registrations before orientation week, 0.4 for registrations on the first day, etc.
        return(level) #returns the updated dictionary
        
    def undgrad_priority(self, major, year, reg_day):     
        level = 0
        if major == 'cs' or major == 'math':
            level = level+10 # adds 10 to the level for cs or math majors,
            
        level = level + year # adds 1,2,3, or 4 to the level based on the year. 
        level = level +(.5-(.1*(reg_day))) #+0.5 for students registered before the orientation week, same as for auditors.

        return(level) #return the updated dictionary

    def register_student(self, name, major, year, reg_day):
        if int(reg_day) < 6:
            if int(year) > 4:
                self.grad_list[name] = [(major, year, reg_day)]
            elif int(year) == 0:
                priority = self.audit_priority(reg_day)
                if self.auditor_list.root is None:
                    self.auditor_list.root = self.auditor_list.insert(self.auditor_list.root, name, major, year, reg_day, priority)
                else:
                    priority = self.undgrad_priority(major, year, reg_day)
                    self.auditor_list.root = self.auditor_list.insert(self.auditor_list.root, name, major, year, reg_day, priority)
            else:
                priority = self.undgrad_priority(major, year, reg_day)
                if self.undgrad_list.root is None:
                    self.undgrad_list.root = self.undgrad_list.insert(self.undgrad_list.root, name, major, year, reg_day, priority)
                else:
                    priority = self.undgrad_priority(major, year, reg_day)
                    self.undgrad_list.root = self.undgrad_list.insert(self.undgrad_list.root, name, major, year, reg_day, priority)
        else:
            self.waitlist = {}

if __name__ == "__main__":
    reg_stud = stud_registration()

    # Insert students
    reg_stud.register_student('Alice', 'cs', 3, 3)
    reg_stud.register_student('Bob', 'math', 2, 4)
    reg_stud.register_student('Charlie', 'art', 2, 1)
    reg_stud.register_student('David', 'cs', 3, 2)
    reg_stud.register_student('Eve', 'art',  5, 1)
    reg_stud.register_student('Frank', 'cs',  0, 1)

    print("Undgrad List:")
    reg_stud.undgrad_list.print_tree(reg_stud.undgrad_list.root)

    print("Auditor List:")
    reg_stud.auditor_list.print_tree(reg_stud.auditor_list.root)

# class Node deals with the information about the relation and information that each node contains 
class Node:
    def __init__(self, name, major, year, reg_day, priority):
        self.name = name # student's name
        self.major = major 
        self.year = year
        self.reg_day = reg_day
        self.priority = priority

        # when inputing a node there is no child attached 
        self.left = None 
        self.right = None
        self.height = 1 # will be used to help determine rebalancing 

# class AVL_Tree contains information about the structure of AVL_Tree and how to maintain it
# such as the rotation, insertion, and deletion form the tree
class AVL_Tree:
    def __init__(self):
        self.root = None

    # determines the tree height of each subtree, helps to determine if the subtree needs to be rotated and in which direction
    def tree_height(self, node):
        if node is None:
            return 0
        left_height = self.tree_height(node.left) # getting the height of the left subtree
        right_height = self.tree_height(node.right) # getting the height of the right subtree
        return max(left_height, right_height) + 1 # return the subtree which has the largest depth (adding 1 since we start our count at 0)
    
    def left_left_rotation(self, node):
        new_parent = node.right # setting the right child as the pivot/new parent
        temp_var = new_parent.left # temparary variable that will be reattached when tree has been rotated
        new_parent.left = node # setting parent node as left child
        node.right = temp_var # since the node is going to be smaller than the temp var, it is going to be placed as right child

        # since we repositioned the parent node and the right child's position, we need to update the height of each
        node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1 
        new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

        # return the new_parent for recalculation to see if the tree is now balanced
        return new_parent
    
    def right_right_rotation(self, node):
        new_parent = node.left # setting the left child as the pivot/new parent
        temp_var = new_parent.right # temparary variable that will be reattached when tree has been rotated
        new_parent.right = node # setting parent node as right child
        node.left = temp_var # since the node is going to be bigger than the temp var, it is going to be placed as left child

        # since we repositioned the parent node and the right child's position, we need to update the height of each
        node.height = max(self.tree_height(node.left), self.tree_height(node.right)) + 1
        new_parent.height = max(self.tree_height(new_parent.left), self.tree_height(new_parent.right)) + 1

        # return the new_parent for recalculation to see if the tree is now balanced
        return new_parent

    def left_right_rotation(self, node):
        node.left = self.left_left_rotation(node.left)
        return self.right_right_rotation(node)

    def right_left_rotation(self, node):
        node.right = self.right_right_rotation(node.right)
        return self.left_left_rotation(node)
 
    def insert(self, parent_node, name, major, year, reg_day, priority):
        if parent_node is None:
            return Node(name, major, year, reg_day, priority)

        if priority < parent_node.priority:
            parent_node.left = self.insert(parent_node.left, name, major, year, reg_day, priority)
        else:
            parent_node.right = self.insert(parent_node.right, name, major, year, reg_day, priority)

        parent_node.height = max(self.tree_height(parent_node.left), self.tree_height(parent_node.right)) + 1
        balance = self.tree_height(parent_node.left) - self.tree_height(parent_node.right)
        if balance > 1:
            if priority < parent_node.left.priority:
                return self.right_right_rotation(parent_node)
            else:
                return self.left_right_rotation(parent_node)

        if balance < -1:
            if priority > parent_node.right.priority:
                return self.left_left_rotation(parent_node)
            else:
                return self.right_left_rotation(parent_node)

        return parent_node

    def search_AVL(self, node, value_check):
        if node is None or value_check == node.name:
            return node
        if value_check < node.name:
            return self.search_AVL(node.left, value_check)
        else:
            return self.search_AVL(node.right, value_check)
        
    def print_tree(self, node):
        if node:
            self.print_tree(node.left)
            print(node.name, node.major, node.year, node.reg_day)
            self.print_tree(node.right)

class stud_registration:
    def __init__(self):
        self.grad_list = {}
        self.undgrad_list = AVL_Tree()
        self.auditor_list = {}
        self.waitlist = {}

    def audit_priority(self,reg_day): 
        level = 0 #reset the level for each function call
        level = level + (.5-(.1*(reg_day))) # level will equal 0.5 for registrations before orientation week, 0.4 for registrations on the first day, etc.
        return(level) #returns the updated dictionary
        
    def undgrad_priority(self, major, year, reg_day):     
        level = 0
        if major == 'cs' or major == 'math':
            level = level+10 # adds 10 to the level for cs or math majors,
            
        level = level + year # adds 1,2,3, or 4 to the level based on the year. 
        level = level +(.5-(.1*(reg_day))) #+0.5 for students registered before the orientation week, same as for auditors.

        return(level) #return the updated dictionary

    def register_student(self, name,year,reg_day,major):
        if int(reg_day) < 6:
            if int(year) > 4:
                self.grad_list[name] = [(major, year, reg_day)]
            elif int(year) == 0:
                priority = self.audit_priority(reg_day)
                self.auditor_list[name] = [(major, year, reg_day)]
            else:
                priority = self.undgrad_priority(major, year, reg_day)

                if self.undgrad_list.root is None:
                    self.undgrad_list.root = self.undgrad_list.insert(self.undgrad_list.root, name, major, year, reg_day, priority)
                else:
                    priority = self.undgrad_priority(major, year, reg_day)
                    self.undgrad_list.root = self.undgrad_list.insert(self.undgrad_list.root, name, major, year, reg_day, priority)
        else:
            self.waitlist = {}

if __name__ == "__main__":
    reg_stud = stud_registration()
    list = None
    reg_stud.register_student('a', 4, 3, 'cs')
    reg_stud.register_student('b', 3, 4, 'math')
    reg_stud.register_student('c', 3, 6, 'cs')
    reg_stud.register_student('d', 4, 2, 'cs')
    reg_stud.register_student('e', 0, 1, 'art')
    reg_stud.register_student('f', 4, 1, 'cs')

    print("Undgrad List:")
    reg_stud.undgrad_list.print_tree(reg_stud.undgrad_list.root)


######################################################################################################

#  classes is an object constructor which allows for new instances of that type to be made
# in BST, the base structure is a node with a possible left and right child

# creating a class for the boject constructor of the base structure
class Node:
    def __init__(self, node):
        self.node = node
        self.left = None # intially, there are no left child for a node since structure has not been made
        self.right = None # intially, there are no right child for a node
        self.height = 1

class AVL_Tree:

    def __init__(self):
        self.root = None

    def left_height(self, node):
        if node != None:
            left_height = node.left.height if root.left else 0 # if root.left!= None (it exists)
            right_height = node.rigt.height if root.right else 0 # if root.right!= None (it exists)
            root.height = max(left_height, right_height)+1 # finds which subtree has the largest height (adding 1 since count starts at 0)


    def left_left_rotation(self, node):
        new_parent = node.right # getting node that will be roated on
        temp_var = new_parent.left # temparary variable that will be reattached when tree has been rotated
        new_parent.left = node # setting parent node as left child
        node.right = temp_var # since the node is goig to be smaller than the temp var, it is going to be placed as right child


    def right_right_rotation(self, node):
        new_parent = node.left 
        temp_var = new_parent.right
        new_parent.right = node 
        node.left = temp_var 

        # if new_parent.right:
    # goes through the BST and finds if a value is within the tree

        # inserting a node into the BST structure
    def insert(self, parent_node, inserting_node):
        # If the tree is empty, return a new node
        if parent_node is None:
            return Node(inserting_node)
    
        # Otherwise, recur down the tree
        
        # checking to see if the node you want to insert is less than or greater than the nodes currently in the structure
        # it will move it to the place within the BST and then do the comparison again if there are more nodes to compare
        if inserting_node < parent_node.node:
            parent_node.left = self.insert(parent_node.left, inserting_node)
        else:
            parent_node.right = self.insert(parent_node.right, inserting_node)
    

        # Return the (unchanged) node pointer
        return parent_node
    
    def search_BST(self, root, value_check):

        # checking to see if the tree doesn't have a root or if the value is the root node
        if root is None or value_check == root.node:
            return root
        
        # iterates through the tree to find the value
        if value_check < root.node:
            return search_BST(root.left,value_check) # if its smaller than the root/parent then look through the left sub-tree
        else:
            return search_BST(root.right,value_check) # if its smaller than the root/parent then look through the right sub-tree
        
        

if __name__== "__main__":
    Tree = AVL_Tree()
    root = None
    root = Tree.insert(root, 5)
    # insert(root, 3)
    # insert(root, 2)
    # insert(root, 4)
    # insert(root, 7)
    # insert(root, 6)
    # insert(root, 8)
    # insert(root, 1)
    
    # test_BST = [5,4,10,7,11, 1]
    # for i, val in enumerate(test_BST, start=1):
    #     result = search_BST(root, val)

    #     if result is not None:
    #         print(f"Value {result.node} found in the BST.")
    #     else:
    #         print("Value not found in the BST.")


#########################################################################
class Node:
    def __init__(self, root):
        self.root = root
        self.left = None # intially, there are no left child for a node since structure has not been made
        self.right = None # intially, there are no right child for a node

def max_depth(node):
    if node is None:
        return 0
    else:
 
        # Compute the depth of each subtree
        left_depth = max_depth(node.left)
        right_depth = max_depth(node.right)
 
        # Use the larger one
        if left_depth > right_depth and (left_depth-right_depth) >1:
            return True
        else:
            return True
 

# inserting a node into the BST structure
def insert(parent_node, inserting_node):
    # If the tree is empty, return a new node
    if parent_node is None:
        return Node(inserting_node)
 
    if parent_node.root < inserting_node:
        parent_node.root, inserting_node = inserting_node, parent_node.root 
    # Otherwise, recur down the tree
    print(max_depth(parent_node))
    # checking to see if the node you want to insert is less than or greater than the nodes currently in the structure
    # it will move it to the place within the BST and then do the comparison again if there are more nodes to compare
    if parent_node.left == None:
        parent_node.left = insert(parent_node.left, inserting_node)

    elif parent_node.right == None:
        parent_node.right = insert(parent_node.right, inserting_node)

    else:
        # Recur down the tree by choosing the subtree with fewer nodes
        if parent_node.left.root > parent_node.right.root:
            parent_node.left = insert(parent_node.left, inserting_node)
        else:
            parent_node.right = insert(parent_node.right, inserting_node)
    # Return the (unchanged) node pointer

    return parent_node

# goes through the BST and finds if a value is within the tree
def search_heap(root, value_check):
    # checking to see if the tree doesn't have a root or if the value is the root node
    if root is None or value_check == root.root:
        return root
    
    # iterates through the tree to find the value
    elif value_check != root.root:
        return search_BST(root.left, value_check) # if its smaller than the root/parent then look through the left sub-tree
    
    elif value_check != root.root:
        return search_BST(root.right,value_check) # if its smaller than the root/parent then look through the right sub-tree
    

def print_max_heap(root):
    if root is not None:
        print("Root:", root.root)
        if root.left is not None:
            print("Left Child:", root.left.root)
        if root.right is not None:
            print("Right Child:", root.right.root, '\n')
        print_max_heap(root.left)
        print_max_heap(root.right)
    
def print_max_heap_visual(root, indent="", is_left=True):
    if root is not None:
        print(indent, end="")
        if is_left:
            print("L---", root.root)
            new_indent = indent + "|   "
        else:
            print("R---", root.root)
            new_indent = indent + "    "
        
        print_max_heap_visual(root.left, new_indent, True)
        print_max_heap_visual(root.right, new_indent, False)

if __name__== "__main__":
    root = None
    root = insert(root, 5)
    insert(root, 3)
    insert(root, 2)
    insert(root, 4)
    insert(root, 7)
    insert(root, 6)
    insert(root, 8)
    insert(root, 1)
        
    # print_max_heap(root)
    print_max_heap_visual(root)

    print("Size of the tree is %d" %(max_depth(root)))






###########################################################################################
# # used in max_heap to iterate through the input which is a vector of tuples
# # this index [1:3] of the tuple is how we determin priority
# def compare_tuple_list (child, largest, ind_tuple):
#     # determines if child has priority over what is held in the largest position which will signal a swap in the max_heap
#     if int(child[ind_tuple]) > int(largest[ind_tuple]):
#         return True
    
#     # determines if the children are less than the parent in priority 
#     elif int(child[ind_tuple]) < int(largest[ind_tuple]):
#         return False
    
#     # goes to the next variable to check for priority if the current check are the same
#     if ind_tuple + 1 < len(child) and ind_tuple + 1 < len(largest):
#         return int(child[ind_tuple + 1]) > int(largest[ind_tuple + 1])
#     return False


# # heapifying the array of tuples 
# def max_heap(reg_list, node_ind, N, ind_tuple):

#     left = 2*node_ind+1 # getting the index of the left child
#     right = 2*node_ind+2 # getting the index of the right child
#     largest = node_ind # we divided the array in half and are iterating backwards to 0

#     # if left child is larger than parent
#     if left < N and compare_tuple_list(reg_list[left], reg_list[largest], ind_tuple): 
#         largest = left
#     else:
#           largest = node_ind

#     # if right child is larger than parent
#     if right < N and compare_tuple_list(reg_list[right], reg_list[largest], ind_tuple): 
#         largest = right

#     # swaping child and parent
#     if largest != node_ind:
#         reg_list[node_ind], reg_list[largest] = reg_list[largest], reg_list[node_ind]
#         max_heap(reg_list, largest, N, ind_tuple)

#     # if there isn't a swap, then enter the max_heap again but look at the next varible in the list of a tuple
#     # to find if a chile has a priority over the parent
#     else:
#         if ind_tuple < 3:
#             ind_tuple += 2
#             max_heap(reg_list, largest, N, ind_tuple)

#     return(reg_list)

# def build_heap(reg_list, ind_tuple):
#     N = len(reg_list)
#     n = (N//2)-1
#     for node_ind in range(n,-1,-1):
#         max_heap(reg_list,node_ind, N, ind_tuple)
#     return reg_list

# # changes the major into numerics based on priority listed 
# def num_major (major):
#     if  major == 'ds':
#         return 2
#     elif major == 'cs' or major == 'math':
#         return 1
#     else:
#         return 0

# # changes time of registration to negative numbers 
# def reg_Date(regDate):
#     regDate = -abs(regDate)
#     return(regDate)


# # user input necessary for inserting into the max_heap
# def insert_heap(reg_list):
#     flag = True
#     while (flag == True):
#         name = input('Insert: Type Last Name: ')
#         year = int(input('What year are you in (if graduate type 5): '))
#         major = int(num_major(input('What is your major(ds, cs, math, or other): ')))
#         regDate = int(input('registration date: '))
#         flag = input('Any more entries?: ')
       
#         reg_list.append(tuple((name, major, year, regDate)))   
        
#         # stop inputting entries 
#         flag = True if flag == 'y' else False
    
#     build_heap(reg_list, 1) 
#     return(reg_list)

# # user input necessary for removing from the max_heap
# def delete_heap(reg_list):
#     if len(reg_list) == 0:
#         return
#     else:
#         flag = True
#         while (flag == True):
#             pop_name = input('Type Last Name: ')
#             # iterating through to see if the person you want to remove is in in the list
#             for i, curr in enumerate(reg_list, start=1):
#                 if i<=len(reg_list):
#                     check_name = reg_list[i-1]
#                     check_name = check_name[0]
                    
#                     if pop_name == check_name:
#                         reg_list.remove(curr)

#             flag = input('Any more entries?: ')
#             # stop inputting entries 

#         flag = True if flag == 'y' else False
#     build_heap(reg_list, 1) 
#     return(reg_list)


# reg_list = [('l', 2, 6, -1),  ('d', 0, 6, -2), ('a', 1, 4, -2), ('j', 1, 2, -1), 
#             ('k', 1, 1, -5), ('m', 0, 5, -2), ('e', 0, 2, -3), ('h', 1, 4, -1)]

# print(build_heap(reg_list, 1))
# # delete_heap(reg_list)


# ##################################################################################################################
# # CODE DUMP


# reg_Dict = {'a': [(2, 3, -1)], 'b': [(1, 4, -1)], 'c': [(2, 5, -2)], 'd': [(0, 1, -3)]} # dictionary {key, values} where the values is a tuple that contains the year, major, and registration date

# def max_heap(reg_Dict, dict_ind, N):

#     left = 2*dict_ind+1 # getting the index of the left child
#     right = 2*dict_ind+2 # getting the index of the right child
#     largest = dict_ind # we divided the array in half and are iterating backwards to 0

#     parent_node = list(reg_Dict.keys())[largest]
#     print('p', reg_Dict[parent_node])
#     if left < N:
#         left_child = list(reg_Dict.keys())[left] 
#         print('l', reg_Dict[left_child])

#     if right < N:
#         right_child = list(reg_Dict.keys())[right] 
#         print('r', reg_Dict[right_child])
    
    
#     # # if left child is larger than parent
#     # if left < N and compare_tuple_list(reg_Dict[left], reg_Dict[largest], ind_tuple): 
#     #     largest = left
#     # else:
#     #       largest = dict_ind

#     # # if right child is larger than parent
#     # if right < N and compare_tuple_list(reg_Dict[right], reg_Dict[largest], ind_tuple): 
#     #     largest = right

#     # # swaping child and parent
#     # if largest != dict_ind:
#     #     reg_Dict[dict_ind], reg_Dict[largest] = reg_Dict[largest], reg_Dict[dict_ind]
#     #     max_heap(reg_Dict, largest, N)

#     # # if there isn't a swap, then enter the max_heap again but look at the next varible in the list of a tuple
#     # # to find if a chile has a priority over the parent
#     # else:
#     #     if ind_tuple < 3:
#     #         ind_tuple += 2
#     #         max_heap(reg_Dict, largest, N)

#     # return(reg_Dict)

# def build_heap(reg_Dict):
#     N = len(reg_Dict)
#     n = (N//2)-1
#     for dict_ind in range(n,-1,-1):
#         max_heap(reg_Dict,dict_ind, N)
#     return reg_Dict

# build_heap(reg_Dict)


# def compare_dict_values(child, largest, indx):
#     for tuple_values in child.values():
#         child_value = tuple_values[0][indx]

#     for tuple_values in largest.values():
#         largest_value = tuple_values[0][indx]

#     if child_value > largest_value:
#         return True
    
#     elif child_value < largest_value:
#         return False
    
#     if child_value == largest_value and indx < 3:
#         indx =+ 1
#         return compare_dict_values(child, largest, indx)
    
#     return False

# largest = {'a': [(2, 3, -1)]}
# child = {'c': [(2, 5, -2)]}
# indx = 0

# compare_dict_values(child, largest, indx)





# class reg_entry(self, name, major, year, reg_Date):
#     self.name = name
#     self.major = major
#     self.year = year
#     self.reg_Date = reg_Date
    
class Node():
     def __init__(self, root):
        self.root = root
        self.left = None
        self.right = None

def size(node):
    if node is None:
        return 0
    else:
        return (size(node.left)+ 1 + size(node.right))
    
def insert(parent_node, inserting_node):
    # If the tree is empty, return a new node
    if parent_node is None:
        return Node(inserting_node)
 
    # Otherwise, recur down the tree
    
    # checking to see if the node you want to insert is less than or greater than the nodes currently in the structure
    # it will move it to the place within the BST and then do the comparison again if there are more nodes to compare
    
    if parent_node.left == None:
        parent_node.left = insert(parent_node.left, inserting_node)
    elif parent_node.left != None and parent_node.right == None:
        parent_node.right = insert(parent_node.right, inserting_node)
    
    # Return the (unchanged) node pointer
    return parent_node

def search_BST(root, value_check):
    # checking to see if the tree doesn't have a root or if the value is the root node
    if root is None or value_check == root.root:
        return root
    
    # iterates through the tree to find the value
    if root.left != None:
        return search_BST(root.left,value_check) # if its smaller than the root/parent then look through the left sub-tree
    if root.right != None:
        return search_BST(root.right,value_check)
    
if __name__== "__main__":
    root = None
    root = insert(root, 3)
    insert(root, 2)
    insert(root, 4)
    insert(root, 7)
    insert(root, 6)
    insert(root, 8)
    insert(root, 1)

    print("Size of the tree is %d" %(size(root)))


    test_BST = [5,3,10,7,11,1]
    for i, val in enumerate(test_BST, start=1):
        result = search_BST(root, val)

        if result is not None:
            print(f"Value {result.root}, {result.left} , {result.right} found in the Heapify.")
        else:
            print("Value not found in the Heapify.")


