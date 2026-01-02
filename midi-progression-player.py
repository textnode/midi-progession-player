# Copyright 2025 Darren Elwood <darren@textnode.com> http://www.textnode.com @textnode
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at 
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mido

import time
import pprint
import itertools

chromatic_notes = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']
chromatic_loop = itertools.cycle(chromatic_notes)

midi_notes = list(zip(range(128), chromatic_loop))

major_intervals = [2,2,1,2,2,2,1]

def select_using_intervals(interval_input):
    selector = [1] #tonic
    intervals = iter(itertools.chain(interval_input * 10))
    for interval in intervals:
        for i in range(interval-1):
            selector.append(0)
        selector.append(1)
    return selector

def flatten_midi_note(midi_note_to_flatten):
    reversed_midi_notes = reversed(midi_notes)
    starting_point = itertools.dropwhile(lambda note: note != midi_note_to_flatten, reversed_midi_notes)
    next(starting_point)
    return(next(starting_point))

def sharpen_midi_note(midi_note_to_sharpen):
    starting_point = itertools.dropwhile(lambda note: note != midi_note_to_sharpen, midi_notes)
    next(starting_point)
    return(next(starting_point))

def flatten_chromatic_note(chromatic_note_to_flatten):
    reversed_chromatic_notes = reversed(chromatic_notes * 2)
    starting_point = itertools.dropwhile(lambda note: note != chromatic_note_to_flatten, reversed_chromatic_notes)
    next(starting_point)
    return(next(starting_point))



def build_scale(intervals, tonic):
    selector = select_using_intervals(intervals)
    starting_point = itertools.dropwhile(lambda note: note != tonic, iter(chromatic_notes))
    diatonic_notes = list(itertools.compress(starting_point, selector))
    return diatonic_notes


def build_chord(tonic, intervals, notes, octave):
    selector = select_using_intervals(intervals)
    starting_point = itertools.dropwhile(lambda note: note[1] != tonic, iter(midi_notes))
    for i in range(octave):
        next(starting_point)
        starting_point = itertools.dropwhile(lambda note: note[1] != tonic, starting_point)

    diatonic_notes = list(itertools.compress(starting_point, selector))

    notes_to_play = []
    for chord_note in notes:
        position = int(chord_note[-1])
        midi_note = (diatonic_notes[position-1])
        if chord_note[0] == 'b':
           notes_to_play.append(flatten_midi_note(midi_note))
        elif chord_note[0] == '#':
           notes_to_play.append(sharpen_midi_note(midi_note))
        else:
           notes_to_play.append(midi_note)

    return notes_to_play

def play_chord(port, tonic, intervals, chord):
    [chord_tonic, notes] = notation[chord]
    notes_to_play = build_chord(chord_tonic, intervals, notes, 4)
    print("%s %s, chord: %s notes:%s" % (tonic, intervals, chord, notes_to_play))
    for note_to_play in notes_to_play:
        msg = mido.Message("note_on", note=note_to_play[0])
        outport.send(msg)
    time.sleep(2)
    for note_to_stop in notes_to_play:
        msg = mido.Message("note_off", note=note_to_stop[0])
        outport.send(msg)
    time.sleep(0.5)

def add_notations_for(notations, root, degree_modifier):
    major = ['1','3','5']
    maj6 = ['1','3','5','6']
    dom7 = ['1','3','5','b7']
    maj7 = ['1','3','5','7']
    maj9 = ['1','3','5','7','9']
    aug = ['1', '3', '#5']
    aug7 = ['1', '3', '#5', '7']

    minor = ['1','b3','5']
    min6 = ['1','b3','5','6']
    min7 = ['1','b3','5','b7']
    min9 = ['1','b3','5','b7','9']

    sus2 = ['1','2','5']
    sus4 = ['1','4','5']

    notation[degree_modifier + major_degrees[index]] = [root, major]
    notation[degree_modifier + major_degrees[index] + '6'] = [root, maj6]
    notation[degree_modifier + major_degrees[index] + '7'] = [root, dom7]
    notation[degree_modifier + major_degrees[index] + 'M7'] = [root, maj7]
    notation[degree_modifier + major_degrees[index] + '9'] = [root, maj9]
    notation[degree_modifier + major_degrees[index] + '+'] = [root, aug]
    notation[degree_modifier + major_degrees[index] + '+7'] = [root, aug7]

    notation[degree_modifier + minor_degrees[index]] = [root, minor]
    notation[degree_modifier + minor_degrees[index] + '6'] = [root, min6]
    notation[degree_modifier + minor_degrees[index] + '7'] = [root, min7]
    notation[degree_modifier + minor_degrees[index] + '9'] = [root, min9]

    notation[degree_modifier + major_degrees[index] + 'sus2'] = [root, sus2]
    notation[degree_modifier + minor_degrees[index] + 'sus2'] = [root, sus2]

    notation[degree_modifier + major_degrees[index] + 'sus4'] = [root, sus4]
    notation[degree_modifier + minor_degrees[index] + 'sus4'] = [root, sus4]

with mido.open_output('Gen', virtual=True) as outport:
    user_data = input("Enter root (e.g. C) and press <Enter>...")
    fields = user_data.split(' ')

    tonic = fields[0]

    intervals = major_intervals
    diatonic_scale = build_scale(intervals, tonic)

    print(diatonic_scale)

    notation = {}

    major_degrees = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
    minor_degrees = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']


    for index, root in enumerate(diatonic_scale):
        add_notations_for(notation, root, "")
        flattened = flatten_chromatic_note(root)
        add_notations_for(notation, flattened, "b")

    pprint.pp(notation)

    canned = [
"i bVII v bVI",
"i bIII bVII IV",
"I vi III IV",
"bVI V i",
"I IV bVII bVI I",
"iv7 bVII7 I",
"I I7 IV iv",
"I ii vi IV",
"I III IV iv",
"I V vi IV",
"vi IV I V",
"i bVII bVI V",
"i bIII IV bVI",
"bVI bVII i i",
"I III vi V IV iv",
"I V vi IV"]


    while True:
        response = input("Enter canned numbers and/or notation (e.g. ii) and press <Enter> to continue...")
        choices = response.split()
        print(choices)

        while True:
            for choice in choices:
                try:
                    canned_index = int(choice)
                except ValueError:
                    chord = choice
                    play_chord(outport, tonic, intervals, choice)
                else:
                    for chord in canned[canned_index].split():
                        play_chord(outport, tonic, intervals, chord)


