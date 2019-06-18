import logging

logger = logging.getLogger(__name__)

class BinaryTree():

    class EmpNode():
        def __init__(self, emp_id):
            self.emp_id = emp_id
            self.att_count = 1
            self.left = None
            self.right = None
        
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

        def inc_count(self):
            self.att_count += 1
        
        def dec_count(self):
            self.att_count -= 1

        def __iter__(self):
            if self.left != None:
                for elem in self.left:
                    yield elem

            yield self

            if self.right != None:
                for elem in self.right:
                    yield elem
    
    # Constructor of BinaryTree
    def __init__(self, root=None):
        self.root = root
        self.size = 0

    def insert(self, data):
        # logger.debug("Data value "+ str(data))
        self.root = self.__insert(data, self.root)
    
    def __insert(self, data, root=None ):
        if root == None:
            # logger.debug("Creating node {0}".format(data))
            self.size += 1 # Increment the tree height to 1 
            return BinaryTree.EmpNode(data)
        
        if data < self.root.get_data():
            node = self.search(data)
            if node != None:
                node.inc_count()
            else:
                # logger.debug("Adding left node {0}".format(data))
                root.set_left(self.__insert(data, root.get_left()))

        elif data > self.root.get_data():
            node = self.search(data)
            if node != None:
                node.inc_count()
            else:
                # logger.debug("Adding right node {0}".format(data))
                root.set_right(self.__insert(data, root.get_right()))
        
        return root

    def get_size(self):
        """
            Size gives the total number of nodes in the tree
            @return int size
        """
        return self.size

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

    def __str_(self):
        return "Binary Tree("+ repr(self.root) +")" 
    
    def __iter__(self):
        if self.root != None:
            return iter(self.root)
        else:
            return iter([])