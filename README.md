# pulseboard
The arguably functional, proof-of-concept micspam soundboard tool using Pulseaudio

# Installation
The installtion of this mess consists of 2 parts - setting up the pulseaudio modules to work with the pulseboard.py file using setup.sh and then running the system itself using pulseboard.py

## setup.sh

There are two variations of the setup.sh script - the pulse-pipe.sh (which is a standalone script intended for testing) and setup.sh

Both of these will ask several questions during the installation. The difference is that pulse-pipe is made to be used standalone

## pulseboard.py

Pulseboard uses a config file - ``.pulsebrc``, for setting up the keybindings for sounds.

The format is as follows:

```
[mode#keybind]="command"
```
where "mode" is a modifier for the keybinding set to be used, "keybind" is a hotkey mapping that looks somewhat like this
```
<alt>+9
<ctrl>+<alt>+j
<ctrl>+n
```
and where "command" is the command to be executed if the hotkey is used. See the example below for reference.

## Console mode

The console mode allows tuning some specific settings, like volume, output device, etc.
All of the commands in the console mode can be set as keybindings (even ``help``, if you're willing to do that for some reason). 
To view the full list of commands, type ``help``.

## .pulsebrc Example

```
[<alt>+<shift>+g]="mode ingame"
[<alt>+<shift>+d]="mode discord"
[ingame#<alt>+1]="play /home/yessiest/sounds/sound1.wav"
[ingame#<alt>+2]="play /home/yessiest/sounds/sound2.mp3"
[ingame#<alt>+<shift>+1]="play /home/yessiest/sounds/sound3.wav"
[discord#<alt>+g]="play /home/yessiest/sounds/discord/funnifarts.ogg"
[discord#<alt>+t]="play /home/yessiest/sounds/discord/rickroll.mp3"
```

This will create 2 modes - the mode named "discord" (which is activated by pressing alt+shift+d) and the "ingame" mode (which is activated by pressing alt+shift+g)

Both modes have different keybindgins set for them. Note that the commands are typed exactly as they would be typed in the console mode.

#License

This work is licensed under the MIT license.
