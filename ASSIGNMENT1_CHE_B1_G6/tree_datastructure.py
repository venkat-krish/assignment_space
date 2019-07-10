""" 
    BinaryTree class has a inner class EmpNode to represent the employee information and 
    the behaviors to construct and search tree with the given input.

    class EmpNode: 
        emp_id - Employee Id 
        left - Type of EmpNode which gets constructed as left sub-tree
        right - Type of EmpNode, which will hold the right sub-tree
    
    insert(n) - Inserts the data element into the tree structure
    search(n) - Does the search of the node in the tree structure    
"""
class BinaryTree():

    """ EmpNode is a node object which stores the data element, left and right node connected with it."""
    class EmpNode():

        def __init__(self, emp_id):
            self.emp_id = emp_id # Employee id attribute
            self.att_count = 1 # Attendance is equal to swipe count
            self.left = None
            self.right = None

        """ ** Getters and setters of the class attributes ** """
        def get_data(self):
            return self.emp_id

        def get_att_count(self):
            return self.att_count

        def get_left(self):
            return self.left

        def get_right(self):
            return self.right

        def set_left(self, node):
            self.left = node

        def set_right(self, node):
            self.right = node

        def has_children(self):
            return (self.left and self.right)

        def inc_count(self):
            self.att_count += 1

        def dec_count(self):
            self.att_count -= 1

        """ Default method to produce the iterator of the object """
        def __iter__(self):
            if self.left != None:
                for elem in self.left:
                    yield elem

            yield self

            if self.right != None:
                for elem in self.right:
                    yield elem

        """ Object string representation """
        def __str__(self):
            return "Emp Node("+ repr(self.emp_id) +")"

    # Constructor of BinaryTree
    def __init__(self, root=None):
        self.root = root
        self.size = 0
    """ 
        insert() - Inserts the given data into a tree structure
        @param data - Employee id data 
        Running time: Worst case runtime of inner method is O(n) 
                      Hence running time of this method is O(n) 
    """
    def insert(self, data):
        self.root = self.__insert_node(data, self.root)

    """ 
        __insert_node() - It's a private method, takes emp id and root node as parameters
        @param data : Emp id
        @param root : EmpNode - Current root of the tree
        Running time: - Depends on tree height O(h)
                      - Worst case if the tree is skewed Tree then its O(n)             
    """

    def __insert_node(self, data, root=None):
        if root == None:
            self.size += 1  # Increment the tree size by 1
            return BinaryTree.EmpNode(data)

        if data == root.get_data():  # If data is equal to the node data then increment count and return the root node
            root.inc_count() # Increment the attedance count
            return root

        elif data < root.get_data(): # if the given data is lesser then insert a node at left side
            root.set_left(self.__insert_node(data, root.get_left()))

        else:
            root.set_right(self.__insert_node(data, root.get_right()))

        return root

    """ 
        __insert_node() - It's a private method, takes emp id and root node as parameters
        @param data : Emp id
        @param root : EmpNode - Current root of the tree
        Running time: - Depends on tree height O(h)
                      - Worst case if the tree is skewed then its O(n)
    """
    def search(self, data):
        current = self.root
        while(current != None):
            if current.get_data() > data:
                current = current.get_left()
            elif current.get_data() < data:
                current = current.get_right()
            else:
                return current
        return current

    """
    Find max visitor based on the visit count
    Running time: Internal method has O(n) running time, hence this method is of O(n)
    """

    def max_visitor(self):
        return self.__max_visitor_node(self.root)

    """
    Find max visitor based on the visit count - internal recursion method
    Max of each subtree (child) will be computed, and then over all max will be found   
    Running time: Each node will be visited once, hence running time is O(n)
    """
    def __max_visitor_node(self, root:EmpNode):
        if root.get_left() is None and root.get_right() is None:   # leaf node - hence max node is same as current node
            return root
        if root.get_left() is None:                                # Non Leaf - with one child - right
            return self.max_compare(root,self.__max_visitor_node(root.get_right()))
        elif root.get_right() is None:                             # Non Leaf - with one child - left
            return self.max_compare(root,self.__max_visitor_node(root.get_left()))
        else:                                                      # Non Leaf - with 2 child
            max_child=self.max_compare(self.__max_visitor_node(root.get_left()),self.__max_visitor_node(root.get_right()))
            return self.max_compare(root,max_child)

    """
    Compare two nodes based on visit count
    Running Time: O(1)
    """
    def max_compare(self, node1:EmpNode, node2:EmpNode):
        if node1.get_att_count() >= node2.get_att_count():
            return node1
        else:
            return node2


    def get_size(self):
        """
            Size gives the total number of nodes in the tree
            @return int size
            Running time: - O(1)
        """
        return self.size

    def __str_(self):
        return "Binary Tree("+ repr(self.root) +")"

    def __iter__(self):
        if self.root != None:
            return iter(self.root)
        else:
            return iter([])