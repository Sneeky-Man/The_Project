## Errors and Bugs

### Critical
##### This bug is completely game breaking and happens fairly regularly
* .

### Major
##### This bug is a big problem but is either not game breaking, or happens very irregularly
* Grabbing the screen and moving it will cause the game to slow to about 30fps, causing bullets to fire faster
* Using arcade.Text to draw text sometimes causes big red lines to appear. This is likely a bug within arcade.
* When moving and aiming, the red line in not accurate to the cursor
(probably because it's not taking into account the player movement)

### Minor
##### This bug is a minor problem, due to its lack of severity or extreme rarity
* When the building is set to turn towards a target (not snap), if the target comes at a certain angle, 
the building will do a 360 instead of turning to the target
* There is a fps drop of about 20 frames for a couple seconds, when it just started the map. (This happens on all maps).

### Non-Lethal
##### A Bug that really shouldn't happen, but pose very-little to no threat
* When downloading the packages, The_Project-(whatever the version is) is downloaded.
* When two bullets hit the same target at the same time, both bullets will be lost, even if the target was killed by the first bullet