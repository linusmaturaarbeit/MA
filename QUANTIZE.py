import math
import itertools
import ast
import math
from operator import itemgetter

givequantizedfilename ="quantized_midinotes.txt"

# #statische Variable:
# normal_tempo = 60

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

#variable Tempo
def work(input_tempo, input_which_quantization, sourcefile, outputfile):
    # print(sourcefile)

    #erster Viertel:
    grid_value = grid_intervall(input_tempo, input_which_quantization)


    # -------------- Ab hier nur grid_value nötig --------------
    # midiinputs_raw = read_listtxt_to_list(sourcefile) #format: [[0.00], [0.50], [1.00]]
    #midiinputs = list(itertools.chain(*midiinputs_raw)) #flatting list : [0.00, 0.50, 1.00]

    midiinputs, only_hands = seperate_time_and_hand(sourcefile)


    grid_list = []
    last_item = midiinputs[-1]
    list_start_value = 0

    last_item_rounded_up = math.ceil(last_item) #für grösse/länge des grids

    range_of_grid = int(last_item_rounded_up/grid_value)
    #Bsp: 3viertel, auf 1/16 quan. --> 12er Raster

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
        #print(deltalist)
        quantized_index = deltalist.index(min(deltalist))
        #print(quantized_index)
        quantized.append(grid_list[quantized_index])
        deltalist.clear()

    #quantisierung wurde vorgenommen


    #Jetzt die Listen zusammenbringen
    #Ziel:   [[0,0],[1,0.5],[0,1],[1,1.5],[0,2]]        wären achtel rechts links, funf stück

    # print(quantized)
    # print("--------------------")
    # print(only_hands)

    only_hands_and_time_quanized = []
    zwischenlist = []

    for f, b in zip(only_hands, quantized):
        zwischenlist = [f,b]
        only_hands_and_time_quanized.append(zwischenlist)



    #
    # unflatten list and write it: [4, 5, 6] to [[4], [5], [6]]
    with open(outputfile, 'w') as f:
        for item in only_hands_and_time_quanized:
            f.write("%s\n" % item)

# only_time, only_hands = seperate_time_and_hand("I_2019.08.14-16.47.16.txt")
# print(only_time)
# print("-------------------")
# print(only_hands)
