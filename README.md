# GDriveMgr

A basic Google Drive management tool for **Fedora Linux**. It astonishes me that such a popular distro can be without an official client app for Google Drive.

## Fair Warning
I am currently designing this (very) basic app more for practice than anything else. I am a student trying to improve my coding skills, so please take that into consideration should you stumble across this repo.

## Contact Me
I welcome constructive criticism. If you know of something that could be done much easier or more efficient, please let me know!

## Running Tests
There are 2 ways to run tests at the moment:
1. Run each test directly
  * You need to be in the GDriveMgr root directory and run `python -m tests/<test_file>`
  * You need to have the GDriveMgr folder in the $PYTHONPATH environment variable:
```
$ export PYTHONPATH=/path/to/GDriveMgr
```
2. Run all tests automatically
  * You cd into the tests folder and call `./run_all.sh`

