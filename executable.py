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

#importiere die eigenen Module
import MIDI_Instrument_Connection
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

#MIDI_Instrument_Connection
try:
    MIDI_Instrument_Connection.work(midi_input_filename_timestamped)
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

#MIDI_TO_PDF
#Linux Opensuse:    'musescore -o "%s" "%s"' % (pdf_generated_filename_timestamped, midi_generated_filename_timestamped)
#Windows 10    :    'MuseScore3.exe -o "%s" "%s"' % (pdf_generated_filename_timestamped, midi_generated_filename_timestamped)
command = 'MuseScore3.exe -o "%s" "%s"' % (pdf_generated_filename_timestamped, midi_generated_filename_timestamped)
subprocess.run(command)
print("\nPDF-File generated under the name: '%s'" %(pdf_generated_filename_timestamped))
