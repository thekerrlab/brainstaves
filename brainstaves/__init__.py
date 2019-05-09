from .bs_musescore import XML # To read and write MuseScore files
from .bs_music import * # The core of the program -- functions and classes for defining instruments and manipulating notes
from .bs_livedata import *
from .bs_makelivescore import makelivescore # For generating the actual score
from .bs_animation import animate # For visualizing the animation
from .bs_app import makeapp, run # For running the server