# Crazy Truck

## How to install the game
First you have to install all requirements.

requirements.txt
```
pygame==2.5.2
pygame-menu==4.4.3
```

The easiest way to install the requirements is by executing the installStart.sh file.
The shell-script works on Linux, may not work on Windows

installStart.sh
```
#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# runnable script
chmod +x installStart.sh

# Run the game
python3 main.py
```

## How to navigate the menu
* Navigation works with the arrow keys + enter or you can also simply use your mouse.

## How to control the transporter
* Move with WASD or arrow keys.

## How to play the game
* Collect ores while the helicopter chases you.
* The helicopter will steal all of your ores in an instant if he manages to catch you.
* Refill your gas, drive to the gas station to do so.
* Not paying attention to your tank leads to a game over.
* You have to deliver atleast 80% of the total amount of ores to win the game.
