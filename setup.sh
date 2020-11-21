#!/bin/bash
#This script installs needed packages and configures pulseaudio modules
echo "Checking pre-requisites"
pkglist=$(pip list)
#check if pulseaudio is available
which pulseaudio && which python3 && which pip3 && which vlc
if [ $? == 1 ]; then
  echo "PulseBoard needs following components to be installed:
vlc
pulseaudio
pip (pip3)
python (python3)

Install them to continue
  "
  exit 1
fi
#check if pulse daemon is running
if [ "$(pgrep pulseaudio)" == "" ]; then
  echo "Pulseaudio daemon isn't running - attempting to start it"
  pulseaudio --start
  if [ $? != 0 ]; then
    echo "Failed to start pulseaudio."
    exit 1
  fi
fi
#check if python-vlc and autokey are installed. if they are not, install them
if [ "$(echo $pkglist | grep python-vlc)" == "" ]; then
  echo "python-vlc is not installed - installing"
  pip3 install --user python-vlc
fi
if [ "$(echo $pkglist | grep autokey)" == "" ]; then
  echo "autokey is not installed - installing"
  pip3 install --user autokey
fi
echo -ne "Finished checking the required python modules\n"
unset pkglist
if [ $(pacmd list-sinks | grep "pulseboard-sink") ]; then
  echo "PulseBoard seems to be loaded - sink exists. Skipping."
  exit 0
fi
echo "Enabling pulse modules"
sources="$(pacmd list-sources)"
source_count=$(grep index -c <<< "$sources")
if [ "$source_count" -gt 1 ]; then
  echo "There are multiple sources available for microphone"
  echo "$sources" | grep "index:" -A 4
  echo "Type the index of the your microphone and press enter"
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
pacmd load-module module-null-sink sink_name="pulseboard-sink"
echo $?
#relay the audio from the mic into the null sink
pacmd load-module module-loopback source="$mic_name" sink="pulseboard-sink"
#make our monitor a source
pacmd load-module module-remap-source master="pulseboard-sink.monitor" source_name="pulseboard-sink.remap"
echo "Finished setting up pulse modules"
echo "If everything went right, you now should have a device called \"Remapped Monitor of Null Output\". Set it as your mic and you're good to go"
