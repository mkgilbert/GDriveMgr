#!/usr/bin/env python

from __future__ import absolute_import

import os
import pickle

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
        """:param: root_dir = a node to build tree off of"""
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
        """ 
        Gets the metadata for all the children inside a Google Drive folder
        
        :param: folder_id = the Google Drive id of a folder

        :return: list of dicts that have all the file metadata
        """
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

            files_list.append({
                                'id': child_id, 
                                'mime': mime, 
                                'title': title, 
                                'parent_id': parent_id,
                                'metadata': metadata
                            })
            
            # logging to stdout
            total += 1
            print("Retrieved file " + str(total) + ". " + title + " (" + mime + ")")
        
        return files_list
        
    def create_tree(self):
        """
        Generate a Tree object using file metadata from all of the files in
        Google Drive. then save it as a pickled object inside the data directory.
        """
        self._rec_create_tree("root") # Google API uses "root" as id of root folder 
        # pickle the object to a file so we can reuse it as a template to download files
        dir_tree_path = os.path.join(gdrive.DATA_DIR, 'dir_tree.pickle')
        with open(dir_tree_path, 'wb') as f:
            pickle.dump(self.dir_tree, f)
        
    def _rec_create_tree(self, folder_id):
        """
        Helper to create directory tree object

        :param: folder_id = Google Drive id of a folder
        """
        if folder_id is None:
            return

        if folder_id == 'root':
            print("")
            print("----------------------------------------")
            print(" Starting to create tree from Root")
            print("----------------------------------------")
            print("")

        files_list = self._get_files_in_folder(folder_id) # tuple
       
        for f in files_list:
            # add the file to the folder with id 'folder_id'
            new_node = Node(id=f['id'], 
                            title=f['title'], 
                            parent_id=f['parent_id'],
                            metadata=f['metadata'])
            
            result = self.dir_tree.add(new_node)
          
            if result == 0:
                # parent_id was None, so it shouldn't be added
                continue
            elif result == -1:
                # parent node doesn't exist yet, so go get it
                self._rec_create_tree(f['parent_id'])

            # file is a folder that could have files in it...
            if f['mime'] == 'application/vnd.google-apps.folder':
                print("")
                print("----------------------------------------")
                print(" New folder: " + f['title'])
                print("----------------------------------------")
                print("")

                self._rec_create_tree(f['id'])  
  
        return
                

    def _rec_download_files(self, node):
        """Helper function to download_files()"""
        for child in node.get_children():
            if child.get_mime() == 'application/vnd.google-apps.folder':
                try:
                    os.mkdir(child.get_title())
                except OSError as e:
                    print("Error:", e)
                    print("Tried to create '%s'" % child.get_title())
                try:    
                    os.chdir(child.get_title())
                except OSError as e:
                    print("Error:", e)
                    print("Couldn't chdir to '%s'. Skipping download of this directory." % child.get_title())
                    continue

                self._rec_download_files(child)
            elif 'vnd.google-apps' in child.get_mime():
                # file is a "google doc" file and can't be downloaded. Http error 400
                continue
            else:
                try:
                    gdrive.download_file(self.get_service(), 
                                         child.get_id(), 
                                         child.get_title())
                except OSError as e:
                    print("Error:", e)
                    print("Failed downloading '%s'" % child.get_title())
        os.chdir('../')

    def download_files(self):
        """ 
        Uses dir_tree to create folders and download all files except Google Docs.
        
        :return: 1 if encountered an OSError, 0 if no errors
        """
        with open('dir_tree.pickle', 'rb') as f:
            print("loading tree...")
            tree = pickle.load(f)
        
        os.chdir(gdrive.GDRIVE_ROOT_DIR)

        try:
            self._rec_download_files(tree.get_root())
            return 0
        except OSError as e:
            return 1

    def update_gdrive_dir_tree(self):
        pass

    def push_local_file_changes_to_drive(self):
        pass

if __name__ == '__main__':
    gdrivehelper = GDriveMgrHelper('~') # root dir will be home
    # get authorized and create a service
    gdrive.create_drive_root_dir()
    service = gdrive.create_service()
    gdrivehelper.set_service(service)
    #gdrivehelper.create_tree("root") # this will build tree starting at root google drive directory
    #print(gdrivehelper.dir_tree)
    
    # pickle the object to a file so we can reuse it as a template to download files
    #with open('dir_tree.pickle', 'wb') as f:
    #    pickle.dump(gdrivehelper.dir_tree, f)
        
    # next create the local directory Tree
    # then create the file structure - temporary for testing
    # then download all the files into their proper locations

    gdrivehelper.download_files() 
    print("")
    print("*** Finished Downloading Files ***")

