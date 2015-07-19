""" Testing the gdrivefunctions script that handles talking to the API """
import unittest
import os

from tree import Tree, Node
import gdrivefunctions as gdrive

class TestGdrivefunctions(unittest.TestCase):
    
    def setUp(self):
        self.root_file_id = u'19GSi5-kmCvJ9ldwBUcqe8vhzSF8fvSgOmch-3MuOYKw'
        self.root_file_title = u'perl script'
        self.nested_file_id = "0ByKN-hr2wl1PeG5LTTZQb2NDaWc"
        self.nested_file_title = "Project 5.iml"
        self.service = gdrive.create_service()

    def tearDown(self):
        self.root_file_id = None
        self.root_file_title = None
        self.nested_file_id = None
        self.nested_file_title = None
        self.service = None

    def test_get_file_metadata_on_root_file(self):
        """ test getting data for a file that belongs directly in root folder"""
        data = gdrive.get_file_metadata(self.service, self.root_file_id)
        parent_is_root = data['parents'][0]['isRoot']
        self.assertTrue(parent_is_root)        

    def test_get_file_metadata_on_nested_file(self):
        """ test a file that is further nested, make sure it's parent is not root"""
        data = gdrive.get_file_metadata(self.service, self.nested_file_id)
        parent_is_root = data['parents'][0]['isRoot']
        self.assertFalse(parent_is_root)
        
    def test_get_children_of_root_folder_only_type(self):
        """ tests just getting first page results of children of root 
            Google Drive folder and making sure it's a dictionary type object"""
        children = gdrive.get_children(self.service, "root")
        self.assertEqual(type([]), type(children)) 

    def test_root_file_title_is_correct(self):
        """ make sure I got the root file id and title correct """
        data = gdrive.get_file_metadata(self.service, self.root_file_id)
        self.assertEqual(data['title'], self.root_file_title)

    def test_nested_file_title_is_correct(self):
        """ make sure I got the nsted file id and title correct """
        data = gdrive.get_file_metadata(self.service, self.nested_file_id)
        self.assertEqual(data['title'], self.nested_file_title)
        

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGdrivefunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)

