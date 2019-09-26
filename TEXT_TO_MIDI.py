#!/usr/bin/env python
import ast
from midiutil import MIDIFile
import time

def return_filename(fname, format):
    timestamp = time.strftime("%Y.%m.%d-%H.%M.%S")
    return "%s%s.%s" %(fname,timestamp, format)

# inputfile = "Q_2019.06.23-22.38.01.txt"
# givemidiname = return_filename("othertempo", "mid")


def read_listtxt_to_list(filename):
     newlist = []
     lines = [line.rstrip('\n') for line in open(filename)]
     for i in lines:
          newlist.append(ast.literal_eval(i))
     return(newlist)

# def seperate_time_and_hand(filename):
#     list_content = read_listtxt_to_list(filename)
#     list_only_hands = []
#     list_only_time_quantized = []
#
#
#     for i in list_content:
#         list_only_hands.append(i[0])
#         list_only_time_quantized.append(i[1])
#     return(list_only_time_quantized, list_only_hands)



def work(source, out, tempo):

    track    = 0    # Track numbers are zero-origined
    channel  = 0    # MIDI Channel
    time     = 0    # In beats
    duration = 2    # In beats
    #tempo    = 60   # In BPM
    volume   = 100  # 0-127, as per the MIDI standard
    #pitch    = 60   # MIDI note number

    midiinputs = read_listtxt_to_list(source)
    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created automatically)
    MyMIDI.addTempo(track, time, tempo)

    # midiinputs_quantized, hands = seperate_time_and_hand(source)

    # for i in midiinputs_quantized:
    #     time = i
    #     hand = hands[i]
    #     MyMIDI.addNote(track, channel, pitch, time, duration, volume)
    #     print(hand)
    #
    # with open(out, "wb") as output_file:
    #     MyMIDI.writeFile(output_file)

    for i in midiinputs:
        time = i[1]
        pitch = i[0]
        MyMIDI.addNote(track, channel, pitch, time, duration, volume)

    with open(out, "wb") as output_file:
        MyMIDI.writeFile(output_file)


    # l = [[0,4],[1,2]]
    # for i in l:
    #     hand = i[0]
    #     time = i[1]


# work("QQQ.txt", "yaasbitch.mid", 60)
