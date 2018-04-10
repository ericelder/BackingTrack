"""Synthesizes a blues solo algorithmically."""

import atexit
import os
import pygame
import time
from random import choice
from pygame.locals import *
from psonic import *

# The sample directory is relative to this source file's directory.
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "C3_chords")

SAMPLE_NOTE_FILE = os.path.join(SAMPLES_DIR, "bass_D2.wav")
SAMPLE_NOTE = D2  # the sample file plays at this pitch

SAMPLE_CHORD_FILE = os.path.join(SAMPLES_DIR, "major.wav")
SAMPLE_CHORD = C3

chords = {}

ImportantNotesDict = {"major":(0,4,7), "minor":(0,3,7), "major7":(0,4,7,11), "minor7":(0,3,7,10)}

class Window:
    """
    This is the window that contains the visual components and input for the app.
    """
    def __init__(self):
        self.running = True
        self.display_surf = None
        self.image_surf = None
        self.window_width = 900
        self.window_height = 900
        self.progression = ChordProgression(("C","major7"),("F","minor"),("G","major"),("D","minor7"))

    def go(self):
        """
        This is the main method that gets called to start the whole thing.
        """
        pygame.init() #Gets pygame going
        # display_surf and image_surf are also from a pygame tutorial
        self.display_surf = pygame.display.set_mode((self.window_width,self.window_height), pygame.HWSURFACE)
        self.running = True
        self.paused = False

        loc = 0

        while self.running:
            pygame.event.pump()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
            pygame.key.set_repeat(10000,1000)
            keys = pygame.key.get_pressed()

            if (keys[K_ESCAPE]):
                self.running = False
                pygame.quit()

            if (keys[K_SPACE]):
                self.paused = not self.paused
                print("Paused = {}".format(self.paused))

            if self.paused == False:
                play_chord(self.progression.chord_list[loc][0],self.progression.chord_list[loc][1])
                message1 = self.progression.chord2str(self.progression.chord_list[loc])
                font = pygame.font.Font(None, 24)
                text1 = font.render(message1, 1, (10,10,10))


                message2 = important_notes(self.progression.chord_list[loc])
                text2 = font.render(message2, 1, (10,10,10))

                board.fill ((250,250,250), (0,900,900,25))
                board.blit(text1, (10,900))
                board.blit(text2, (20,900))



                print(self.progression.chord2str(self.progression.chord_list[loc]))
                print(important_notes(self.progression.chord_list[loc]))

            pygame.display.flip()

class ChordProgression:
    """
    A chord in this program is a tuple of (root, tonality).
    The chord progression contains a list of chord tuples
    and methods to interact with that list.
    """
    def __init__(self, *chords):
        self.chord_list = []
        for i in chords:
            self.chord_list.append(i)
        # print(len(self.chord_list))

    def __str__(self):
        """
        Should read like "C major7     F minor     G major     A minor7"
        """
        self.printout = ""
        for i in self.chord_list:
            self.printout += self.chord2str(i)
            self.printout += "     "
        print(self.printout)

    def chord2str(self, chord):
        """
        Takes a chord tuple and turns it into a readable str, like "C major"
        """
        return "{} {}".format(chord[0], chord[1])


    def play(self, def_beats=4, def_bpm=120):
        """Plays the chords in the chord progression for 4 beats each"""

        for i in self.chord_list:
            play_chord(i[0],i[1], beats=def_beats,bpm=def_bpm)
            print(self.chord2str(i))
            print(important_notes(i))


def play_note(note, beats=1, bpm=60, amp=1):
    """Plays a note given a pitch as a position on the piano"""
    half_steps = note - SAMPLE_NOTE
    rate = (2 ** (1 / 12)) ** half_steps
    assert os.path.exists(SAMPLE_NOTE_FILE)

    sample(os.path.realpath(SAMPLE_NOTE_FILE), rate=rate, amp=amp)
    sleep(beats * 60 / bpm)

def play_chord(root, tonality, beats=4, bpm=120, amp=1):
    """Plays a chord defined by the Chord class"""
    half_steps = note2steps(root) - 60
    rate = (2 ** (1/12)) ** half_steps
    assert os.path.exists(chords[tonality])

    sample(os.path.realpath(chords[tonality]), rate=rate, amp=amp)
    sleep(beats * 120 / bpm)


def stop():
    """Stop all tracks."""
    msg = osc_message_builder.OscMessageBuilder(address='/stop-all-jobs')
    msg.add_arg('SONIC_PI_PYTHON')
    msg = msg.build()
    synth_server.client.send(msg)

def read_midi(filename):
    """
    We probably don't need this anymore.
    """
    pass

def make_chord_dict():
    """
    Creates a dictionary of .wav files print(chords)for each tonality of chord.
    """
    chord_types = ["major","minor","major7","minor7"]
    SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "C3_chords")
    for i in chord_types:
        chords[i] = os.path.join(SAMPLES_DIR, "{}.wav".format(i))

def note2steps(pitch):
    """
    Takes a pitch as a str ("Bb") and returns it as an integer that SonicPi can play.
    """
    white_keys = {'A':57, 'B':59, 'C':60, 'D':62, 'E':64, 'F':65, 'G':67}
    if len(pitch) == 1:
        modifier = 0
    elif pitch[1] == '#':
        modifier = 1
    elif pitch[1] == 'b':
        modifier = -1
    return (white_keys[pitch[0]]+modifier)

def step2notes(notes):
    """
    Takes an int that sonc pi can play and converts it to the corresponding note string.
    """
    all_notes = ["C","C#/Db","D","D#/Eb","E","F","F#/Gb","G","G#/Ab","A","A#/Bb","B"]
    pitches = []
    for i in notes:
        pitches.append(all_notes[i%12])
    return pitches

def important_notes(chord):
    root = note2steps(chord[0])
    imp_intervals = ImportantNotesDict[chord[1]]
    imp_steps = []
    for i in imp_intervals:
        imp_steps.append(i + root)
    imp_motes = (step2notes(imp_steps))
    note_display = ""
    for i in imp_motes:
        note_display += i
        note_display += "     "
    return note_display

atexit.register(stop)

make_chord_dict()

# play_note(60, 1, 60)

#play_chord('A','minor7')
# play 60

# print(practiceChordProgression.chord2str(("D","minor")))

# print(note2steps('Eb'))

window = Window()
# practiceChordProgression = ChordProgression(("C","major7"),("F","minor"),("G","major"),("D","minor7"))
# print(practiceChordProgression)
# practiceChordProgression.play()
window.go()
