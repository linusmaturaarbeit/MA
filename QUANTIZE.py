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

import math
import itertools
import ast
import math
from operator import itemgetter

givequantizedfilename ="quantized_midinotes.txt"

def grid_intervall(metrum, quantize_note):
    metrum = int(float(metrum))
    quantize_note = int(float(quantize_note))
    normal_tempo = 60

    #erster Viertel:
    first_quart = (normal_tempo / metrum)

    #Rastererstellung:
    grid_value = (first_quart / quantize_note)

    return grid_value


def read_listtxt_to_list(filename):
     newlist = []
     lines = [line.rstrip('\n') for line in open(filename)]
     for i in lines:
          newlist.append(ast.literal_eval(i))
     return(newlist)


def seperate_time_and_hand(filename):
    list_content = read_listtxt_to_list(filename)
    list_only_time = []
    list_only_hands = []

    for i in list_content:
        list_only_hands.append(i[0])
        list_only_time.append(i[1])
    return(list_only_time, list_only_hands)

def work(input_tempo, input_which_quantization, sourcefile, outputfile):
    #erster Viertel:
    grid_value = grid_intervall(input_tempo, input_which_quantization)
    midiinputs, only_hands = seperate_time_and_hand(sourcefile)

    grid_list = []
    last_item = midiinputs[-1]
    list_start_value = 0

    last_item_rounded_up = math.ceil(last_item) #für grösse/länge des grids

    range_of_grid = int(last_item_rounded_up/grid_value)

    # Liste für Raster
    for i in range(range_of_grid+1):
        grid_list.append(list_start_value)
        list_start_value += grid_value

    # -------------- Quantisierung --------------
    deltalist = []
    quantized = []

    for i in midiinputs:
        for j in grid_list:
            deltalist.append(abs(i-j))
        quantized_index = deltalist.index(min(deltalist))
        quantized.append(grid_list[quantized_index])
        deltalist.clear()

    only_hands_and_time_quanized = []
    zwischenlist = []

    for f, b in zip(only_hands, quantized):
        zwischenlist = [f,b]
        only_hands_and_time_quanized.append(zwischenlist)

    # unflatten list and write it: [4, 5, 6] to [[4], [5], [6]]
    with open(outputfile, 'w') as f:
        for item in only_hands_and_time_quanized:
            f.write("%s\n" % item)
