#!/usr/bin/python

from __future__ import absolute_import

import httplib2
import os

from apiclient import discovery
from apiclient import errors 
from apiclient import http
import oauth2client
from oauth2client import client
from oauth2client import tools

from tree import Tree, Node

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Quickstart'

# Directories
HOME_DIR = os.path.expanduser('~')
GDRIVE_ROOT_DIR = os.path.join(HOME_DIR, 'Google_Drive')
CREDENTIAL_DIR = os.path.join(HOME_DIR, '.credentials')

 
def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    :return: Returns credentials, the obtained credential via oauth.
    """
    
    if not os.path.exists(CREDENTIAL_DIR):
        os.makedirs(CREDENTIAL_DIR)
    credential_path = os.path.join(CREDENTIAL_DIR, 'credentials.dat')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print ('Storing credentials to ' + credential_path)
    return credentials


def create_drive_root_dir():
    """ Simply creates directory in /home/$USER called 'Google_Drive'"""
    if not os.path.exists(GDRIVE_ROOT_DIR):
        os.mkdirs(GDRIVE_ROOT_DIR)
    
     
def download_file(service, file_id, local_fd):
    """
    Download a Drive file's content to local filesystem
    
    Args:
        service: Drive API Service instance
        file_id: ID of the Drive file to be downloaded
        local_fd: io.Base or file object, the stream that Drive file's contents
            will be written to.
    """
    request = service.files().get_media(fileId=file_id)
    media_request = http.MediaIoBaseDownload(local_fd, request)

    while True:
        try:
            download_progress, done = media_request.next_chunk()
        except errors.HttpError, error:
            print("an error occurred: %s" % error)
            return
        if download_progress:
            print("Download progress: %d%%" % int(download_progress.progress()*100))
        if done:
            print("Download Complete")
            return

def create_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)
    return service

def get_file_metadata(service, file_id):
    """ queries Drive API to get info about a file """
    return  service.files().get(fileId=file_id).execute()

def get_children(service, folder_id):
    """ 
    Gets all children items of a folder from Google Drive
    :param: service = a Google Drive service object
    :param: folder_id = the Google Drive id of a folder. Use "root" to
    get all children items of Google Drive root folder
    :return: Returns a list of children file/folder ids
    """
    page_token = None
    child_id_list = []
    
    while True:
        children = service.children().list(folderId=folder_id, pageToken=page_token).execute()
        for child in children.get('items', []):
            child_id_list.append(child['id'])
        page_token = children.get('nextPageToken')
        if not page_token:
            break
    return child_id_list

def main():
    """Shows basic usage of the Google Drive API.
    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    create_drive_root_dir() # make sure Google_Drive dir exists

    service = create_service() 
    
    # Main directory Tree structure used to build drive folders
    root_node = Node('Google_Drive')
    gdrive_tree = Tree(root_node)

    results = get_children(service, 'root')
    for result in results:
        print(result)
    print("there were " + str(len(results)) + " files found in root folder")
    #results = service.files().list(maxResults=10).execute()
    #items = results.get('items', [])
    # just test that the root dictionary of children is right
    #print(get_children(service, "root"))

    # ignore the rest of this function
    items = None
    if not items:
        print 'No files found.'
    else:
        print 'Files:'
        for item in items:
            print '{0}|{1}|{2}'.format(item['title'], item['id'], item['parents'])
            print("-----------------------------------")
            print("file id is type: " + str(type(item['id'])))
            nothing =  """ if item['parents']:
                parent = item['parents'][0]
                curr_node = Node(item['title'], item['id'], parent['id']) 
                parent_node = curr_node
                while not parent['isRoot']:
                    curr_node = parent_node
                    # get the parent info from Google Drive API
                    request = service.files().get(fileId=curr_node.get_id())
                    
                    # create parent node for querying next node up
                    if not request['parents']:
                        break
                    parent_node = Node(request['title'], request['id'])
                        # add current node as child as we walk up the hierarchy
                    parent_node.add_child(curr_node)
                # getting here should mean parent is root
                root_node.add_child(curr_node) # global variable 'root_node'
    #local_file = open(item['title'], "w")
    #download_file(service, item['id'], local_file)
"""

if __name__ == '__main__':
    pass
    #import timeit
    #print("Timing calling google drive to list 20 children from root")
    #print("----------------------------------------------------")
    #print(timeit.timeit("main()", number=1))
    #main()
