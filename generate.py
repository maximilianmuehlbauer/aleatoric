#!/usr/bin/env python
#coding=utf-8

# Copyright 2013 Maximilian Mühlbauer
#
# This file is part of aleatoric.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, os
import subprocess
import random
import time
import multiprocessing
from render import *

"""
Settings
speed: for the fourths
musicdirs: the dirs containing music
"""
speed = 96
musicdirs = ["~/Musik/", "~/Audiobooks/"]
synths = ["sine", "pluck"]
rendertypes = ["music", "synth"]

# parse arguments
play = True if sys.argv[1] == "play" else False
rendertype = sys.argv[2] if len(sys.argv) > 2 else "chance"
synth = sys.argv[3] if rendertype == "synth" and len(sys.argv) > 3 else "chance"

# the music list, containing all the music
music = []

for musicdir in musicdirs:

	# scan for all mp3's and ogg's
	for (dirpath, dirnames, filenames) in os.walk(os.path.expanduser(musicdir)):
		musicfiles = []
		for file in filenames:
			if not file.endswith("mp3") and not file.endswith("ogg"):
				continue
			musicfiles.append(dirpath + "/" + file)
		music.extend(musicfiles)

random.seed()

run = 0
if play:
	if rendertype == "synth":
		numruns = random.randint(10, 20)
	else:
		numruns = 5
else:
	numruns  = random.randint(10, 100 if rendertype != "music" else 15)
numplays = random.randint(50, 100)
print "#############################"
print "runs:  " + str(numruns)
print "plays: " + str(numplays)
print "#############################"
time.sleep(5)

procs = []
while run < numruns:
	outdir = "parts/" + str(run).rjust(5, '0') + "/"
	if not os.path.isdir(outdir):
		os.mkdir(outdir)
	run += 1

	p = multiprocessing.Process(target=render, args=(rendertype, synth, music, outdir, speed, rendertypes, synths, numplays, play))
	p.start()

	procs.append(p)

for p in procs:
	p.join()
