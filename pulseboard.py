from pynput import keyboard
import vlc
import re
import random
print("Instantiating the player")
instance = vlc.Instance()
micspam_player = instance.media_player_new()
#get device list
devices = []
mods = micspam_player.audio_output_device_enum()
if mods:
    mod = mods
    while mod:
        mod = mod.contents
        devices.append(mod.device)
        mod = mod.next
vlc.libvlc_audio_output_device_list_release(mods)
#print the dialogue for selecting the audio output
print("Select audio device: ")
iter = 0
for devname in devices:
    print(str(iter)+") "+devname.decode("utf-8"))
    iter+=1
device_id = int(input())
while device_id < 0 or device_id > len(devices)-1:
   print("No such device")
   device_id = int(input())
global device
device = devices[device_id]
#define some functions for help
mode = ""
def exists(dic,key):
    try:
        return dic[key]
    except:
        return False
class InputHandler:
    def __init__(self):
        self.keymap = {}
        self.inputbuffer = []
        self.mode = ""
    def on_press(self,key):
        self.inputbuffer.append(key)
        if exists(self.keymap,self.mode+"#"+str(self.inputbuffer)):
            exec(self.keymap[self.mode+"#"+str(self.inputbuffer)])
    def on_release(self,key):
        try:
            self.inputbuffer.remove(key)
        except:
            self.inputbuffer.clear()
    def bind(self,keymap,comm):
        keybind = re.match("(.*#)?(.+)",keymap)
        kmode = keybind.group(1) or "#"
        name = keyboard.HotKey.parse(keybind.group(2))
        self.keymap[kmode[0:-1]+"#"+str(name)] = comm
    def unbind(self,keymap):
        name = keyboard.HotKey.parse(keymap)
        if exists(self.keymap,mode+"#"+str(name)):
            self.keymap.pop(mode+"#"+str(name))
    def list(self):
        for k,v in self.keymap.items():
           print(k+": "+v)
    def set_mode(self,mode):
        self.mode = mode
kmap = InputHandler()
def exec(comm):
    global device
    if comm.startswith("play "):
        filename = re.match("play (.+)",comm).group(1)
        micspam_player.set_mrl(filename)
        micspam_player.audio_output_device_set(None,device)
        micspam_player.play()
    if comm.startswith("stop"):
        micspam_player.stop()
    if comm.startswith("mode"):
        mode = re.match("mode([^\n]+)",comm).group(1)
        mode = mode.lstrip()
        kmap.set_mode(mode)
    if comm.startswith("list"):
        kmap.list()
    if comm.startswith("device-list"):
        dev_id = 0
        for I in devices:
            print(str(dev_id)+") "+I.decode("utf-8"))
            dev_id+=1
    if comm.startswith("device-set "):
        dev_id = re.match("device-set (\d+)",comm).group(1)
        device = devices[int(dev_id)]
    if comm.startswith("volume"):
        volume = re.match("volume ([\+\-]?)(\d+)",comm)
        current = micspam_player.audio_get_volume()
        if volume == None:
          print("Volume: "+str(current))
        else:
          if volume.group(1) == '':
            micspam_player.audio_set_volume(int(volume.group(2)))
          elif volume.group(1) == '+':
            micspam_player.audio_set_volume(current+int(volume.group(2)))
          elif volume.group(1) == "-":
            micspam_player.audio_set_volume(current-int(volume.group(2))) 
          print("Volume: "+str(micspam_player.audio_get_volume()))

    if comm.startswith("help"):
        print("""
Commands:
help - print this message
play <filename> - play the sound to the currently set device
stop - stop the sound
mode <mode> - set the bind mode
list - list all bindings
device-list - list all devices
device-set - set the output device
exit - exit the program
volume [<-+>]<percent> - set volume (example: volume +5, volume 50)

bindings should be set via ./.pulsebrc file in this form:
[mode#<shift>+k]="command"
where <shift>+k is the keybinding you wish to set (special keys should be wrapped in <>)
and command is the command to execute
        """)
try:
    rc = open("./.pulsebrc")
    text = rc.read()
    for match in re.findall("\[([^\]]+)\]=\"([^\"]+)\"\n",text):
        kmap.bind(match[0],match[1])
except IOError:
    print("No pulsebrc found - creating")
    rc = open("./.pulsebrc","w")
    exit()
running = True
with keyboard.Listener(on_press=kmap.on_press,on_release=kmap.on_release) as listener:
    while running:
        term_comm = input("> ")
        if term_comm.startswith("exit"):
            running = False
        else:
            exec(term_comm)

