# Software um Gespieltes zu transkribieren
# Copyright (C) 2019  Linus Wesp
#
# This file is part of "Digitaler Kromarograph"
#
# "Digitaler Kromarograph" is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# "Digitaler Kromarograph" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with "Digitaler Kromarograph".  If not, see <https://www.gnu.org/licenses/>.

#!/usr/bin/env python
import ast
from midiutil import MIDIFile
import time

def return_filename(fname, format):
    timestamp = time.strftime("%Y.%m.%d-%H.%M.%S")
    return "%s%s.%s" %(fname,timestamp, format)

def read_listtxt_to_list(filename):
     newlist = []
     lines = [line.rstrip('\n') for line in open(filename)]
     for i in lines:
          newlist.append(ast.literal_eval(i))
     return(newlist)

def work(source, out, tempo):

    track    = 0    # Track numbers are zero-origined
    channel  = 0    # MIDI Channel
    time     = 0    # In beats
    duration = 2    # In beats
    volume   = 100  # 0-127, as per the MIDI standard

    midiinputs = read_listtxt_to_list(source)
    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created automatically)
    MyMIDI.addTempo(track, time, tempo)

    for i in midiinputs:
        time = i[1]
        pitch = i[0]
        MyMIDI.addNote(track, channel, pitch, time, duration, volume)

    with open(out, "wb") as output_file:
        MyMIDI.writeFile(output_file)
