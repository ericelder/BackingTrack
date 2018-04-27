"""Synthesizes a blues solo algorithmically."""

import atexit
import os
import pygame
import time
import math
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

important_notes = {"major":(0,4,7), "minor":(0,3,7), "major7":(0,4,7,11), "minor7":(0,3,7,10)}

class Window:
    """
    This is the window that contains the visual components and input for the app.
    """
    def __init__(self, prog):
        self.running = True
        self.display_surf = None
        self.image_surf = None
        self.window_width = 1200
        self.window_height = 900
        self.progression = prog

    def draw_measures(self, hashes, measures):
        """
        This draws the measures with a certain number of hashes.
        """
        num_lines = math.ceil(measures/8)
        bar_height = self.window_height/2/num_lines
        for i in range(num_lines):
            if i+1 == num_lines and measures%8 != 0:
                meas = measures%8
            else:
                meas = 8
            y = self.window_height/4 + bar_height*(i + 0.5)
            pygame.draw.line(self.display_surf, (100,100,255), (0,y),(self.window_width,y),10)
            pygame.draw.line(self.display_surf, (0,0,0), (20,y-bar_height/3),(20,y+bar_height/3),5)
            for j in range(meas):
                meas_length = (self.window_width-40)/meas
                x = 20 + meas_length*(j+1)
                pygame.draw.line(self.display_surf, (0,0,0), (x,y-bar_height/4),(x,y+bar_height/5),5)

                chord_idx = i*8+j
                chord_message = "{} {}".format(self.progression.chord_list[chord_idx][0],self.progression.chord_list[chord_idx][1])
                chord_text = pygame.font.Font(None, 25).render(chord_message, 1, (0,0,0))
                self.display_surf.blit(chord_text, (x-meas_length/2-chord_text.get_width()/2,y-bar_height/3))

                for k in range(hashes):
                    hashspace = meas_length/hashes
                    x2 = x - meas_length+ hashspace*(k + 0.5)
                    pygame.draw.line(self.display_surf, (0,0,0), (x2+10,y-bar_height/6),(x2-10,y+bar_height/6),2)



    def go(self):
        """
        This is the main method that gets called to start the whole thing.
        """
        pygame.init() #Gets pygame going
        # display_surf and image_surf are also from a pygame tutorial
        self.display_surf = pygame.display.set_mode((self.window_width,self.window_height), pygame.HWSURFACE)
        self.running = True
        self.paused = False
        i = 0
        bpm = 120
        last_time = time.time()

        space_pressed = False
        r_pressed = False
        f_pressed = False
        s_pressed = False
        print(self.progression.chord_list)
        while self.running:
            if i >= self.progression.length():
                i = 0

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
                if space_pressed == False:
                    space_pressed = True
                    if self.paused:
                        print("Unpaused")
                        self.paused = False
                    else:
                        print("Paused")
                        self.paused = True
            else:
                space_pressed = False

            if (keys[K_r]):
                if r_pressed == False:
                    r_pressed = True
                    i = 0
            else:
                r_pressed = False

            if (keys[K_f]):
                if f_pressed == False:
                    f_pressed = True
                    bpm += 10
                    print("BPM = {}".format(bpm))
            else:
                f_pressed = False

            if (keys[K_s]):
                if s_pressed == False:
                    s_pressed = True
                    bpm -= 10
                    print("BPM = {}".format(bpm))
            else:
                s_pressed = False

            elapsed = abs(time.time() - last_time - (4*60/bpm))

            if ((self.paused == False) and (elapsed<0.1)): # 4 is a hardcoded number of beats
                play_chord(self.progression.chord_list[i][0],self.progression.chord_list[i][1], bpm=bpm)

                message1 = self.progression.chord2str(self.progression.chord_list[i])
                font = pygame.font.Font(None, 100)
                text1 = font.render(message1, 1, (0,0,0))

                message2 = get_important_notes(self.progression.chord_list[i])
                text2 = font.render(message2, 1, (0,0,0))

                self.display_surf.fill ((250,250,255))
                self.display_surf.blit(text1, (self.window_width/6-text1.get_width()/2,self.window_height*7/8-text1.get_height()/2))
                self.display_surf.blit(text2, (self.window_width*3/4-text2.get_width()/2,self.window_height*7/8-text2.get_height()/2))
                pygame.draw.line(self.display_surf, (0,0,0), (0,self.window_height*3/4),(self.window_width,self.window_height*3/4),5)
                pygame.draw.line(self.display_surf, (0,0,0), (0,self.window_height/4),(self.window_width,self.window_height/4),5)

                message3 = "Here we will put some buttons"
                text3 = pygame.font.Font(None, 50).render(message3, 1, (0,0,0))
                self.display_surf.blit(text3, (self.window_width/2-text3.get_width()/2,self.window_height/8-text3.get_height()/2))
                self.draw_measures(4,12)

                print(self.progression.chord2str(self.progression.chord_list[i]))
                print(get_important_notes(self.progression.chord_list[i]))
                last_time = time.time()
                i += 1


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
        self.convert()
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

    def length(self):
        """
        A wrapper to more easily get the number of chords.
        """
        return len(self.chord_list)

    def convert(self):
        """
        This converts the progression from chord tuples of (root, tonality, duration)
        into a more parseable format of (root, tonality) with copies for the duration.
        """
        new_chord_list = []
        for i in self.chord_list:
            for j in range(i[2]):
                new_chord_list.append(i[0:2])
        self.chord_list = new_chord_list

def play_note(note, beats=1, bpm=60, amp=1):
    """Plays a note given a pitch as a position on the piano"""
    half_steps = note - SAMPLE_NOTE
    rate = (2 ** (1 / 12)) ** half_steps
    assert os.path.exists(SAMPLE_NOTE_FILE)

    sample(os.path.realpath(SAMPLE_NOTE_FILE), rate=rate, amp=amp)
    sleep(beats * 60 / bpm)

def play_chord(root, tonality, beats=4, bpm=120, amp=1):
    """Plays a chord defined by root note and tonality (i.e. major, minor)"""
    half_steps = note2steps(root) - 60
    rate = (2 ** (1/12)) ** half_steps
    assert os.path.exists(chords[tonality])

    sample(os.path.realpath(chords[tonality]), rate=rate, amp=amp)

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

def get_important_notes(chord):
    """
    This finds the notes that will sound good over a certain chord.
    """
    root = note2steps(chord[0])
    imp_intervals = important_notes[chord[1]]
    imp_steps = []
    for i in imp_intervals:
        imp_steps.append(i + root)
    imp_notes = (step2notes(imp_steps))
    note_display = ""
    for i in imp_notes:
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

# window = Window(prog = ChordProgression(("C","major7"),("F","minor"),("G","major"),("D","minor7")))
window = Window(prog = ChordProgression(("F","major", 3),("F","major7", 1),("Bb","major7", 2),("F","major", 2),("C","major7",1),("Bb","major7",1),("F","major",2)))
# practiceChordProgression = ChordProgression(("C","major7"),("F","minor"),("G","major"),("D","minor7"))
# print(practiceChordProgression)
# practiceChordProgression.play()
window.go()
