#!/usr/bin/env python
import subprocess
import random
import time


def render(rendertype, synth, music, outdir, speed, rendertypes, synths, numplays, play):
	random.seed()
	i = 0
	if not play:
		logfile = open(outdir + "log.txt", "a+")
	while i < numplays:
		random.seed()

		# common types
		length = 60.0 / float(speed) * float(random.randint(1, 120)) / 20.0
		silent = True if random.randint(-100, 30) < 0 else False
		vol    = -200 if silent and not play else random.randint(-20,  0)
		print "Length: " + str(length)
		print "Volume: " + str(vol)

		# output file
		outname = str(i).rjust(5, '0') + ".ogg"

		cur_rendertype = rendertype if rendertype in rendertypes else rendertypes[random.randint(0, len(rendertypes) -1)]
		print "rendertype: " + cur_rendertype
		if cur_rendertype == "music":
			file = music[random.randint(0, len(music) - 1)]
			print file

			fileinfo = subprocess.Popen(["ffprobe", file], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

			for line in fileinfo.stderr.readlines():
				if "Duration" in line:
					time    = line.split()[1].split(",")[0].split(":")
					seconds = float(time[2]) + (int(time[1]) * 60)


			starttime = random.randint(0, (int(seconds - length) - 1)) if (int(seconds - length) - 1) > 0 else 0

			bass   = random.randint(-20, 20)
			treble = random.randint(-20, 20)

			print "Starttime: " + str(starttime // 60) + ":" + str(starttime % 60)
			print "Bass: " + str(bass)
			print "Treble: " + str(treble)

			callarray = ["play"] if play else ["sox"]
			callarray.append(file)
			if not play:
				callarray.append(outdir + outname)
			callarray.extend(["bass", str(bass), "treble", str(treble), "vol", str(vol) + "dB", "trim", str(starttime // 60) + ":" + str(starttime % 60), str(length), "rate", "44k", "channels", "2"])

			subprocess.Popen(callarray)

		else:
			freq = random.randint(-48, 39)
			print "Frequency: " + str(freq)
			synthtouse = synth if synth in synths else synths[random.randint(0, len(synths) - 1)]

			callarray = ["play"] if play else ["sox"]
			callarray.append("-n")
			if not play:
				callarray.append(outdir + outname)
			callarray.extend(["synth", str(length), synthtouse, "%" + ("+" if freq > 0 else "") + str(freq), "vol", str(vol) + "dB", "rate", "44k", "channels", "2", "chorus", "0.5", "0.9", "50", "0.4", "0.25", "2", "-t"])
			subprocess.call(callarray)

		if not play:
			logfile.write("Mode: " + cur_rendertype + "\n")
			logfile.write("Length: " + str(length) + "s\n")
			logfile.write("Volume: " + str(vol) + "dB\n")

			if cur_rendertype == "music":
				logfile.write("Starttime: " + str(starttime // 60) + ":" + str(starttime % 60) + "\n")
				logfile.write("Bass: " + str(bass) + "\n")
				logfile.write("Treble: " + str(treble) + "\n")
				logfile.write("Musicfile: " + file)

			else:
				logfile.write("Frequency: " + str(freq) + "\n")
				logfile.write("Synth: " + synthtouse)

			logfile.write("\n" + "\n")

		if not play:
			i += 1
