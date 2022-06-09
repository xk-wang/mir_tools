import pretty_midi
import os
import argparse
pretty_midi.pretty_midi.MAX_TICK = 1e10

parser = argparse.ArgumentParser()
parser.add_argument('--midi_path', type=str, required=True)
parser.add_argument('--txt_path', type=str, required=True)


def extract_labels_from_midi(midi_file):
	midi_data = pretty_midi.PrettyMIDI(midi_file)
	outputs = []
	for instrument in midi_data.instruments:
		notes = instrument.notes
		for note in notes:
			start = note.start
			end = note.end
			pitch = note.pitch
			velocity = note.velocity
			outputs.append([start, end, pitch, velocity])
	outputs.sort(key=lambda elem: elem[0])
	return outputs


def convert_midis_to_txt(args):
	for midiname in os.listdir(args.midi_path):
		suffix = '.'+midiname.split('.')[-1]
		assert suffix in ['.midi', 'mid', 'MID',
                    'MIDI'], 'your midi file suffix is not right!'
		savename = midiname.replace(suffix, '.txt')
		savepath = os.path.join(args.txt_path, savename)

		midipath = os.path.join(args.midi_path, midiname)
		datas = extract_labels_from_midi(midipath)

		with open(savepath, 'wt', encoding='utf8') as f:
			for data in datas:
				onset, offset, pitch, velocity = data
				f.write("{:8.4f}\t{:8.4f}\t{}\t{}\n".format(
					onset, offset, pitch, velocity))


if __name__ == '__main__':
	args = parser.parse_args()
	convert_midis_to_txt(args)