# GDriveMgr

A basic Google Drive management tool for **Fedora Linux**. It astonishes me that such a popular distro can be without an official client app for Google Drive.

## Fair Warning
I am currently designing this (very) basic app more for practice than anything else. I am a student trying to improve my coding skills, so please take that into consideration should you stumble across this repo.

## Contact Me
I welcome constructive criticism. If you know of something that could be done much easier or more efficient, please let me know in the comments to a commit!

## How it works
This tool was originally just an exercise in learning how to download all the files in a Google drive account and recreate its directory and file structure on the local computer. That is currently all it does, but this hopefully will continue to grow as a long term project. The program can currently create a tree structure by querying Google Drive for every file, saving file info as a leaf of the tree, and putting it all into a pickle file. This pickle file, called "dir_tree.pickle" can then be loaded and used to download all of the files and place them in their appropriate directories, which are also created on the fly.

## How to use it
currently, the "gdrivemgrhelper.py" file serves as the main calling file. the downloading and creation of the tree happen here for now. Comment out the lines for creating the directory tree structure if it is already saved. Simply running the file will download all the files and place them in a folder called "~/Google_Drive".

## Running Tests
There are 2 ways to run tests at the moment

1. Run each test directly
  * You need to be in the GDriveMgr root directory and run `python -m tests/<test_file>`
  * You need to have the GDriveMgr folder in the $PYTHONPATH environment variable
  ```
  $ export PYTHONPATH=/path/to/GDriveMgr
  ```

2. Run all tests automatically
  * You cd into the tests folder and call `./run_all.sh`

