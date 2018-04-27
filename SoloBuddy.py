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

    def draw_imp_notes(self, i):
        """
        Draws the current chord name and important notes in the bottom section of the screen.
        """
        #Display the name of the chord
        message1 = self.progression.chord2str(self.progression.chord_list[i])
        text1 = pygame.font.Font(None, 100).render(message1, 1, (0,0,0))
        self.display_surf.blit(text1, (self.window_width/6-text1.get_width()/2,self.window_height*7/8-text1.get_height()/2))

        # Display the most important notes
        message2 = get_important_notes(self.progression.chord_list[i])
        text2 = pygame.font.Font(None, 100).render(message2, 1, (0,0,0))
        self.display_surf.blit(text2, (self.window_width*3/4-text2.get_width()/2,self.window_height*7/8-text2.get_height()/2))

    def draw_measures(self, ind):
        """
        This draws the measures, hashes, and chord names in the middle section of the screen.
        It will separate the screen into measures, up to 8 per line, with hashes based on the
        time signature. It puts each chord name above the measure and highlights the current one.
        """
        measures = self.progression.length()
        hashes = self.time_signature
        num_lines = math.ceil(measures/8)
        bar_height = self.window_height/2/num_lines
        space_width = 5
        for i in range(num_lines): # i is the line number
            if i+1 == num_lines and measures%8 != 0:
                meas = measures%8
            else:
                meas = 8
            y = self.window_height/4 + bar_height*(i + 0.5)
            pygame.draw.line(self.display_surf, (0,0,0), (20,y-bar_height/6),(20,y+bar_height/6),6) # at start of line
            for j in range(meas): # j is the measure within that line
                meas_length = (self.window_width-40)/meas
                x = 20 + meas_length*(j+1)
                if (i*8+j == ind):
                    pygame.draw.line(self.display_surf, (255,255,0), (x-meas_length+3,y),(x-3,y),50) # the highlight
                pygame.draw.line(self.display_surf, (0,0,0), (x,y-bar_height/6),(x,y+bar_height/6),6) # barlines between measures


                chord_idx = i*8+j
                # The root and tonality of the chord are displayed separately to faciltate click detection.
                chord_root_message = self.progression.chord_list[chord_idx][0]
                chord_tonality_message = self.progression.chord_list[chord_idx][1]
                chord_root_text = pygame.font.Font(None, 30).render(chord_root_message, 1, (0,0,0))
                chord_tonality_text = pygame.font.Font(None, 30).render(chord_tonality_message, 1, (0,0,0))
                self.display_surf.blit(chord_root_text, (x-(meas_length+chord_root_text.get_width()+space_width+chord_tonality_text.get_width())/2, y-bar_height/5))
                self.display_surf.blit(chord_tonality_text, (x-(meas_length-chord_root_text.get_width()-space_width+chord_tonality_text.get_width())/2, y-bar_height/5))

                # self.display_surf.blit(chord_text, (x-meas_length/2-chord_text.get_width()/2,y-bar_height/5)) # Chord labels

                for k in range(hashes): # k is the hash (beat) within that measure
                    hashspace = meas_length/hashes
                    x2 = x - meas_length+ hashspace*(k + 0.5)
                    pygame.draw.line(self.display_surf, (0,0,0), (x2+10,y-bar_height/12),(x2-10,y+bar_height/12),4) # the hashes

    def draw_buttons(self):
        """
        Fills the top section of the screen with the buttons to change the settings.
        """
        message3 = "Here we will put some buttons"
        text3 = pygame.font.Font(None, 50).render(message3, 1, (0,0,0))
        self.display_surf.blit(text3, (self.window_width/2-text3.get_width()/2,self.window_height/8-text3.get_height()/2))


    def go(self):
        """
        This is the main method that gets called to start the whole thing.
        It has a continuous loop that listens for user input via keys, and
        also plays the chord progression. The chord progression plays based
        on a timer, so it and the key listener do not delay each other.
        """
        pygame.init() #Gets pygame going
        # display_surf and image_surf are also from a pygame tutorial
        self.display_surf = pygame.display.set_mode((self.window_width,self.window_height), pygame.HWSURFACE)
        # Running is if the code is running, paused measures if it is acutally playing.
        self.running = True
        self.paused = False
        i = 0 # The index of where we are in the chord progression.
        self.bpm = 120
        self.time_signature = 4 # We only care about the top of the time signature
        last_time = time.time() # Start the timer.

        # Flags to avoid having the same button detected twice when it is held.
        space_pressed = False
        r_pressed = False
        f_pressed = False
        s_pressed = False
        while self.running:
            # While loop instead of a for loop, because the chords run on a timer,
            # so each chord plays through multiple cycles of the loop.
            if i >= self.progression.length():
                i = 0

            pygame.event.pump()

            # Detects exit button to close program.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
            pygame.key.set_repeat(10000,1000)
            keys = pygame.key.get_pressed()

            # Detects escape button to close program.
            if (keys[K_ESCAPE]):
                self.running = False
                pygame.quit()

            # Space bar toggles pause and play.
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

            # Takes i, the index of the chord progression, back to the top.
            if (keys[K_r]):
                if r_pressed == False:
                    r_pressed = True
                    i = 0
            else:
                r_pressed = False

            # F and S make the music faster or slower by increments of 10 self.bpm.
            if (keys[K_f]):
                if f_pressed == False:
                    f_pressed = True
                    self.bpm += 10
                    print("self.bpm = {}".format(self.bpm))
            else:
                f_pressed = False

            if (keys[K_s]):
                if s_pressed == False:
                    s_pressed = True
                    self.bpm -= 10
                    print("self.bpm = {}".format(self.bpm))
            else:
                s_pressed = False

            # This doesn't actually measure elapsed time, but instead measures
            # how close the elapsed time is to 1 measure.
            elapsed = abs(time.time() - last_time - (self.time_signature*60/self.bpm))

            if ((self.paused == False) and (elapsed<0.1)):
                #If close to one measure has passed, play the next chord.
                play_chord(self.progression.chord_list[i][0],self.progression.chord_list[i][1], bpm=self.bpm)

                # Display boundaries between the sections of the screen
                self.display_surf.fill ((250,250,255))
                pygame.draw.line(self.display_surf, (0,0,0), (0,self.window_height*3/4),(self.window_width,self.window_height*3/4),5)
                pygame.draw.line(self.display_surf, (0,0,0), (0,self.window_height/4),(self.window_width,self.window_height/4),5)

                # Display each section of the screen
                self.draw_imp_notes(i) # Display bottom section of screen
                self.draw_measures(i) # Display middle section of screen
                self.draw_buttons() # Display top section of screen


                print(self.progression.chord2str(self.progression.chord_list[i]))
                print(get_important_notes(self.progression.chord_list[i]))

                # Update the clock, and move the chord index to the next chord.
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
    Takes an int that sonic pi can play and converts it to the corresponding note string.
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
