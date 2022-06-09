import librosa
import librosa.display
import os
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.patches as patches

audio_path = '/home/data/wxk/lab_dataset/OMAP/test/wav/02_03.wav'
label_path = '/home/data/wxk/lab_dataset/OMAP/test/align_test/02_03.txt'

off=10
duration=10

audio, sr = librosa.load(audio_path, sr=16000, mono=True, offset=off, duration=duration)
spec = librosa.cqt(audio, sr=sr, hop_length=512, fmin=27.5, n_bins=352, bins_per_octave=48)
spec = librosa.amplitude_to_db(np.abs(spec), ref=np.max)
fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True)
librosa.display.specshow(spec, sr=sr, hop_length=512, fmin=27.5, bins_per_octave=48, x_axis='time', y_axis='cqt_hz', ax=ax)

# ax.add_patch(patches.Rectangle((1.5, 256), 1, 50, linewidth=1, edgecolor="white", fill=False))

notes = np.loadtxt(label_path)
for onset, offset, pitch in notes:
	if onset>=off and (duration is None or onset<off+duration):
		hz = librosa.midi_to_hz(pitch)
		ax.add_patch(patches.Rectangle((onset-off, hz-5), offset-onset, 20, linewidth=1, edgecolor="white", fill=False))

plt.savefig("4.png")
