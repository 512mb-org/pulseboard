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
    iter+=1
    print(str(iter)+") "+devname.decode("utf-8"))
device_id = int(input())
while device_id < 0 or device_id > len(devices):
    print("No such device")
    device_id = int(input())
device = devices[device_id]
#define some functions for help
def exists(dic,key):
    try:
        return dic[key]
    except:
        return False
def exec(comm):
    print(comm)
    if comm.startswith("play"):
        filename = re.match("play (.+)",comm).group(1)
        micspam_player.audio_output_device_set(None,device)
        micspam_player.set_mrl(filename)
        micspam_player.play()
    if comm.startswith("debug"):
        print("Debug test")
    if comm.startswith("test"):
        raise StopException()
class InputHandler:
    def __init__(self):
        self.keymap = {}
        self.inputbuffer = []
    def on_press(self,key):
        self.inputbuffer.append(key)
        if exists(self.keymap,str(self.inputbuffer)):
            exec(self.keymap[str(self.inputbuffer)])
    def on_release(self,key):
        try:
            self.inputbuffer.remove(key)
        except:
            self.inputbuffer.clear()
    def bind(self,keymap,comm):
        name = keyboard.HotKey.parse(keymap)
        self.keymap[str(name)] = comm
    def unbind(self,keymap):
        name = keyboard.HotKey.parse(keymap)
        if exists(self.keymap,str(name)):
            self.keymap.pop(str(name))
kmap = InputHandler()
try:
    rc = open("./.pulsebrc")
    text = rc.read()
    for match in re.findall("\[([^\]]+)\]=\"([^\"]+)\"\n",text):
        kmap.bind(match[0],match[1])
except IOError:
    print("No pulsebrc found - creating")
    rc = open("./.pulsebrc","w")
with keyboard.Listener(on_press=kmap.on_press,on_release=kmap.on_release) as listener:
    listener.join()
