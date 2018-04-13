# BackingTrack

Authors: Eric Elder Jacobsen & Flynn Michael-Legg
Last Updated: April 13, 2018

This program utilizes pygame and SonicPi v2.10.

SoloBuddy is designed to help musicians learn to improvise and solo by playing a
backing track that they can play over while the program suggests important chord
tones that they can utilize over each chord in real time. This version can only
play the chord progression, but future versions will allow the musician to pause,
play, and modify the speed  of the backing track with simple controls so that they
do not have to put down their instrument.

While a streamlined way to input chords is in progress, currently the user has to
manually input them into the code. The program is by default set to play a modified
C major progression, but to change it simply type a new one where it appears at the
very bottom of the SoloBuddy.py file. With SonicPi open in the background, the
file can be run out of the terminal with:

$ cd BackingTrack
$ python SoloBuddy.py

The display is very rudimentary right now. It plays the chord, displays the name
of that chord, and shows the three or four important notes that go with that chord.
In future versions, we hope to make the display more attractive and intuitive, and
to have it also display the next chord so that the musician can prepare.
