# This is a record of all changes to the project


## 07/12/21
After accidentally deleting all my files, I decided to restart from the start to make sure I do this right.
* The Initial Commit of most of my files
* Attempted to get pip install -e. to work, but failed. Will try again tomorrow

## 08/12/21, 16:19
* Added Logging System. All logs INFO and above go to log_file.txt
* Started work on a very basic prototype of the ground tile sheet
* Started work on a more realistic ground tile sheet

## 09/12/21, 00:11
* Done more work on a very basic prototype of the ground tile sheet
* Setup terrain correctly for the tile sheet

## 09/12/21 17:55
* Another attempt at getting pip install -e. to work 
* Added prototype turret designs

## 09/12/21 23:20
* Installing the repo should now work
* Added BUGS.md
* Added directions to download the repo

## 10/12/21 12:48 
* Moved BUGS.md

## 11/12/21 23:25
* Added an Entity Sprite Class
* Added a Player Class using Entity
* Added a Paths.py script that auto creates paths, and logs errors if the path wasn't found
* Added a constants.py file
* Added a bunch of prototype sprites
* Added sprites that now work
* Added basic physics engine
* Implemented a naming convention for sprites. Examples (turret_tier_2_blue)(base_red)

## 12/12/21 20:05
* Added a lot of comments in Entity
* Added new tile sets with correct naming conventions 
* A logging bug fix

## 16/12/21 00:40
* Relative lack of progress is due to not knowing what kind of game I want to make. 
I'm still pretty unsure, but I think it's best to make some prototypes, and find out what's fun that way.
* Due to this, I have switched up a lot of the ROADMAP.md
* Added building.py
* Updated how file paths are found
* Updated the tile sets

## 21/12/21 11:13
* Lack of progress is due to procrastination, will try to do actual work over the holidays

## 03/01/22 23:07
* Procrastination has continued as i have gotten very invested in foxhole, to the detriment of other things. Will force myself to start doing work.

## 03/01/22 23:13
* Added Bullet.py
* Updated tile sets
* Added same_team to entity
* Other minor improvement

## 05/01/22 04:57
* Created branch database_dev to store future commits
* Started work on replacing the triple dict in constants.py with a SQLite database

## 07/01/22 01:44
* Finished initially setting up the database. Work still needs to be done on integrating the map and database

## 07/01/22 02:44
* Added an automatic check if the paths exists
* Commented out paths.py. Will likely delete soon

## 03/02/22 01:11
* Due to massive amounts of procrastination, and a sprinkling of prelims and database stuff, little work has been done.
* To compensate, a GANTT chart has been made and the roadmap will be updated soon

## 04/02/22 23:40
* The database has been replaced and implemented. It still needs to be integrated with the tiled map.
* Logging on the database has been changed to be more helpful.
* GANTT chart updated.

## 09/02/22 11:00
* Database has been fully integrated with the tiled map. All tiles in the foreground are now converted to be a Building.
* Redone the Entity and Building classes to be more simplified and readable
* Re-added Range Detectors for buildings. They are now colored.
* Buildings with enemies in their range detectors will snap to face them. 
* Work still needs to be done on firing at the closest target and turning slower.
* GANTT chart updated
* Will attempt to merge database_dev to the main branch