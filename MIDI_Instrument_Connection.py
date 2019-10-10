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

import itertools
import pygame.midi
import time

pygame.midi.init()
num_devices = pygame.midi.get_count()

def uglylist_to_nicelist(midi_input):
    newlist=[]
    flattend = list(itertools.chain(*midi_input))
    for i in flattend[0]:
        newlist.append(i)
    newlist.append(flattend[1])
    return newlist


#Linux Opensuse Boppad name:    b'BopPad MIDI 1'
#Windows 10     Boppad name:    b'Boppad'
def return_midi_device():
    for i in range(num_devices):
        device = pygame.midi.get_device_info(i)
        if device[1] == b'BopPad':
            if device[2] == 1:
                print("BOPPAD DEVICE INFORMATION: %s" %(str(pygame.midi.get_device_info(i))))
                MIDI_DEVICE = pygame.midi.Input(i, 4096)
            else:
                pass
    return MIDI_DEVICE

def work(export_file):
    my_device = return_midi_device()
    l=[]
    nl = []
    lever=True
    n_zero = 0
    while_count = 0
    export_file = open(export_file, "w")

    while True:
        if my_device.poll():
            l=my_device.read(1)
            nl = uglylist_to_nicelist(l)

            #start timestamps from zero
            if while_count == 0:
                n_zero = nl[4]
                nl[4] = nl[4]-n_zero
                del nl[3],nl[2],nl[0]
            else:
                nl[4] = (nl[4]-n_zero)/1000
                del nl[3],nl[2],nl[0]

            #turn lever on/off to exclude release midiinputs
            if lever == True:
                export_file.write("%s\n"   % str(nl))
                #return ("%s"   % str(nl))
                print(nl)
                lever = False
            elif lever == False:
                pass
                lever = True

            while_count += 1
        else:
        	pass
