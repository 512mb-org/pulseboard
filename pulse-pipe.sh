#!/bin/bash
#This is a standalone test version of the upcoming soundboard's pulseaudio pipe system

which pulseaudio
if [ $? == 1 ]; then
  echo "Pulseaudio is not installed, cannot continue"
fi
if [ "$(pgrep pulseaudio)" == "" ]; then
  echo "Pulseaudio daemon isn't running - attempting to start it"
  pulseaudio --start
  if [ $? != 0 ]; then
    echo "Failed to start pulseaudio."
    exit 1
  fi
fi
if pacmd list-sinks | grep -q "pulsepipe-sink"; then
  echo "Pulsepipe seems to be loaded - sink exists. Skipping."
  echo "(\"pulseaudio -k; pulseaudio --start\" to reset the config)"
  exit 0
fi
sources="$(pacmd list-sources)"
source_count=$(grep index -c <<< "$sources")
if [ "$source_count" -gt 1 ]; then
  echo "There are multiple sources available for microphone"
  echo "$sources" | grep "index:" -A 4
  echo "Type the device index of the your microphone and press enter"
  read mic_index
  while grep -q 'index: '"$mic_index" <<< "$mic_index"; do
    echo "No such source"
    read mic_index
  done
  mic_name=$(echo "$sources" | grep "index: $mic_index" -A 4 | grep -o -P '(?<=name: <)[^>]+')
  unset sources
  unset source_count
fi
echo "Using $mic_name"
#create the sink to connect vlc to
pacmd load-module module-null-sink sink_name="pulsepipe-sink"
#relay the audio from the mic into the null sink
pacmd load-module module-loopback source="$mic_name" sink="pulsepipe-sink"
#make our monitor a source
pacmd load-module module-remap-source master="pulsepipe-sink.monitor" source_name="pulsepipe-sink.remap"
echo "Finished setting up pulse modules"
echo "If everything went right, you now should have a device called \"Remapped Monitor of Null Output\". Set it as your mic."
echo "Then, set the output of VLC (or any other player) as Null Output"
echo "And have fun!"
