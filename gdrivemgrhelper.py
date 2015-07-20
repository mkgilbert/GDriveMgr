#!/usr/bin/python

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
        
    def create_tree(self, folder_id):
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
                self.create_tree(f['parent_id'])

            # file is a folder that could have files in it...
            if f['mime'] == 'application/vnd.google-apps.folder':
                print("")
                print("----------------------------------------")
                print(" New folder: " + f['title'])
                print("----------------------------------------")
                print("")

                self.create_tree(f['id'])  
  
        return
                

    def create_files(self):
        """ Builds directory file structure based on the dir_tree """
        

    def download_files(self):
        # downloads only "num_of_files" number of files
        # this may not make any sense actually. Does this download
        # files based on the directory structure created by the tree?
        with open('dir_tree.pickle', 'rb') as f:
            print("loading tree...")
            tree = pickle.load(f)
        
        root = gdrive.GDRIVE_ROOT_DIR
        path = root
        curr_node = tree.get_root()
        while True:
            for node in curr_node.get_children():
                if node.get_mime() == 'application/vnd.google-apps.folder':
                    path = os.path.join(path, node.get_title())
                    os.mkdir(path)
                else:
                    gdrive.download_file(self.get_service(),
                                         node.get_id(),
                                         os.path.join(path, node.get_title()))
            break

    def update_gdrive_dir_tree(self):
        pass

    def push_local_file_changes_to_drive(self):
        pass

if __name__ == '__main__':
    gdrivehelper = GDriveMgrHelper('~') # root dir will be home
    # get authorized and create a service
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
