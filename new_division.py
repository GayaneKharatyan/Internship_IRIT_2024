import sys
import numpy as np
import matplotlib.pyplot as plt
import chardet
import codecs

voyelles=['AE_S','A~_S','a~_S','E~_S','o~_S','E_S','a_S','e_S','i_S','O_S','o_S','u_S','y_S', 'i','e','ɛ','ɛː','y','ø','œ','ə','u','o','ɔ','a','ɑ','ɑ̃','ɔ̃','ɛ̃','œ̃','j','ɥ','w']
# Function to parse TextGrid files and extract intervals
def parse_textgrid_file(filename):
    intervals = []
    # Detect file encoding
    with open(filename, 'rb') as file:
        raw_data = file.read()
        encoding = chardet.detect(raw_data)['encoding']
    # Read file content with detected encoding
    with codecs.open(filename, 'r', encoding) as file:
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
            #if text and not text.isspace() and text != 'sil':  # Exclude intervals with empty or "sil" text
            current_intervals.append({'xmin': xmin, 'xmax': xmax, 'text': text})
    intervals.append(current_intervals)
    return intervals


def extract_phoneme_sequences(interval_set):
    phoneme_sequence = [(interval['text'][1:], interval['xmin'], interval['xmax']) if interval['text'].startswith('/') else (interval['text'], interval['xmin'], interval['xmax']) for interval in interval_set]
    return phoneme_sequence



def divide_data(intervals):
    divided_parts = []
    current_part = []

    for interval in intervals:
        xmin = interval['xmin']
        xmax = interval['xmax']

        if is_silence(interval['text'].strip()):
            silence_duration = xmax - xmin
            if silence_duration > 0.45:
                if current_part:
                    divided_parts.append(current_part)
                    current_part = []
            current_part.append(interval)

        else:
            current_part.append(interval)

    if current_part:
        divided_parts.append(current_part)



    return divided_parts



def merge_and_filter_silences(part):
    merged_part = []
    current_silence_start = None
    current_silence_end = None
    silence_duration = 0

    for interval in part:
        if is_silence(interval['text'].strip()):
            if current_silence_start is None:
                current_silence_start = interval['xmin']
            current_silence_end = interval['xmax']
            silence_duration += interval['xmax'] - interval['xmin']
        else:
            if silence_duration > 0:
                merged_part.append({'xmin': current_silence_start, 'xmax': current_silence_end, 'text': 'sil'})
            current_silence_start = None
            current_silence_end = None
            silence_duration = 0
            merged_part.append(interval)

    if silence_duration > 0:
        merged_part.append({'xmin': current_silence_start, 'xmax': current_silence_end, 'text': 'sil'})

    filtered_part = [interval for interval in merged_part if interval['text'].strip() != 'sil' or (interval['xmax'] - interval['xmin']) > 0.15] #take other phonemes, and silences that are longer than 0.15

    return filtered_part



def remove_silence(parts):
    for part in parts:


    # Remove silence from the beginning and end
        while part and is_silence(part[0]['text'].strip()):
            part.pop(0)

        while part and is_silence(part[-1]['text'].strip()):
            part.pop()

    return parts

def remove_vowel_and_silence(parts):
    parts = remove_silence(parts)
    for part in parts:
    # Remove the last vowels
        while part and part[-1]['text'].strip() in voyelles:
            part.pop()
    
    return parts



def is_silence(phon):
    return (phon=='sil' or phon==' ' or phon=="" or phon =='inh' or phon=='sil/inh')

def calculate_metrics(datas):
    total_silence_duration = 0
    total_silence_count = 0
    total_vowel_duration = 0
    total_vowel_count = 0
    total_duration = datas[-1][2]-datas[0][1]

    i = 0
    while i < len(datas):
        phon, deb, fin = datas[i]

        if is_silence(phon):
            silence_duration = fin - deb
            total_silence_duration += silence_duration
            total_silence_count += 1
            i += 1  # Move to the next entry
        elif phon in voyelles:
            vowel_duration = fin - deb
            if i < len(datas) - 1:
                next_phon, next_deb, next_fin = datas[i+1]
                if is_silence(next_phon):
                    next_silence_duration = next_fin - next_deb
                    if next_silence_duration >= 0.45:
                        i += 1  # Skip only the vowel if it's followed by a long silence
                        continue

            total_vowel_duration += vowel_duration
            total_vowel_count += 1
            i += 1  # Move to the next entry
        else:
            i += 1  # Move to the next entry

    average_silence_duration = total_silence_duration / total_silence_count if total_silence_count != 0 else 0
    phonation_time=total_duration-total_silence_duration
    speech_rate = total_vowel_count / phonation_time
    average_vowel_duration = total_vowel_duration / total_vowel_count if total_vowel_count != 0 else 0

    return average_silence_duration, speech_rate, average_vowel_duration,  datas[0][1]  # returning the first xmin



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename1>")
        sys.exit(1)

    file_intervals = parse_textgrid_file(sys.argv[1])
    print("file intervals: ", file_intervals)

    merged_silences = merge_and_filter_silences(file_intervals[0])
    print("merged_silences: ", merged_silences)
    

    divided_parts = divide_data(merged_silences)
    
    parts=remove_vowel_and_silence(divided_parts)
    # Remove empty lists
    parts = [part for part in parts if part]


    for i, part in enumerate(parts):
        print("\nPart {}:".format(i+1))

        # Extract phoneme sequences
        phoneme_sequences = extract_phoneme_sequences(part)

        print("Part {} phoneme sequences: {}".format(i+1, phoneme_sequences))
        
        # Calculate metrics
        average_silence_duration, speech_rate, average_vowel_duration, first_xmin = calculate_metrics(phoneme_sequences)
        print("Metrics for part {}:".format(i+1))
        print("Start: {:.2f}".format(first_xmin))  # Printing the first xmin
        print("Average Silence Duration: {:.4f}".format(round(average_silence_duration, 4)))
        print("Speech Rate: {:.4f}".format(round(speech_rate, 4)))
        print("Average Vowel Duration: {:.4f}".format(round(average_vowel_duration, 4)))
