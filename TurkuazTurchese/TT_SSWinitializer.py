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

from TT_TWgatherer import *

res_flamers = []
res_noflamers = []

def append_flamer(flamer_list, cond):
    ids = []
    conversation = []
    for flamer in flamer_list:
        if not flamer['user_id'] in ids:
            ids.append(flamer['user_id'])
            user = getUserAll(flamer['user_id'])
            conversation.append(user)
            print user
    if cond:
        res_noflamers.append(conversation)
    else: 
        res_flamers.append(conversation)

def SSW_init():
    
    return 0