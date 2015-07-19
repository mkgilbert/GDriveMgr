""" tests Node class """

from __future__ import absolute_import

import unittest
from sets import Set

from tree import Node, Tree

class TestNodeMethods(unittest.TestCase):
    
    def setUp(self):
        # create test objects
        self.n = Node('node1')
        self.n2 = Node('node2', '2')
        self.n3 = Node('node3', '3')
        self.n4 = Node('node4', '4')
        self.n5 = Node('node5', '5')
        self.n6 = Node('node6', '6')
        self.n7 = Node('node7', '7')

    def tearDown(self):
        # set objects to none or delete stuff
        self.n = None
        self.n2 = None

    def test_get_id_where_no_id(self):
        self.assertEqual(self.n.get_id(), None)
        
    def test_get_id_and_title_n_n2(self):
        self.assertEqual(self.n.get_title(), 'node1')
        self.assertEqual(self.n2.get_title(), 'node2')
        self.assertEqual(self.n2.get_id(), '2')
    
    def test_string_repr(self):
        self.assertEqual(self.n.__str__(), 'node1')
        self.assertEqual(self.n2.__str__(), 'node2')

    def test_adding_2_children(self):
        self.n.add_child(self.n2)
        self.n.add_child(self.n3)
        children = Set()
        children.add(self.n2)
        children.add(self.n3)
        self.assertEqual(self.n.get_children(), children)

    def test_parent_id(self):
        n = Node(id='6', parent_id='1')
        self.assertEqual(n.get_parent_id(), '1')

    def test_set_and_get_parent_id(self):
        n = Node(id='1')
        n.set_parent_id(0)
        id = n.get_parent_id()
        self.assertEqual(0, id)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNodeMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
