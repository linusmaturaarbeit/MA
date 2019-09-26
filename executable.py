#importiere die eigenen Module
import WINDOWS_VERSION
import QUANTIZE
import TEXT_TO_MIDI
#
import time
import subprocess

#Funktion für Filenames mit Zeitstempel
def return_filename(fname, format):
    timestamp = time.strftime("%Y.%m.%d-%H.%M.%S")
    return "%s%s.%s" %(fname,timestamp, format)


#Midi-Input Filename
midi_input_filename = "I_"
midi_input_filename_timestamped = return_filename(midi_input_filename, "txt")

#Midi-Quantisiert Filename
midi_quantized_filename = "Q_"
midi_quantized_filename_timestamped = return_filename(midi_quantized_filename, "txt")

#Midi-File Filename
midi_generated_filename = "M_"
midi_generated_filename_timestamped = return_filename(midi_generated_filename, "mid")

pdf_generated_filename = "PDF_"
pdf_generated_filename_timestamped = return_filename(pdf_generated_filename, "pdf")

#WINDOWS_VERSION
try:
    WINDOWS_VERSION.work(midi_input_filename_timestamped)
except KeyboardInterrupt:
    print("quit recording\n")
except NameError:
    print("BopPad is not connected")


#QUANTIZE
input_tempo = int(input("Tempo: "))
input_which_quantization = input("Quantisierung auf 1/4=1, 1/8=2, 1/12=3, 1/16=4, 1/24=6, 1/32=8:")
QUANTIZE.work(input_tempo, input_which_quantization,  midi_input_filename_timestamped, midi_quantized_filename_timestamped)


#TEXT_TO_MIDI
TEXT_TO_MIDI.work(midi_quantized_filename_timestamped, midi_generated_filename_timestamped, input_tempo)
#print("\nMIDI-File generated under the name: '%s'" %(midi_generated_filename_timestamped))
#
#
#MIDI_TO_PDF
command = 'MuseScore3.exe -o "%s" "%s"' % (pdf_generated_filename_timestamped, midi_generated_filename_timestamped)
subprocess.run(command)
print("\nPDF-File generated under the name: '%s'" %(pdf_generated_filename_timestamped))
