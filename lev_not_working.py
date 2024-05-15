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
                intervals.append(current_intervals)
                break
            if read_intervals and line.strip().startswith("intervals"):
                current_intervals = []
                continue
            if read_intervals and line.strip().startswith("xmin"):
                xmin = float(line.split('=')[1].strip())
                xmax = float(lines[lines.index(line) + 1].split('=')[1].strip())
                text = lines[lines.index(line) + 2].split('=')[1].strip().strip('" ')
                if text and not text.isspace() and text != 'sil':  # Exclude intervals with empty or "sil" text
                    current_intervals.append({'xmin': xmin, 'xmax': xmax, 'text': text})
    return intervals


# Function to extract phoneme sequences from TextGrid intervals
def extract_phoneme_sequences(intervals):
    phoneme_sequences = []
    for interval_set in intervals:
        phoneme_sequence = [(interval['text'], interval['xmax'] - interval['xmin']) for interval in interval_set]
        phoneme_sequences.append(phoneme_sequence)
    return phoneme_sequences


# Levenshtein Distance function
def levenshtein_distance(ref_sequence, test_sequence, insertion_deletion_penalty=0.5):
    m = len(ref_sequence)
    n = len(test_sequence)

    
    d = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    for i in range(m + 1):
        d[i][0] = i * insertion_deletion_penalty
    for j in range(n + 1):
        d[0][j] = j * insertion_deletion_penalty
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            ref_phoneme, ref_duration = ref_sequence[i - 1]
            test_phoneme, test_duration = test_sequence[j - 1]
            cost = 0 if ref_phoneme == test_phoneme else 1
            d[i][j] = min(
                d[i - 1][j] + insertion_deletion_penalty,
                d[i][j - 1] + insertion_deletion_penalty,
                d[i - 1][j - 1] + cost
            )
    return d[m][n]


# Parse TextGrid files and extract intervals
file1_intervals = parse_textgrid_file("alignement_Lucile/HC/1HC-ACBC-chevre.wav/1HC-ACBC-chevre_manuel.TextGrid")
file2_intervals = parse_textgrid_file("alignement_Lucile/HC/1HC-ACBC-chevre.wav/ctm.textgrid")

# Extract phoneme sequences from intervals
file1_phoneme_sequences = extract_phoneme_sequences(file1_intervals)
file2_phoneme_sequences = extract_phoneme_sequences(file2_intervals)

print("file1_phoneme_sequences", file1_phoneme_sequences)

# Calculate Levenshtein Distance between phoneme sequences
distance = levenshtein_distance(file1_phoneme_sequences, file2_phoneme_sequences)
print("Levenshtein Distance:", distance)

