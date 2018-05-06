# BackingTrack

Authors: Eric Elder Jacobsen & Flynn Michael-Legg
Last Updated: May 6th, 2018

This program utilizes pygame, SonicPi v2.10, and simple-pygame-menu from Gummbum.
For more info on the simple-pygame-menu package, see the following README link:
https://github.com/zgoda-mobica/simple-pygame-menu/blob/master/README.txt

SoloBuddy is designed to help musicians learn to improvise and solo by playing a
backing track that they can play over while the program suggests important chord
tones that they can utilize over each chord in real time. SoloBuddy also suggests
notes for the upcoming chord below, so that the user has time to process what is
coming next. The suggested notes are comprised of the root, third, fifth, and
other characteristic notes of the chord. The root and fifth, being more harmonically
consonant, are displayed in black to convey their relative safety, and the other
notes, which encourage more adventurous harmony, are displayed in blue.

SoloBuddy lets the improviser input their chord progression using drop-down menus.
Then, the program plays a backing track for them to solo over, highlighting the
current chord, and suggesting scale-appropriate notes to implement over said current
chord. When a measure is added, the chord for that measure defaults to C major.

The top section of SoloBuddy contains buttons to pause/play, speed up/slow down, move
forward/back, add/delete measures, or restart the progression. Since users will be
holding instruments while using our program, we have implemented key presses for all
of these features as well (SPACE, f/s, LEFT/RIGHT ARROW, +/-, and r, respectively).

With SonicPi open in the background, the
file can be run out of the terminal with:

$ cd BackingTrack
$ python SoloBuddy.py
