#!/usr/bin/python
""" A Tree where each node can have multiple children """
from __future__ import absolute_import

from sets import Set


class Node:

    def __init__(self, title="(no title)", 
                       id=None, 
                       parent_id=None):
        """
        :param: nested_level = helper for how to print the string rep-
                resentation of the node and it's children
        """
        self._id = id
        self._title = title
        self._children = Set()
        self._parent_id = parent_id

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_parent_id(self):
        return self._parent_id

    def set_parent_id(self, id):
        self._parent_id = id

    def get_title(self):
        return self._title

    def get_children(self):
        return self._children

    def add_child(self, node):
        self._children.add(node)

    def print_all_descendants(self):
        """
        String representation of the the node and it's children in a tree
        like format. Instead of putting the majority of the logic in the
        Tree class, I put it here due to the nature of how file structures
        work.
        I did 2 versions: One that prints directly to stdout and another that
        returns a string representing the whole structure. I imagine the 
        print version uses less memory, but I figured it would be better
        to be able to represent the whole tree using a string
        """
        #self._print_all_descendants_rec(self, 0) # stdout version  
        string = "|---" + str(self) + "\n"
        return self._return_string_all_descendants_rec(self, string, 0)

    def _print_all_descendants_rec(self, node, level):
        """ helper function to recursively print all node's descendants"""
        if level == 0:
            print("|---" + str(node))
        
        if node.get_children():
            level += 1
            for child in node.get_children():
                string = "|   "*level
                print(string + "|---" + str(child))
                self._print_all_descendants_rec(child, level)
            return
        else:
            if level == 0:
                string = ""
            else:
                string = "|" + ("   "*level)
            return 

    def _return_string_all_descendants_rec(self, node, string, level):
        """ 
        helper function returns a string of all descendants
        :param: node = current node we're getting descendants of
        :param: string = the current state of the return string
        :param: level = the level of the tree; helps with figuring out how
        far over to push the current line
        :return: string representing current node and all its descendants
        """
        if len(node.get_children()) == 0:
            return string
        else:
            level += 1
            for child in node.get_children():
                string += "|   "*level
                string += "|---" + str(child) + "\n"
                string = self._return_string_all_descendants_rec(child, string, level)
            return string

    def __str__(self):
        return self.get_title()


class Tree:
    
    def __init__(self, node=None):
        # make sure node's id is 'root' cuz this is how we can search API
        if node is None:
            node = Node(title='Google_Drive', id='root')
        elif node.get_id() != 'root':
            node.set_id('root')
            print('setting root node id to "root"')
        else:
            pass
        self._root = node

    def get_root(self):
        return self._root

    def set_root(self, node):
        #TODO: if there are children, move them to the new root
        try:
            if node.get_id() != 'root':
                node.set_id('root')
                print("setting root node id to 'root'")
            self._root = node
            return self._root
        except AttributeError: # node was None
            print("root was none! Can't set root to none type object")
            return None
    
    def add(self, node):
        """ 
        searches the tree for a new node's parent which is found 
        outside of this class using a Google Drive API call

        Idea for algorithm:
        1. search for existing parent node with id node.get_parent_id()
            if node.get_parent_id() is None, shouldn't even search cuz
                its likely that it's the Google drive root
                return 0
            if parent node exists, add node as child to parent node
                and return 1
            else, the parent doesn't yet exist,
                return -1
            (this is because we will have to query the Google Drive API
             for the parent node and try to do the add again)
            note: don't know if this is a good solution, but going to try
            it
        """
        parent_id = node.get_parent_id()
        
        if parent_id is None:
            return 0

        # Added for testing...don't know if this method works!
        if parent_id == 'root':
            self._root.add_child(node)
            return 1

        # get parent node if it exists
        parent_node = self.search(parent_id)

        if parent_node:
            parent_node.add_child(node)
            return 1
        else:
            # parent node doesn't exist yet
            return -1  

    def remove(self, node):
        pass

    def search(self, id):
        return self._search_rec(id, self.get_root())

    def _search_rec(self, id, root):
        if id == root.get_id():
            return root
        else:
            children = root.get_children()
            if children is None:
                return None
            else:
                for child in children:
                    # node is what we're looking for, child is new root 
                    result = self._search_rec(id, child)
                    if result is not None:
                        return result

    def __str__(self):
        root = self.get_root()
        if root == None:
            return ""
        else:
            return root.print_all_descendants() 


if __name__ == '__main__':
    
    r = Node(id=0, title='Groot')
    
    n = Node(id=1, title='first', parent_id='root')
    n2 = Node(id=2, title='second', parent_id=1)
    n3 = Node(id=3, title='third', parent_id=1)
    n4 = Node(id=4, title='fourth', parent_id=2)
    n5 = Node(id=5, title='fifth', parent_id=3)
    n6 = Node(id=6, title='sixth', parent_id=3)
    n7 = Node(id=7, title='seventh', parent_id=1)
    """
    # this helped me test that searching was working 
    tree = Tree(r)
    r.print_all_descendants()
    r.add_child(n)
    n.add_child(n2)
    n.add_child(n3)
    n2.add_child(n4)
    n3.add_child(n5)
    n3.add_child(n6)
    n6.add_child(n7)
    print(r.print_all_descendants())
    print(tree.search(7))
    print(tree.search(4))
    print(tree.search(3))
    print(tree.search(2))
    print(tree.search(1))
    print(tree.search('root'))
    
    # once I got searching working, I commented out the above test
    # and used the tree add method instead
    t = Tree()
    t.add(n)
    t.add(n2)
    t.add(n3)
    t.add(n4)
    t.add(n5)
    t.add(n6)
    t.add(n7)
    print(t)
    """
