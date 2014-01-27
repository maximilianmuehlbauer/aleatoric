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

import os
import subprocess

for (dirpath, dirnames, filenames) in os.walk("parts"):
	for dirname in dirnames:
		subprocess.Popen(["cat parts/" + dirname + "/*.ogg > parts/" + dirname + "-out.ogg"], shell=True)
