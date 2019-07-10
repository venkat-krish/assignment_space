
import logging
import os
from tree_datastructure import BinaryTree

# Logger is an instance of logging 
logger = logging.getLogger(__name__)

"""
    Employee Attendance class contains the following member variable and instance methods 
    employee_tree: BinaryTree - Datastructure of employees information
    RESULT_MSGS: List() - List of resultant messages
"""
class EmployeeAttendance():

    RESULT_MSGS = {
        'HeadCount':'Total number of employees today is: {0}',
        'EmployeePresent': 'Employee ID {0} is present today',
        'EmployeeAbsent': 'Employee ID {0} is absent today',
        'SwipeCountYes': 'Employee id {0} swiped {1} times today and is currently in office',
        'SwipeCountNo': 'Employee id {0} did not swipe today',
        'FrequentCount': 'Employee id {0} swiped the most number of times today with a count of {1}',
        'Range': 'Range: {0} to {1}\n',
    }

    """ Constructor of EmployeeAttendance class """
    def __init__(self, input_file=None, output_file=None):
        self.output_file = output_file

        if input_file != None:
            file_data = self.__read_input_file(input_file)

            # Strips the trailing newline from the file
            data_set = [int(line.rstrip('\n')) for line in file_data]  

            # Initialization of BinaryTree data structure
            self.employee_tree = BinaryTree()
            # Constructs the employee tree with the given input data
            self._readEmployeeRec(self.employee_tree, data_set, 0)
        else:
            logger.error("Error: Input file is required to construct the basic tree structure.")

    """
        This function reads the given input file and returns the list of extracted lines
        @return List lines extracted
    """
    def __read_input_file(self, input_file):
        
        try:
            # Openning the file as 'read only' mode and extracts the file lines
            with open(input_file, 'r') as fp:
                lines = fp.readlines()
            return lines
        except IOError as ie:
            logger.error("IO Exception: The given file is either not found or invalid {0}".format(input_file)) 


    """ 
        _readEmployeeRec() : Reads the data from the given input file and constructs the tree
        @return BinaryTree object
    """
    def _readEmployeeRec(self, emp_tree, emp_list, idx):
        if idx == len(emp_list):
            return emp_tree
        # Creates a node and inserts into a binary tree
        emp_tree.insert(emp_list[idx])
        idx += 1
        # Recursive call to insert the elements into the binary tree
        self._readEmployeeRec(emp_tree, emp_list, idx)


    """ 
        _getHeadCountRec() : Counts the number of unique records stored in the tree and 
                            prints the employee headcount for the day. 
    """
    def _getHeadCountRec(self):
        # Get the unique employee records count from the Binary Tree
        head_count = self.employee_tree.get_size()

        out_msg = self.RESULT_MSGS['HeadCount'].format(head_count)

        self.__output_result(out_msg)

    """
        _searchIDRec() : Searches the given employee id in the stored binary tree and returns the node
        @param: eID employee id
    """
    def _searchIDRec(self, eId):
        # Search the given employee id in the binary tree
        emp_node = self.employee_tree.search(eId)

        if emp_node != None:
            out_msg = self.RESULT_MSGS['EmployeePresent'].format(emp_node.get_data())
        else:
            out_msg = self.RESULT_MSGS['EmployeeAbsent'].format(eId)

        # Write into a output file
        self.__output_result(out_msg)

    """
        _howOftenRec() : Finds the employee id that how often he has swiped the system.
        @param: eID employee id
    """
    def _howOftenRec(self, eId):
         # Search the given employee id in the binary tree
        emp_node = self.employee_tree.search(eId)

        if emp_node != None:
            out_msg = self.RESULT_MSGS['SwipeCountYes'].format(emp_node.get_data(), emp_node.get_att_count())
        else:
            out_msg = self.RESULT_MSGS['SwipeCountNo'].format(eId)

        # Write into a output file
        self.__output_result(out_msg)



    """
        _frequentVisitorRec() : Finds the employee id that how often he has swiped the system.
        @param: eID employee id
    """
    def _frequentVisitorRec(self):
        try:
            employees = [node for node in self.employee_tree]

            employees.sort(key=lambda x: x.get_att_count(), reverse=True)
            
            out_msg = self.RESULT_MSGS['FrequentCount'].format(employees[0].get_data(), employees[0].get_att_count())

            # Write into a output file
            self.__output_result(out_msg)
        except ValueError as ve:
            logger.error("Error in method freqentVisitorRec; {0}".format(ve))


    """
        _printRangePresent() : Finds the employee id that how often he has swiped the system.
        @param: startId employee id
        @param: endId employee id
    """   
    def _printRangePresent(self, startId, endId):
        try:
            out_msg = self.RESULT_MSGS['Range'].format(startId, endId)

            for eId in range(startId, endId):
                emp_node = self.employee_tree.search(eId)

                if emp_node != None:
                    presence = 'In' if emp_node.get_att_count() % 2 > 0 else 'Out'    

                    out_msg += "{0}, {1}, {2}\n".format(emp_node.get_data(), emp_node.get_att_count(), presence)

            # Write into a output file
            self.__output_result(out_msg)
        except ValueError as ve:
            logger.error("Error in method freqentVisitorRec; {0}".format(ve))

    """
        output_result() : It writes the output result into the output file.
        @param : Result message
    """
    def __output_result(self, result_msg):
        try:
            with open(self.output_file, 'a+') as ofp:
                ofp.write(result_msg+"\n") # Write the given result message into an output file.

        except IOError as ie:
            logger.error("Error in writing the result into output file")

    """
        attendance_operations() : It's a controller function that invokes the required methods in a sequential order.
    """
    def attendance_operations(self, prompt_file):
        try:
            # Erase the content of the output file
            # Cleanse the file data
            self.__clear_output()

            query_tuple =  [tuple(line.rstrip('\n').split(':'))  for line in self.__read_input_file(prompt_file)]

            # 1. Method to get the head count for the records from the tree
            self._getHeadCountRec()
            
            startId, endId = None, None

            # 2. Iterate through the prompt queries from the promptPS1.txt file
            for i in range(0, len(query_tuple)):
                if query_tuple[i][0] == 'searchID':
                    # 3. Iterate through the prompt queries from the promptPS1.txt file
                    self._searchIDRec(int(query_tuple[i][1])) # Invoking search employee id method
                elif query_tuple[i][0] == 'howOften':
                    # 4. Iterate through the prompt queries from the promptPS1.txt file
                    self._howOftenRec(int(query_tuple[i][1])) # Invoking how often employee has swiped
                elif query_tuple[i][0] == 'range':
                    # Taking the startID and endID value from Range
                    startId, endId = int(query_tuple[i][1]), int(query_tuple[i][2])
                
            # 5. Find frequently swiped employee
            self._frequentVisitorRec()
            # 6. Print range of employees attendance
            self._printRangePresent(startId, endId)

        except ValueError as ve:
            logger.error("Error in value given in the prompt file: {0}".format(ve))
        except IOError as ie:
            logger.error("Error in prompt file: {0}".format(prompt_file))

    """ 
        print_tree() : prints the data elements of the binary tree
    """
    def print_tree(self):
        for item in self.employee_tree:
            print("Emp ID :{0}, Left:{1}, Right:{2},  Attendance:{3} ".format(item.get_data(), item.get_left(), item.get_right(), item.get_att_count()))

    """
        clear_output(): Erase the content of the text file
    """
    def __clear_output(self):
        if os.path.exists(self.output_file) & os.path.isfile(self.output_file):
            with open(self.output_file, 'r+') as ofp:
                ofp.truncate(0)
                ofp.close()


if __name__ == '__main__':
    # Setting the logging level as INFO
    logging.basicConfig(level=logging.DEBUG)
    # Declarations of input, prompt and output files
    input_file = 'data/input/inputPS1.txt'
    prompt_file = 'data/input/promptsPS1.txt'
    output_file = 'data/outputPS1.txt'

    # Instantiation of EmployeeAttendance class object
    eas = EmployeeAttendance(input_file, output_file)
    # Invocation of attendance operations with query input file.
    eas.attendance_operations(prompt_file)