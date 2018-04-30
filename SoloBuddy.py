"""Synthesizes a blues solo algorithmically."""

import atexit
import os
import sys
import pygame
import time
import math
import numpy as np
from random import choice
from pygame.locals import *
from psonic import *
from MenuBackStuff import PopupMenu

# The sample directory is relative to this source file's directory.
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "C3_chords")

SAMPLE_NOTE_FILE = os.path.join(SAMPLES_DIR, "bass_D2.wav")
SAMPLE_NOTE = D2  # the sample file plays at this pitch

SAMPLE_CHORD_FILE = os.path.join(SAMPLES_DIR, "major.wav")
SAMPLE_CHORD = C3

progname = sys.argv[0]
progdir = os.path.dirname(progname)
sys.path.append(os.path.join(progdir,'gamelib'))

chords = {}

important_notes = {"major":(0,4,7), "minor":(0,3,7), "major7":(0,4,7,11), "minor7":(0,3,7,10)}

menu_data = (
    'Roots',
    (
        'Ab',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    (
        'A',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    (
        'A#',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    (
        'Bb',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    (
        'B',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    (
        'C',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    (
        'C#',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    (
        'Db',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    (
        'D',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    (
        'D#',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    (
        'Eb',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    (
        'E',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    (
        'F',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    (
        'F#',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    (
        'Gb',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    (
        'G',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    (
        'G#',
        'major',
        'minor',
        'major7',
        'minor7',
    ),
    'Quit',
)

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

        # size of the cells in the button panel
        self.cell_width = self.window_width/5
        self.cell_height = self.window_height/12

    def draw_imp_notes(self, i):
        """
        Draws the current chord name and important notes in the bottom section of the screen.
        """

        # For the current chord
        # Display the name of the chord
        message1 = self.progression.chord2str(self.progression.chord_list[i])
        text1 = pygame.font.Font(None, 100).render(message1, 1, (0,0,0))
        self.display_surf.blit(text1, (self.window_width/6-text1.get_width()/2,self.window_height*13/16-text1.get_height()/2))

        # Display the most important notes
        message2 = get_important_notes(self.progression.chord_list[i])
        text2 = pygame.font.Font(None, 100).render(message2, 1, (0,0,0))
        self.display_surf.blit(text2, (self.window_width*3/4-text2.get_width()/2,self.window_height*13/16-text2.get_height()/2))

        # For the next chord
        if i+1 == self.progression.length():
            i = 0 # So that it loops back around
        else:
            i += 1

        message3 = self.progression.chord2str(self.progression.chord_list[i])
        text3 = pygame.font.Font(None, 50).render(message3, 1, (0,0,0))
        self.display_surf.blit(text3, (self.window_width/6-text3.get_width()/2,self.window_height*15/16-text3.get_height()/2))

        # Display the most important notes
        message4 = get_important_notes(self.progression.chord_list[i])
        text4 = pygame.font.Font(None, 50).render(message4, 1, (0,0,0))
        self.display_surf.blit(text4, (self.window_width*3/4-text4.get_width()/2,self.window_height*15/16-text4.get_height()/2))

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
                chord_message = "{} {}".format(self.progression.chord_list[chord_idx][0], self.progression.chord_list[chord_idx][1])
                chord_text = pygame.font.Font(None, 30).render(chord_message, 1, (0,0,0))
                self.display_surf.blit(chord_text, (x-(meas_length+chord_text.get_width())/2, y-bar_height/5))
                self.progression.chord_pos[chord_idx] = (\
                    x-(meas_length+chord_text.get_width())/2,\
                    y-bar_height/5,\
                    x-(meas_length-chord_text.get_width())/2,\
                    y-bar_height/5+chord_text.get_height())

                # self.display_surf.blit(chord_text, (x-meas_length/2-chord_text.get_width()/2,y-bar_height/5)) # Chord labels

                for k in range(hashes): # k is the hash (beat) within that measure
                    hashspace = meas_length/hashes
                    x2 = x - meas_length+ hashspace*(k + 0.5)
                    pygame.draw.line(self.display_surf, (0,0,0), (x2+10,y-bar_height/12),(x2-10,y+bar_height/12),4) # the hashes

    def draw_buttons(self):
        """
        Fills the top section of the screen with the buttons to change the settings.
        """
        # All cell counts are 0.5 lower to put text in center of cell.
        pause_message = "PAUSE/PLAY"
        pause_text = pygame.font.Font(None, 50).render(pause_message, 1, (0,0,0))
        self.display_surf.blit(pause_text, (self.cell_width*2.5-pause_text.get_width()/2,self.cell_height*1.5-pause_text.get_height()/2))

        reset_message = "RESET"
        reset_text = pygame.font.Font(None, 50).render(reset_message, 1, (0,0,0))
        self.display_surf.blit(reset_text, (self.cell_width*2.5-reset_text.get_width()/2,self.cell_height*2.5-reset_text.get_height()/2))

        slow_message = "SLOWER"
        slow_text = pygame.font.Font(None, 50).render(slow_message, 1, (0,0,0))
        self.display_surf.blit(slow_text, (self.cell_width*0.5-slow_text.get_width()/2,self.cell_height*1.5-slow_text.get_height()/2))

        fast_message = "FASTER"
        fast_text = pygame.font.Font(None, 50).render(fast_message, 1, (0,0,0))
        self.display_surf.blit(fast_text, (self.cell_width*1.5-fast_text.get_width()/2,self.cell_height*1.5-fast_text.get_height()/2))

        next_message = "NEXT"
        next_text = pygame.font.Font(None, 50).render(next_message, 1, (0,0,0))
        self.display_surf.blit(next_text, (self.cell_width*3.5-next_text.get_width()/2,self.cell_height*2.5-next_text.get_height()/2))

        last_message = "LAST"
        last_text = pygame.font.Font(None, 50).render(last_message, 1, (0,0,0))
        self.display_surf.blit(last_text, (self.cell_width*1.5-last_text.get_width()/2,self.cell_height*2.5-last_text.get_height()/2))

        bpm_message = "BPM = {}".format(self.bpm)
        bpm_text = pygame.font.Font(None, 50).render(bpm_message, 1, (0,0,0))
        self.display_surf.blit(bpm_text, (self.cell_width*1-bpm_text.get_width()/2,self.cell_height*0.5-bpm_text.get_height()/2))

        add_message = "ADD MEAS."
        add_text = pygame.font.Font(None, 50).render(add_message, 1, (0,0,0))
        self.display_surf.blit(add_text, (self.cell_width*3.5-add_text.get_width()/2,self.cell_height*1.5-add_text.get_height()/2))

        del_message = "DEL. MEAS."
        del_text = pygame.font.Font(None, 50).render(del_message, 1, (0,0,0))
        self.display_surf.blit(del_text, (self.cell_width*4.5-del_text.get_width()/2,self.cell_height*1.5-del_text.get_height()/2))

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
        bpm_entry = "{}".format(self.bpm)

        # Flags to avoid having the same button detected twice when it is held.
        space_pressed = False
        r_pressed = False
        back_pressed = False
        next_pressed = False
        add_pressed = False
        subtract_pressed = False
        f_pressed = False
        s_pressed = False
        flag = False #Indicates that we have exited the regular time loop
        bpm_text_active = False
        while self.running:
            # While loop instead of a for loop, because the chords run on a timer,
            # so each chord plays through multiple cycles of the loop.
            if i >= self.progression.length():
                i = 0 # Loop back to the top of the progression
            elif i < 0:
                i = 0

            pygame.event.pump()

            # Detects exit button to close program.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                elif event.type == MOUSEBUTTONUP:
                    chosen_chord = 0
                    if (self.cell_width*2 < pygame.mouse.get_pos()[0] < self.cell_width*3 and self.cell_height*1 < pygame.mouse.get_pos()[1] < self.cell_height*2):
                        if self.paused:
                            print("Unpaused")
                            self.paused = False
                            flag = True
                        else:
                            print("Paused")
                            self.paused = True
                    elif (self.cell_width*2 < pygame.mouse.get_pos()[0] < self.cell_width*3 and self.cell_height*2 < pygame.mouse.get_pos()[1] < self.cell_height*3):
                        i = 0
                        elapsed = 0
                    elif (self.cell_width*0 < pygame.mouse.get_pos()[0] < self.cell_width*1 and self.cell_height*1 < pygame.mouse.get_pos()[1] < self.cell_height*2):
                        self.bpm -= 10
                        print("bpm = {}".format(self.bpm))
                    elif (self.cell_width*1 < pygame.mouse.get_pos()[0] < self.cell_width*2 and self.cell_height*1 < pygame.mouse.get_pos()[1] < self.cell_height*2):
                        self.bpm += 10
                        print("bpm = {}".format(self.bpm))
                    elif (self.cell_width*3 < pygame.mouse.get_pos()[0] < self.cell_width*4 and self.cell_height*2 < pygame.mouse.get_pos()[1] < self.cell_height*3):
                        flag = True
                    elif (self.cell_width*1 < pygame.mouse.get_pos()[0] < self.cell_width*2 and self.cell_height*2 < pygame.mouse.get_pos()[1] < self.cell_height*3):
                        i -= 2
                        flag = True
                    elif (self.cell_width*3 < pygame.mouse.get_pos()[0] < self.cell_width*4 and self.cell_height*1 < pygame.mouse.get_pos()[1] < self.cell_height*2):
                        self.progression.chord_list.append(("C","major"))
                        self.progression.chord_pos.append([0, 0, 0, 0])
                    elif (self.cell_width*4 < pygame.mouse.get_pos()[0] < self.cell_width*5 and self.cell_height*1 < pygame.mouse.get_pos()[1] < self.cell_height*2):
                        self.progression.chord_list = self.progression.chord_list[:-1]
                        self.progression.chord_pos = self.progression.chord_pos[:-1]
                    else:
                        try:
                            for label in range(len(self.progression.chord_pos)):
                                p1 = self.progression.chord_pos[label][0:2]
                                p2 = self.progression.chord_pos[label][2:4]
                                if (p1[0] < pygame.mouse.get_pos()[0] < p2[0] and p1[1] < pygame.mouse.get_pos()[1] < p2[1]):
                                    # Blocking popup menu.
                                    popup = PopupMenu(menu_data, pos = pygame.mouse.get_pos())
                                    chosen_chord = label
                        except: # To prevent it from crashing if a non-button is clicked
                            pass
                    # Check if text entry field is clicked.
                    if (self.cell_width*1.5 < pygame.mouse.get_pos()[0] < self.cell_width*2.5 and self.cell_height*1 < pygame.mouse.get_pos()[1] < self.cell_height*2):
                        bpm_text_active = not bpm_text_active
                    else:
                        bpm_text_active = False

                    if event.type == pygame.KEYDOWN:
                        if bpm_text_active:
                            if event.key == pygame.K_RETURN:
                                self.bpm = int(bpm_entry)
                            elif event.key == pygame.K_BACKSPACE:
                                bpm_entry = bpm_entry[:-1]
                            else:
                                bpm_entry += event.unicode

                elif event.type == USEREVENT:
                    if event.code == 'MENU':
                        self.progression.chord_list[chosen_chord] = handle_menu(event)
                        flag = True


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
                        flag = True
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
                    flag = True
            else:
                r_pressed = False

            if (keys[K_EQUALS]):
                if add_pressed == False:
                    add_pressed = True
                    self.progression.chord_list.append(("C","major"))
                    self.progression.chord_pos.append([0, 0, 0, 0])
            else:
                add_pressed = False

            if (keys[K_MINUS]):
                if subtract_pressed == False:
                    subtract_pressed = True
                    self.progression.chord_list = self.progression.chord_list[:-1]
                    self.progression.chord_pos = self.progression.chord_pos[:-1]
            else:
                subtract_pressed = False

            # F and S make the music faster or slower by increments of 10 self.bpm.
            if (keys[K_f]):
                if f_pressed == False:
                    f_pressed = True
                    self.bpm += 10
                    print("bpm = {}".format(self.bpm))
            else:
                f_pressed = False

            if (keys[K_s]):
                if s_pressed == False:
                    s_pressed = True
                    self.bpm -= 10
                    print("bpm = {}".format(self.bpm))
            else:
                s_pressed = False

            # This doesn't actually measure elapsed time, but instead measures
            # how close the elapsed time is to 1 measure.
            elapsed = abs(time.time() - last_time - (self.time_signature*60/self.bpm))

            if (keys[K_LEFT]):
                if back_pressed == False:
                    back_pressed = True
                    i -= 2
                    elapsed = 0
            else:
                back_pressed = False

            if (keys[K_RIGHT] or flag):
                if next_pressed == False:
                    next_pressed = True
                    elapsed = 0
                    flag = False
            else:
                next_pressed = False

            if ((self.paused == False) and (elapsed<0.1)):
                #If close to one measure has passed, play the next chord.
                play_chord(self.progression.chord_list[i][0],self.progression.chord_list[i][1], beats = self.time_signature, bpm=self.bpm)

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
        self.chord_pos = []
        for i in range(self.length()):
            self.chord_pos += (0, 0, 0, 0)
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
    """
    Plays a note given a pitch as a position on the piano.
    We don't actually ever call this, but we left it here
    because play_chord is based on it.
    """
    half_steps = note - SAMPLE_NOTE
    rate = (2 ** (1 / 12)) ** half_steps
    assert os.path.exists(SAMPLE_NOTE_FILE)

    sample(os.path.realpath(SAMPLE_NOTE_FILE), rate=rate, amp=amp)
    sleep(beats * 60 / bpm)

def play_chord(root, tonality, beats=4, bpm=120, amp=1):
    """Plays a chord defined by root note and tonality (i.e. major, minor)"""
    half_steps = note2steps(root) - 60
    rate = (2 ** (1/12)) ** half_steps

    sample(os.path.realpath(chords[tonality]), rate=rate, amp=amp)

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

def step2notes(notes, mode):
    """
    Takes an int that sonic pi can play and converts it to the corresponding note string.
    """
    all_notes = ["C","C#/Db","D","D#/Eb","E","F","F#/Gb","G","G#/Ab","A","A#/Bb","B"]
    pitches = []
    for i in notes:
            pitch = all_notes[i%12]
            # This if statement makes the notes display as "C#" or "Db" rather than "C#/Db"
            if len(pitch) == 1: # a natural note
                pitches.append(pitch)
            elif mode == 'flats': # and not a natural note
                pitches.append(pitch[3:5])
            else: # mode == 'sharps' and not a natural note
                pitches.append(pitch[0:2])
    return pitches

def get_important_notes(chord):
    """
    This finds the notes that will sound good over a certain chord
    and returns a string ready to be displayed.
    """
    root = note2steps(chord[0])
    # This if statement determines whether the notes should be displayed as sharps or flats.
    # If the root is sharp or flat, the mode of the notes matches.
    # If the root is natural, the notes are sharp unless the root is F.
    if len(chord[0]) == 2 and chord[0][1] == 'b': # If root is flat, display notes as flats
        mode = 'flats'
    elif chord[0] == 'F': # An exception to the naturals, because F is unusual
        mode =='flats'
    else: # If the chord is not flat, i.e. natural or sharp
        mode = 'sharps'
    imp_intervals = important_notes[chord[1]]
    imp_steps = []
    for i in imp_intervals:
        imp_steps.append(i + root)
    imp_notes = step2notes(imp_steps, mode)
    black_display = ""
    blue_display = ""
    for i in range(len(imp_notes)):
        if i == 0 or i == 2:
            black_display += imp_notes(i)
            black_display += "    "
            blue_display += "       "
        else:
            blue_display += imp_notes(i)
            blue_display += "     "
            black_display += "       "
    note_display = (black_display, blue_display)
    return note_display

def handle_menu(e):
    print('Menu event: %s.%d: %s' % (e.name,e.item_id,e.text))
    if e.name == 'Roots':
        if e.text == 'Quit':
            quit()
    else:
        return (e.name[0:-3],e.text)



atexit.register(stop)

make_chord_dict()

# play_chord('C','major')
window = Window(prog = ChordProgression(("C","major", 16)))

window.go()
