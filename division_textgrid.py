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
    phoneme_sequence = [(interval['text'], interval['xmin'], interval['xmax']) for interval in interval_set if not interval['text'].startswith('/')]
    return phoneme_sequence





def find_nearest_xmax(intervals, target):

    nearest_xmax = None
    longest_duration = 0
    min_difference = float('inf')

    for set_of_intervals in intervals:
        for interval in set_of_intervals:
            xmax = interval['xmax']
            xmin = interval['xmin']
            text = interval['text']

            if is_silence(text.strip()):
                difference = abs(xmax - target)
                duration = xmax - xmin
                if difference < min_difference or (difference == min_difference and duration > longest_duration):
                    min_difference = difference
                    nearest_xmax = xmax
                    longest_duration = duration

    return nearest_xmax


def divide_data(intervals, nearest_xmax_one_third, nearest_xmax_two_thirds):
    first_part = []
    second_part = []
    third_part = []

    for set_of_intervals in intervals:
        for interval in set_of_intervals:
            xmin = interval['xmin']
            xmax = interval['xmax']

            if xmax <= nearest_xmax_one_third:
                first_part.append(interval)
            elif xmin >= nearest_xmax_one_third and xmax <= nearest_xmax_two_thirds:
                second_part.append(interval)
            elif xmin >= nearest_xmax_two_thirds:
                third_part.append(interval)

    return first_part, second_part, third_part




def merge_consecutive_silences(part):
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
            if silence_duration > 0.15:
                merged_part.append({'xmin': current_silence_start, 'xmax': current_silence_end, 'text': 'sil'})
            current_silence_start = None
            current_silence_end = None
            silence_duration = 0
            merged_part.append(interval)

    if silence_duration > 0.15:
        merged_part.append({'xmin': current_silence_start, 'xmax': current_silence_end, 'text': 'sil'})

    return merged_part


def remove_silence(part):
    part = merge_consecutive_silences(part)

    # Remove silence from the beginning and end
    while part and is_silence(part[0]['text'].strip()):
        part.pop(0)

    while part and is_silence(part[-1]['text'].strip()):
        part.pop()

    return part

def remove_vowel_and_silence(part):
    part = remove_silence(part)

    # Remove the last vowels
    while part and part[-1]['text'].strip() in voyelles:
        part.pop()

    return part


def is_silence(phon):
    return (phon=='sil' or phon==' ' or phon==""or phon=='inh' or phon=='sil/inh')

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

    return average_silence_duration, speech_rate, average_vowel_duration




if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename1> <filename2>")
        sys.exit(1)

    file_intervals = parse_textgrid_file(sys.argv[1])
    print("file intervals: ", file_intervals)

    last_interval = file_intervals[-1][-1]  # Get the last interval in the last set of intervals
    file_duration = last_interval['xmax']  # Extract the 'xmax' value from the last interval
    one_third_point = file_duration * (1/3)
    two_thirds_point = file_duration * (2/3)

    
    print("Duration of the file:", file_duration)
    print("1/3 point of the file duration:", one_third_point)
    print("2/3 point of the file duration:", two_thirds_point)

    nearest_xmax_one_third = find_nearest_xmax(file_intervals, one_third_point)
    nearest_xmax_two_thirds = find_nearest_xmax(file_intervals, two_thirds_point)

    print("Nearest xmax to 1/3 point:", nearest_xmax_one_third)
    print("Nearest xmax to 2/3 point:", nearest_xmax_two_thirds)


    first_part, second_part, third_part = divide_data(file_intervals, nearest_xmax_one_third, nearest_xmax_two_thirds)

    print("First part:")
    for interval in first_part:
        print(interval)

    print("\nSecond part:")
    for interval in second_part:
        print(interval)

    print("\nThird part:")
    for interval in third_part:
        print(interval)


    
    r_first_part = remove_vowel_and_silence(first_part)
    r_second_part = remove_vowel_and_silence(second_part)
    r_third_part = remove_vowel_and_silence(third_part)

    print("\nAfter removing silence from the beginning and end:")

    print("First part after:")
    for interval in r_first_part:
        print(interval)

    print("\nSecond part after:")
    for interval in r_second_part:
        print(interval)

    print("\nThird part after:")
    for interval in r_third_part:
        print(interval)


   
    phoneme_sequences_part1 = extract_phoneme_sequences(r_first_part)
    phoneme_sequences_part2 = extract_phoneme_sequences(r_second_part)
    phoneme_sequences_part3 = extract_phoneme_sequences(r_third_part)
    print("part 1 phoneme sequences: ", phoneme_sequences_part1)
    print("part 2 phoneme sequences: ", phoneme_sequences_part2)
    print("part 3 phoneme sequences: ", phoneme_sequences_part3)

    divided_data=[phoneme_sequences_part1,phoneme_sequences_part2,phoneme_sequences_part3]
	
    for i, data_chunk in enumerate(divided_data):
        average_silence_duration, speech_rate, average_vowel_duration = calculate_metrics(data_chunk)
        print("Metrics for part {}: ".format(i+1))
        print("Average Silence Duration: {:.4f}".format(round(average_silence_duration, 4)))
        print("Speech Rate: {:.4f}".format(round(speech_rate, 4)))
        print("Average Vowel Duration: {:.4f}".format(round(average_vowel_duration, 4)))


