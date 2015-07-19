""" Testing the Tree class that represents file directory structure"""
import unittest
import os

from tree import Tree, Node

class TestTreeMethods(unittest.TestCase):
    
    def setUp(self):
        self.n1 = Node(title='node1', id='1', parent_id='root')
        self.n2 = Node(title='node2', id='2', parent_id='1')
        self.n3 = Node(title='node3', id='3', parent_id='1')
        self.n4 = Node(title='node4', id='4', parent_id='2')
        self.n5 = Node(title='node5', id='5', parent_id='4') 
        
        # set up tree with multiple nodes
        self.t1 = Tree()
        self.t1.add(self.n1) # node1 has many children
        self.t1.add(self.n2)
        self.t1.add(self.n3)
        self.t1.add(self.n4)
        self.t1.add(self.n5)
        print("Tree before the test:")
        print(self.t1)
        
        # set up tree with only one node besides root
        self.n6 = Node('node6', '6', parent_id='root')
        self.one_node_tree = Tree()
        self.one_node_tree.add(self.n6)

    def tearDown(self):
        self.n1 = None
        self.n2 = None
        self.n3 = None
        self.n4 = None
        self.n5 = None
        self.n6 = None
        self.t1 = None
        self.t2 = None

    def test_get_root(self):
        self.assertEqual(self.t1.get_root().get_id(), 'root')

    def test_init_node_not_have_id_root(self):
        """ test init using a node who's id is not 'root'"""
        n = Node(title='foo', id=0)
        t = Tree(n)
        self.assertEqual(t.get_root().get_id(), 'root')

    def test_init_node_has_id_of_root(self):
        n = Node(title='foo', id='root')
        t = Tree(n)
        self.assertEqual(t.get_root().get_id(), 'root')
    
    def test_string_empty_tree(self):
        t2 = Tree(None)
        self.assertEqual(t2.__str__(), '|---Google_Drive\n')

    def test_string_non_empty_tree(self):
        print("You can't really test this...automatically")
        print(self.t1)

    def test_search_for_root(self):
        result = self.t1.search('root')
        self.assertTrue(result.get_id() == 'root')

    def test_search_for_first_node_added(self):
        result = self.t1.search('1')
        self.assertTrue(result.get_id() == '1')

    def test_search_for_nonexisting_node_in_one_node_tree(self):
        result = self.one_node_tree.search(self.n2.get_id())
        self.assertTrue(result == None)
    
    def test_new_tree_add_2_nodes_and_print_it(self):
        t = Tree()
        n = Node(title='test', id='1', parent_id='root')
        t.add(n)
        n = Node(title='test2', id='2', parent_id='1')
        t.add(n)
        print(t)

    def test_new_tree_add_2_nodes_and_search_it(self):
        t = Tree()
        n = Node(title='test', id='1', parent_id='root')
        t.add(n)
        n = Node(title='test2', id='2', parent_id='1')
        t.add(n)
        print(t)
        result = t.search('2')
        self.assertEqual(result.get_id(), '2')

# From here down, tests are failing
    def test_search_for_nested_leaf_node(self):
        result = self.t1.search(self.n5.get_id())
        self.assertTrue('5' == result.get_id())

    def test_search_for_node1(self):
        result = self.t1.search(self.n1.get_id())
        self.assertTrue(result.get_id(), '1')

    def test_search_for_node2(self):
        result = self.t1.search(self.n2.get_id())
        self.assertTrue(result.get_id(), '2')

    def test_search_for_node3(self):
        result = self.t1.search(self.n3.get_id())
        self.assertTrue(result.get_id(), '3')

    def test_search_for_node4(self):
        result = self.t1.search(self.n4.get_id())
        self.assertTrue(result.get_id(), '4')

    def test_search_for_node5(self):
        result = self.t1.search(self.n5.get_id())
        self.assertTrue(result.get_id(), '5')

    def test_search_empty_tree(self):
        root = None
        empty_tree = Tree(root)
        result = empty_tree.search(self.n1.get_id())
        self.assertEqual(result, None)

    def test_check_that_node_was_added(self):
        n = Node('test_node', id='7', parent_id='4')
        was_added = self.t1.add(n)
        print(self.t1)
        self.assertEqual(was_added, 1)

    def test_add_node_whose_parent_is_in_tree(self):
        """ test adding node whose parent is node4 """
        n = Node('test_node2', id='8', parent_id='4')
        was_added = self.t1.add(n) # should be 1
        print(self.t1)
        self.assertEqual(was_added, 1)

    def test_add_node_whose_parent_is_not_in_tree(self):
        n = Node('test_node3', id='9', parent_id='0')
        was_added = self.t1.add(n) # should be -1
        self.assertEqual(was_added, -1)

    def test_add_node_whose_parent_is_none(self):
        n = Node('test_node', id='8')
        was_added = self.t1.add(n) # should be 0
        self.assertEqual(was_added, 0)

 
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTreeMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)

