#!/usr/bin/python

from __future__ import absolute_import

import os

import gdrivefunctions as gdrive
from tree import Node, Tree


class GDriveMgrHelper:
    """
    Takes care of actually building a local structure that matches Google
    Drive's online and downloading all the files and folders into their
    correct places in the hierarchy.
    It uses gdrivefunctions.py to handle the gdrive API calls and auth
    """

    def __init__(self, root_dir):
        # make root_dir a node to build tree off of
        # initialize directory Tree structure
        self.dir_tree = Tree()
        # this will be initialized in main where we get credentials and stuff
        self._service = None
        # where we will store all dl'd files
        self.root_dir = root_dir
    
    def set_service(self, service):
        self._service = service

    def get_service(self):
        return self._service

    def _get_files_in_folder(self, folder_id):
        """ Creates local gdrive directory tree using Tree class """
        # need to iterate through all files in GDrive        
        # just grab the root for now and see what happens
        children_ids = gdrive.get_children(self.get_service(), folder_id)
        total = 0
        files_list = []
        for child_id in children_ids:
            metadata = gdrive.get_file_metadata(self.get_service(), child_id)
            if metadata['labels']['trashed']:
                continue # the file was marked as trash, don't download

            # add file's info as tuple to the returned list
            title = metadata['title']
            mime = metadata['mimeType']
            if len(metadata['parents']) != 0:
                # parent id is in a dict inside a list
                parents = metadata['parents'][0]
                if parents['isRoot']:
                    parent_id = 'root'
                else:
                    parent_id = parents['id']
            else:
                # some files have an empty parents list
                parent_id = None

            files_list.append((child_id, mime, title, parent_id))
            
            # logging to stdout
            total += 1
            print("Retrieved file " + str(total) + title + " (" + mime + ")")
        
        return files_list
        
    def create_tree(self, folder_id):
        if folder_id is None:
            return -1
        files_list = self._get_files_in_folder(folder_id) # tuple
        
        for f in files_list:
            # add the file to the folder with id 'folder_id'
            new_node = Node(id=f[0], title=f[2], parent_id=f[3])
            if folder_id == 'root':
                self.dir_tree.add(new_node)
            if f[1] == 'application/vnd.google-apps.folder':
                continue
            else:
                # add the file to the node
                pass

    def create_files(self):
        """ Builds directory file structure based on the dir_tree """
        pass

    def download_files(self, num_of_files=5):
        # downloads only "num_of_files" number of files
        # this may not make any sense actually. Does this download
        # files based on the directory structure created by the tree?
        pass

    def update_gdrive_dir_tree(self):
        pass

    def push_local_file_changes_to_drive(self):
        pass

if __name__ == '__main__':
    gdrivehelper = GDriveMgrHelper('~') # root dir will be home
    # get authorized and create a service
    service = gdrive.create_service()
    gdrivehelper.set_service(service)
    gdrivehelper.create_tree("root") # this will build tree starting at root google drive directory
    # next create the local directory Tree
    # then create the file structure - temporary for testing
    # then download all the files into their proper locations

 
