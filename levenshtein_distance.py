voyelles=['AE_S','A~_S','a~_S','E~_S','o~_S','E_S','a_S','e_S','i_S','O_S','o_S','u_S','y_S', 'i','e','ɛ','ɛː','y','ø','œ','ə','u','o','ɔ','a','ɑ','ɑ̃','ɔ̃','ɛ̃','œ̃','j','ɥ','w']

# Function to parse TextGrid files and extract intervals
def parse_textgrid_file(filename):
    intervals = []
    texts = []  # List to store texts
    with open(filename, 'r') as file:
        lines = file.readlines()
        read_intervals = False
        current_intervals = []  # Initialize current_intervals
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
                if text and not text.isspace() and text !='sil':  # Check if text is not in vowels list
                    if current_intervals and current_intervals[-1]['text'] == text:
                        # Merge consecutive intervals with the same text
                        current_intervals[-1]['xmax'] = xmax
                    else:
                        current_intervals.append({'xmin': xmin, 'xmax': xmax, 'text': text})
                    texts.append(text)  # Add text to texts list
        intervals.append(current_intervals)
    return intervals, texts  # Return intervals and texts


def levenshtein_distance(ref_sequence, test_sequence, insertion_deletion_penalty=1):
    """
    Calculates the Levenshtein distance between two sequences.

    Args:
        ref_sequence: A list of phonemes (strings).
        test_sequence: A list of phonemes (strings).
        insertion_deletion_penalty: Penalty for insertions/deletions (default 0.5).

    Returns:
        The Levenshtein distance between the sequences.
    """
    m = len(ref_sequence)
    n = len(test_sequence)

    d = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        d[i][0] = i * insertion_deletion_penalty
    for j in range(n + 1):
        d[0][j] = j * insertion_deletion_penalty

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if ref_sequence[i - 1] == test_sequence[j - 1]:
                cost = 0
            else:
                cost = insertion_deletion_penalty

            d[i][j] = min(
                d[i - 1][j] + insertion_deletion_penalty,  # Insertion
                d[i][j - 1] + insertion_deletion_penalty,  # Deletion
                d[i - 1][j - 1] + cost  # Substitution
            )

    return d[m][n]




# Parse TextGrid files and extract intervals
file1_intervals = parse_textgrid_file("alignement_Lucile/MSA/1MSA-FXAY-chevre.wav/1MSA-FXAY-chevre-manuel-old.TextGrid")
file2_intervals = parse_textgrid_file("alignement_Lucile/MSA/1MSA-FXAY-chevre.wav/ctm.textgrid")

list1_data = file1_intervals[1]  
list2_data = file2_intervals[1]
print("list 1: ",list1_data)
print(len(list1_data))
print("list 2: ",list2_data)
print(len(list2_data))
distance = levenshtein_distance(list1_data, list2_data)
print("Levenshtein Distance:", distance)

