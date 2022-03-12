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
* Procrastination has continued as I have gotten very invested in foxhole, to the detriment of other things. Will force myself to start doing work.

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

## 09/02/22 11:30
* Test to make sure merge worked

## 10/02/22 09:50
* Implemented the collision detection system (aside from one bug).
* It now continues to target one enemy until its no longer in range, 
then finds the nearest target and attacks them.

## 12/02/22 18:10
* Reverted the target system due a bug. Now buildings snap to the next target.
* Added and implemented bullets
* Changed map_1 to test_map_sparse
* Added test_map_battle
* Still an issue with buildings not realising their targets have died
* Updated GANTT Chart

## 17/02/22 14:20
* Changed how the building targeting system works.
This was for performance. The previous way was cripplingly slow.
* Changed the Entity, Building, and Player __str__ to __repr__
* __repr__ now show a very basic overview (name, tier, team, coords)
* Entity, Building, and Player now has longer_report() which gives a more detailed report (e.g. path, targets, targetted_by)
* Split the foreground list in scene into four categories: Red Player, Blue Player, Red Building, Blue Building.
This is partially for performance reasons, and because it makes it a lot easier logic wise.
* Added 2 more maps, bring it up to four.
* Sparse_1 is a 1v1 with a red turret and a blue base. This is for testing a single turret, a non turret, and a player
* Sparse_2 is a 3v1 with 3 red turrets and a blue base. This is for testing how multiple turrets handle each other, and if they stop firing correctly.
* Sparse 3 is a 3v3 with 3 red turrets and 3 blue turrets. This is for making sure both teams of turrets work.
* Battle is a mock battle between 25 blue turrets and 25 red turrets. This is for performance testing.
* Added self.__targetted_by to all entities (although bullet doesn't use em). This is a list of all buildings targeting the building/player.
This is needed, as when that player/building dies, it uses that list to tell the buildings shooting it to remove their target.
This means I don't need to keep checking if the target is still their every frame, saving a ton of performance.
* Updated BUGS.md
* Added debug mode. This is enabled by setting self.debug to True. 
* When debug mode is active, if you click over a Building or Player (not bullet), it will print the longer_report of that sprite.
* Additionally, buildings will not start firing until the space bar is pressed.
* Added an FPS counter, and a counter counting the amount of Buildings on the map (excluding Bullets)
* Improved documentation

## 19/02/22 17:00
* Dramatically Updated GANTT Chart
* Bullet is now a subclass of arcade.Sprite, instead of Entity.

## 19/02/22
* Added the health system
* Added the damage system
* Updated the database to handle the new variables
* Got rid of setting variables in Player and Building that should only be set in Entity
* Updated the GANTT Chart

## 23/02/22 15:00
* Updated to arcade 2.6.10. This gave serious fps improvements due to the changes with the collision_with_lists.
* Added hotbar and hotbar selected images 1-5.
* Added damage and healing text (although its temp disabled due to a bug with arcade)
* Added fading_text.py (this is for the damage text)
* Updated BUGS.MD
* Updated GANTT chart

## 23/02/22 15:15
* Added Hotbar Hammer Icon

## 25/02/22 16:47
* Added items.py. This is where all items used in a players hotbar will be made.
* Added Hammer to items.py. This hammer will (when equipped) heal buildings with left click, within a range of 100.
* The hammer, when equipped, will follow the mouse.
* Added Hotbar Hammer Item (just a smaller ver of the icon)
* Replaced all instances of the GameWindow being passed to classes and defs with arcade.get_window()
* While in debug mode, you must middle-click to print the longer_report
* Updated GANTT Chart

## 25/02/22 17:12
* Updated README.md
* Updated GANTT Chart

## 28/02/22 12:23
* Updated how the Hammer positions itself

## 28/02/22 
* Reorganised the asset folders
* Remade all the maps:
  * Normal
    * map_battle: Normal 25v25 battle
  * Test Maps - Testing game features
    * sparse_1: 1v0 (Turret v Base)
    * sparse_2: 1v0 (Turret v Bases)
    * sparse_3: 1v1 (Turret v Turret)
    * sparse_4: 3v1 (Turrets v Turret + Bases)
    * sparse_5: 3v4 (Turret v Turrets)
  * Performance Maps - Testing the performance of the maps
    * map_1: 50 v 50 Bases
    * map_2: 100 v 100 Bases
    * map_3: 200 v 200 Bases
    * map_4: 25 v 25 Turrets
    * map_5: 50 v 50 Turrets
    * map_6: 75 v 75 Turrets
    * map_7: 100 v 100 Turrets
* Health bar will only show when the building isn't full health. This is for performance reasons.
* Pressing middle-click while in debug mode will switch the map to the next one in the list.
* Updated GANTT Chart

## 04/03/22 00:15
* Made Item, a class to deal with player items. 
* Hammer is now a subclass of Item

## 04/03/22 20:15
* Fully implemented the hot bar system.
* Split Bullet into BaseBullet, BuildingBullet and ItemBullet. 
* BuildingBullet and ItemBullet is a subclass of BaseBullet
* Added the Pistol Item
* Added Pistol Icon and Item Images
* Added cool down to Items
* Added a cool down effect to item icons.
* Added a bullet list to Players
* Updated GANTT Chart 

## 07/03/22 20:00
* Complete overhaul on how building targeting works. 
Removed the range detector technique, and replaced it with arcade.get_closest_sprite().
* This increased 50v50 turret fps from 20 to 40. Why did i not find this earlier!
* Added being_built.py, but its not finished yet.
* Slight edit to the pistol images.

## 08/03/22 18:05
* Implemented BeingBuilt in being_built.py. 
* Buildings that are being built will be a member of BeingBuilt, which is a subclass of entity.
* Buildings that are being built will fade in, before transiting into a proper building.
* When right-clicking with the hammer, a lv 1 turret will be made on that tile, if nothing is on the tile.

## 08/03/22 18:06
* Updated GANTT Chart

## 09/03/22 20:20
* Added aiming with weapons
* Added left_click_release and right_click_release to items.
* Updated GANTT Chart

## 12/03/22 17:33
* Added Camera scrolling
* Changed items to work with the new cameras