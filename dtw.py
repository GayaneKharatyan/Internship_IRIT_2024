import numpy as np
from fastdtw import fastdtw
import matplotlib.pyplot as plt 


voyelles=['AE_S','A~_S','a~_S','E~_S','o~_S','E_S','a_S','e_S','i_S','O_S','o_S','u_S','y_S', 'i','e','ɛ','ɛː','y','ø','œ','ə','u','o','ɔ','a','ɑ','ɑ̃','ɔ̃','ɛ̃','œ̃','j','ɥ','w']
# Function to parse TextGrid files and extract intervals
def parse_textgrid_file(filename):
    intervals = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        read_intervals = False
        current_intervals = []
        for line in lines:
            if line.strip().startswith("intervals"):
                read_intervals = True
                continue
            if read_intervals and line.strip().startswith("}"):
                break
            if read_intervals and line.strip().startswith("intervals"):
                current_intervals = []
                continue
            if read_intervals and line.strip().startswith("xmin"):
                xmin = float(line.split('=')[1].strip())
                xmax = float(lines[lines.index(line) + 1].split('=')[1].strip())
                text = lines[lines.index(line) + 2].split('=')[1].strip().strip('" ')
                if text and not text.isspace() and text != 'sil' :  # Exclude intervals with empty or "sil" text
                    current_intervals.append({'xmin': xmin, 'xmax': xmax, 'text': text})
        intervals.append(current_intervals)  # This line should be indented
    return intervals

# Function to extract phoneme sequences from TextGrid intervals
def extract_phoneme_sequences(intervals):
    phoneme_sequences = []
    for interval_set in intervals:
        phoneme_sequence = [(interval['text'], interval['xmax'] - interval['xmin']) for interval in interval_set if not interval['text'].startswith('/')]
        phoneme_sequences.append(phoneme_sequence)
    return phoneme_sequences


# Function to calculate DTW distance between two sequences
def dtw_distance(seq1, seq2):
    distance, path = fastdtw(seq1, seq2)
    return distance, path

# Parse the TextGrid files
file1_intervals = parse_textgrid_file("alignement_Lucile/HC/1HC-ACBC-chevre.wav/1HC-ACBC-chevre_manuel-old.TextGrid")
file2_intervals = parse_textgrid_file("alignement_Lucile/HC/1HC-ACBC-chevre.wav/ctm.textgrid")

print("file1 intervals: ", file1_intervals)
print("file2 intervals: ", file2_intervals)

# Extract phoneme sequences from the intervals
phoneme_sequences1 = extract_phoneme_sequences(file1_intervals)
phoneme_sequences2 = extract_phoneme_sequences(file2_intervals)

print("file1 phoneme sequences: ", phoneme_sequences1)
print("file2 phoneme sequences: ", phoneme_sequences2)

# Extract phoneme durations from the intervals
durations1 = [duration for _, duration in phoneme_sequences1[0]]
durations2 = [duration for _, duration in phoneme_sequences2[0]]

print("file1 durations: ", durations1)
print("file2 durations: ", durations2)

# Calculate DTW distance between the sequences
dtw_dist, path = dtw_distance(durations1, durations2)
print("DTW Distance:", dtw_dist)
print(path)

# Visualization
plt.figure(figsize=(10, 6))

# Plot the sequences
plt.plot(durations1, label="Durations 1")
plt.plot(durations2, label="Durations 2")

# Extract x and y coordinates from path (list of tuples)
x_coords = [point[0] for point in path]
y_coords = [point[1] for point in path]

# Plot the warping path
plt.plot(x_coords, y_coords, 'o-', color='red', label="Warping Path")

plt.xlabel("Sequence 1")
plt.ylabel("Sequence 2")
plt.title("DTW Alignment of Phoneme Durations")
plt.legend()
plt.grid(True)
plt.show()







