# pixels_curve
A clone of [Curve Fever](http://curvefever.com/) for the Arduino Pixels. 

### How to play
The game supports 2-4 players. It is similar to the popular game "Snake", but it's more of a dot that leaves behind a trail in it's own color. You control the dot with only two buttons, which makes it turn left or right by 90°, relative to its current direction. Sometimes there will be a gap in the trail it leaves, so you can slip through. If you move into the trail of someone, including yourself, you die. The last player to live, wins. 

### Controls
* Player 1/Red: First joystick, left/right 
* Player 2/Blue: First set of buttons, Button 1/2
* Player 3/Yellow: Second joystick, left/right 
* Player 4/White: Second set of buttons, Buttons 1/2

### Powerups
* Red: Increase speed 
* Green: Decrease speed
* Cyan: Increase line thickness of enemies
* Blue: Invincibility
* Magenta: Reversed steering of enemies

Colors of powerups are subject to change

### Planned features:
* Random spawning and starting-direction
* Powerups?

You'll need [this](https://github.com/HackerspaceBremen/pygame-ledpixels) to play the game.
