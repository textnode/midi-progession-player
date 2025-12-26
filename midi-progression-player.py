// Copyright 2025 Darren Elwood <darren@textnode.com> http://www.textnode.com @textnode
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import mido

import pprint
import itertools

chromatic_notes = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']
chromatic_loop = itertools.cycle(chromatic_notes)

midi_notes = list(zip(range(128), chromatic_loop))

major_intervals = [2,2,1,2,2,2,1]
natural_minor_intervals = [2,1,2,2,1,2,2]


def select_using_intervals(interval_input):
    selector = [1] #tonic
    intervals = iter(itertools.chain(interval_input * 10))
    for interval in intervals:
        for i in range(interval-1):
            selector.append(0)
        selector.append(1)
    return selector

def flatten_midi_note(midi_note):
    reversed_midi_notes = reversed(midi_notes)
    starting_point = itertools.dropwhile(lambda note: note != midi_note, reversed_midi_notes)
    return(next(starting_point))

def flatten_chromatic_note(note_to_flatten):
    reversed_chromatic_notes = reversed(chromatic_notes * 2)
    starting_point = itertools.dropwhile(lambda note: note != note_to_flatten, reversed_chromatic_notes)
    next(starting_point)
    return(next(starting_point))

def sharpen_chromatic_note(note_to_sharpen):
    forward_chromatic_notes = iter(chromatic_notes * 2)
    starting_point = itertools.dropwhile(lambda note: note != note_to_sharpen, forward_chromatic_notes)
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
        if chord_note[0] != 'b':
           notes_to_play.append(midi_note)
        else:
           notes_to_play.append(flatten_midi_note(midi_note))

    return notes_to_play


def add_notations_for(notations, root, degree_modifier):
    major = ['1','3','5']
    maj6 = ['1','3','5','6']
    dom7 = ['1','3','5','b7']
    maj7 = ['1','3','5','7']
    maj9 = ['1','3','5','7','9']

    minor = ['1','b3','5']
    min6 = ['1','b3','5','6']
    min7 = ['1','b3','5','b7']
    min9 = ['1','b3','5','b7', '9']

    chords = {'M': major, 'M6': maj6, 'M7': maj7, 'M9': maj9, 'm': minor, 'm6': min6, 'm7': min7, 'm9': min9, '7': dom7}

    notation[degree_modifier + major_degrees[index]] = [root, chords['M']]
    notation[degree_modifier + major_degrees[index] + '6'] = [root, chords['M6']]
    notation[degree_modifier + major_degrees[index] + '7'] = [root, chords['7']]
    notation[degree_modifier + major_degrees[index] + 'M7'] = [root, chords['M7']]
    notation[degree_modifier + major_degrees[index] + 'm7'] = [root, chords['m7']]
    notation[degree_modifier + major_degrees[index] + '9'] = [root, chords['M9']]

    notation[degree_modifier + minor_degrees[index]] = [root, chords['m']]
    notation[degree_modifier + major_degrees[index] + 'm6'] = [root, chords['m6']]
    notation[degree_modifier + major_degrees[index] + 'm9'] = [root, chords['m9']]

with mido.open_output('Gen', virtual=True) as outport:
    user_data = input("Enter root and quality (e.g. C m) and press <Enter>...")
    fields = user_data.split(' ')

    tonic = fields[0]

    interval_data = fields[1]
    intervals = major_intervals
    if interval_data == 'm':
        intervals = natural_minor_intervals

    diatonic_scale = build_scale(intervals, tonic)

    print(diatonic_scale)

    notation = {}

    major_degrees = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
    minor_degrees = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']


    for index, root in enumerate(diatonic_scale):
        add_notations_for(notation, root, "")
        flattened = flatten_chromatic_note(root)
        add_notations_for(notation, flattened, "b")
        sharpened = sharpen_chromatic_note(root)
        add_notations_for(notation, sharpened, "#")

    pprint.pp(notation)


    while True:
        response = input("Enter notation (e.g. ii) and press <Enter> to continue...")
        chords = response.split()
        print(chords)

        for chord in chords:
            [chord_tonic, notes] = notation[chord]
            notes_to_play = build_chord(chord_tonic, intervals, notes, 4)
            print("%s %s, chord: %s notes:%s" % (tonic, interval_data, chord, notes_to_play))
            for note_to_play in notes_to_play:
                msg = mido.Message("note_on", note=note_to_play[0])
                outport.send(msg)
            more = input("stop")
            for note_to_stop in notes_to_play:
                msg = mido.Message("note_off", note=note_to_stop[0])
                outport.send(msg)


