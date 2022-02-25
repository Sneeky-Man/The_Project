# The_Project
This is my game for my project in AH Computing and Level 6 Games Design. 
The success or failure of this project is dependent on if the game is fun

* Everything is open-source under the permissive MIT license.
* This game is coded in Python, using the [Arcade](https://api.arcade.academy/en/latest/) library
* Maps are made with [Tiled Map Editor](https://www.mapeditor.org/)


# Important Files
* See the ROADMAP.md file for a roadmap of development
* See the CHANGELOG.md file for a log of all changes
* See the BUGS.md file for a log of all unresolved bugs

# How to Download using [Pycharm](https://www.jetbrains.com/help/pycharm/manage-projects-hosted-on-github.html)
* Navigate to the Main Menu of Pycharm. To find this, close all your current projects
* Press the "Get From VCS" Button at the top right
* Select "Repository URL", Set "Version Control" to Git, Set URL to "https://github.com/Sneeky-Man/The_Project",
and put the directory to where ever you want the project (make sure it's an empty folder)
* Navigate to File > Settings > Project, Python Interpreter
* Add a new environment (python 3.10 may not work!) and finish.
* After this there should be a bunch of packages. If there is only a couple, then navigate to the Terminal and input 
```
pip install -e.
```

# How to Download using [Git for Windows](https://gitforwindows.org)
* Open git-cmd.exe, and type:
```
git clone https://github.com/Sneeky-Man/The_Project
```
* Once it is cloned, open the project up in pycharm (other programs will probably work, but i haven't tested any).
* Navigate to File > Settings > Project, Python Interpreter
* Add a new environment (python 3.10 may not work!) and finish. 
* Navigate to the Terminal and input:
```
pip install -e.
```
# Important Note
* This was coded in Arcade 2.6.10 and Python 3.9. Beware of using updated versions of Arcade or Python