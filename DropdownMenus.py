#!/usr/bin/env python

"""test_menu.py - A no-fuss popup menu demo.
High-level steps for a blocking menu:
1.  Fashion a nested list of strings for the PopupMenu constructor.
2.  Upon creation, the menu runs its own loop.
3.  Upon exit, control is returned to the caller.
4.  Handle the resulting USEREVENT event in the caller where
    event.name=='your menu title', event.item_id holds the selected item
    number, and event.text holds the item label.
"""

# PopupMenu
# Version:  v1.2.1
# Description: A low-fuss, infinitely nested popup menu for pygame.
# Author: Gummbum
# Home: http://code.google.com/p/simple-pygame-menu/
# Source: See home.


import os
import sys

import pygame
from pygame.locals import *

progname = sys.argv[0]
progdir = os.path.dirname(progname)
sys.path.append(os.path.join(progdir,'gamelib'))

from MenuBackStuff import PopupMenu


screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

## Menu data and functions.

menu_data = (
    'Roots',
    (
        'Ab',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    (
        'A',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    (
        'A#',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    (
        'Bb',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    (
        'B',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    (
        'C',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    (
        'C#',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    (
        'Db',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    (
        'D',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    (
        'D#',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    (
        'Eb',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    (
        'E',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    (
        'F',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    (
        'F#',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    (
        'Gb',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    (
        'G',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    (
        'G#',
        'major',
        'minor',
        'major 7',
        'minor 7',
    ),
    'Quit',
)
def handle_menu(e):
    print('Menu event: %s.%d: %s' % (e.name,e.item_id,e.text))
    if e.name == 'Roots':
        if e.text == 'Quit':
            quit()
    elif e.name == 'Ab':
        pass
    elif e.name == 'A':
        pass
    elif e.name == 'A#':
        pass
    elif e.name == 'Bb':
        pass
    elif e.name == 'B':
        pass
    elif e.name == 'C':
        pass
    elif e.name == 'C#':
        pass
    elif e.name == 'Db':
        pass
    elif e.name == 'D':
        pass
    elif e.name == 'D#':
        pass
    elif e.name == 'Eb':
        pass
    elif e.name == 'E':
        pass
    elif e.name == 'F':
        pass
    elif e.name == 'F#':
        pass
    elif e.name == 'Gb':
        pass
    elif e.name == 'G':
        pass
    elif e.name == 'G#':
        pass
    elif e.name == 'More Things':
        pass

## Main loop.

while 1:
    screen.fill(Color('darkblue'))
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == MOUSEBUTTONUP:
            ## Blocking popup menu.
            PopupMenu(menu_data, pos = (0,0))
        elif e.type == USEREVENT:
            if e.code == 'MENU':
                handle_menu(e)
clock.tick(30)
