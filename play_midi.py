"""Synthesizes a blues solo algorithmically."""

import atexit
import os
from random import choice

from psonic import *

# The sample directory is relative to this source file's directory.
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")

SAMPLE_NOTE_FILE = os.path.join(SAMPLES_DIR, "bass_D2.wav")
SAMPLE_NOTE = D2  # the sample file plays at this pitch

SAMPLE_CHORD_FILE = os.path.join(SAMPLES_DIR, "chord_C3.wav")
SAMPLE_CHORD = C3


class Chord:
    def __init__(self, root, tonality):
        self.root = root
        self.tonality = tonality

    def __str__(self):
        print("{} {}".format(self.root, self.tonality))

class ChordProgression:
    def __init__(self, *chords):
        self.chords = []
        for i in chords:
            self.chords.append(i)

def play_note(note, beats=1, bpm=60, amp=1):
    """Plays a note given a pitch as a position on the piano"""
    half_steps = note - SAMPLE_NOTE
    rate = (2 ** (1 / 12)) ** half_steps
    assert os.path.exists(SAMPLE_NOTE_FILE)

    sample(os.path.realpath(SAMPLE_NOTE_FILE), rate=rate, amp=amp)
    sleep(beats * 60 / bpm)

def play_chord(chord, beats=4, bpm=60, amp=1):
    """Plays a chord defined by the Chord class"""
    half_steps = chord - SAMPLE_CHORD
    rate = (2 ** (1/12)) * half_steps
    assert os.path.exists(SAMPLE_CHORD_FILE)

    sample(os.path.realpath(SAMPLE_CHORD_FILE), rate=rate, amp=amp)
    sleep(beats * 60 / bpm)


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

# stop all tracks when the program exits normally or is interrupted
atexit.register(stop)

# play_note(60)

# These are the piano key numbers for a 3-octave blues scale in A.
# See: http://en.wikipedia.org/wiki/Blues_scale
# Let's make a slow blues solo

# These are a bunch of licks using single steps and half-beats.
# To make it cooler, I added the get_lick function above.
play_note(60, 1, 60)

play_chord(62)
# play 60
