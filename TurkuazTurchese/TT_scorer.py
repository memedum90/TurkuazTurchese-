# -*- coding: utf-8 -*-

# Copyright (C) 2013 Federico Montori <fede.selmer@gmail.com>, Mehmet Durna <memdum@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import math
import re

# WEIGHTS
SWupp = 0.1 # Weight assigned to one uppercase
SWmrk = 1.5 # Weigth assigned to one question or exclamation mark
SWgud = -8 # Weigth assigned to one good smiley
SWbad = -0.5 # Weight assigned to one bad smiley
SWvlg = 4 # Weight assigned to one bad or risky word
SWump = 5 # Weight assigned to one politeness point
SWdis = 6 # Weight assigned to one disagreement point

# Final function to compute the overall score of a conversation
def compute_score(conver):
    STupp = 0
    STmrk = 0
    STgud = 0
    STbad = 0
    STvlg = 0
    STump = 0
    STdis = 0
    for idx, tw in enumerate(conver):
        STupp += tw['uppercases']
        STmrk += tw['marks']
        STgud += tw['good']
        STbad += tw['bad']
        STvlg += tw['vulgarity']
        STump += tw['unpoliteness']
        STdis += tw['disagreement']
    return float(SWupp*STupp + SWmrk*STmrk + SWgud*STgud + SWbad*STbad + SWvlg*STvlg + SWdis*STdis) / (len(conver))