#
# Employee attendance system captures all the employee's swipe-in and swipe-out details.
#
# @author Venkataramanan K
#
import logging
from tree_structure.proper_tree import BinaryTree
import re

logger = logging.getLogger(__name__)

class AttendanceSystem():
    employee_tree = None
    output_msgs = None

    def __init__(self, input_file=None, output_file=None):
        self.employee_tree = self.__read_employee_records(input_file)
        self.output_file = output_file
        self.output_msgs  = list()

    def __read_employee_records(self, input_file):
        emp_ids = []
        try:
            arr_lines = self.__read_input_file(input_file)
            emp_ids = [int(line.rstrip('\n')) for line in arr_lines]  

            logger.debug("Emp ids from the file : {0}".format(emp_ids))
            
            return self.__construct_tree(emp_ids)
            
        except ValueError as ve:
            print("Exception: The values must be in numeric only")             
    
    def __read_input_file(self, input_file):
        """
            This function reads the given input file and returns the list of extracted lines
            @return List lines extracted
        """
        try:
            with open(input_file, 'r') as fp:
                lines = fp.readlines()

            return lines
        except IOError as ie:
            logger.debug("Error in read file : {0}".format(input_file))
            print("IO Exception: The given file is either not found or invalid {0}".format(input_file)) 

    def __construct_tree(self, emp_ids):
        """
           This function constructs the tree structure with the given employee ids
           @return Tree constructed tree structure. 
        """
        tree = BinaryTree()

        for emp_id in emp_ids:
            tree.insert(emp_id)
        
        return tree

    def prompt_records(self, prompt_file):

        try:
            # Getting the total number of employees present
            total_employees = self.head_count_records()
            self.output_msgs.append("Total number of employees today is {0}".format(total_employees))

            query_tuple =  [tuple(line.rstrip('\n').split(':'))  for line in self.__read_input_file(prompt_file)]
            
            for i in range(0, len(query_tuple)):
                if query_tuple[i][0] == 'searchID':
                    emp_node = self.employee_tree.search(int(query_tuple[i][1]))
                    if emp_node != None:
                        self.output_msgs.append("Employee ID {0} is present today.".format(emp_node.get_data()))
                    else:
                        self.output_msgs.append("Employee ID {0} is absent today.".format(query_tuple[i][1]))
                elif query_tuple[i][0] == 'howOften':
                    emp_node = self.employee_tree.search(int(query_tuple[i][1]))
                    if emp_node != None:
                        self.output_msgs.append("Employee id {0} swiped {1} times today and is currently in office.".format(emp_node.get_data(), emp_node.get_att_count()))
                    else:
                        self.output_msgs.append("Employee id {0} did not swipe today.".format(query_tuple[i][1]))
                elif query_tuple[i][0] == 'range':
                    # Taking the lower bound and upper bound values from Range
                    lower, upper = int(query_tuple[i][1]), int(query_tuple[i][2])
                    self.output_msgs.append("Range: {0} to {1}".format(lower, upper))
                    self.output_msgs.append("Employee Attendance:")
                    logger.debug("Query range {0} to {1}".format(query_tuple[i][1], query_tuple[i][2]))
                    for i in range(lower, upper+1):
                        # print("Range value ", i)
                        emp_node = self.employee_tree.search(i)
                        if emp_node != None:
                            presence = 'In' if emp_node.get_att_count() % 2 > 0 else 'Out'    
                            self.output_msgs.append("{0}, {1}, {2}".format(emp_node.get_data(), emp_node.get_att_count(), presence))

            # Write the output into the output file
            self.__write_output(self.output_msgs)

            logger.debug("Queries {0}".format(query_tuple))
            logger.debug("Out put message {0}".format(self.output_msgs))
            
        except ValueError as ve:
            raise ValueError
            logger.error("Error query : {0}".format(input_file))

    def head_count_records(self):
        """
            This function counts the number of unique employee IDs stored in the attendance system.
            @return string : Total number of employees today : <Total employees>
        """
        return self.employee_tree.get_size()
        # print("Total number of employees today is {0}".format(total_emps))

    def print_tree(self):
        for item in self.employee_tree:
            print("Emp ID :{0}, Left:{1}, Right:{2},  Attendance:{3} ".format(item.get_data(), item.get_left(), item.get_right(), item.get_att_count()))

    def __write_output(self, message_list):
        """
            This method writes the given message list into a output file
            @param mesage_list list object
        """
        lines = map(lambda l: l + '\n', message_list)
        with open(self.output_file, 'w+') as ofp:
            ofp.writelines(lines)
            ofp.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    input_file = 'data/input/inputPS1.txt'
    prompt_file = 'data/input/promptsPS1.txt'
    output_file = 'data/outputPS1.txt'

    eas = AttendanceSystem(input_file, output_file)
    # eas.print_tree()
    eas.prompt_records(prompt_file)