voyelles=['AE_S','A~_S','a~_S','E~_S','o~_S','E_S','a_S','e_S','i_S','O_S','o_S','u_S','y_S']


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
                if text and not text.isspace() and text !='sil' and text not in voyelles:  # Check if text is not in vowels list
                    if current_intervals and current_intervals[-1]['text'] == text:
                        # Merge consecutive intervals with the same text
                        current_intervals[-1]['xmax'] = xmax
                    else:
                        current_intervals.append({'xmin': xmin, 'xmax': xmax, 'text': text})
                    texts.append(text)  # Add text to texts list
        intervals.append(current_intervals)
    return intervals, texts  # Return intervals and texts



def compare_intervals(file1_intervals, file2_intervals, threshold=0.1):
   for intervals1, intervals2 in zip(file1_intervals[0], file2_intervals[0]):
       for interval1, interval2 in zip(intervals1, intervals2):
           xmin_diff = abs(interval1['xmin'] - interval2['xmin'])
           xmax_diff = abs(interval1['xmax'] - interval2['xmax'])
           print("Comparing intervals:")
           print("File 1: xmin={}, xmax={}, text={}".format(interval1['xmin'], interval1['xmax'], interval1['text']))
           print("File 2: xmin={}, xmax={}, text={}".format(interval2['xmin'], interval2['xmax'], interval2['text']))
           print("Difference: xmin={}, xmax={}".format(xmin_diff, xmax_diff))
           if xmin_diff > threshold or xmax_diff > threshold:
               print("Difference exceeds threshold!")
           print()
   print("Texts from file 1:", file1_intervals[1])
   print("Texts from file 2:", file2_intervals[1])
   
   print(len(file1_intervals[1]))
   print(len(file2_intervals[1]))


   list1_data = file1_intervals[1]  
   list2_data = file2_intervals[1]

   def comp_lists(list1_data, list2_data):
    index_a = 0
    index_b = 0
    mismatch = []

    while index_a < len(list1_data) and index_b < len(list2_data):
      if list1_data[index_a] == list2_data[index_b]:
        index_a += 1
        index_b += 1
      else:
        if index_a + 1 < len(list1_data) and list1_data[index_a + 1] == list2_data[index_b]:
          mismatch.append((index_a, list1_data[index_a], None, None))
          index_a += 1
        elif index_b + 1 < len(list2_data) and list2_data[index_b + 1] == list1_data[index_a]:
          mismatch.append((None, None, index_b, list2_data[index_b]))
          index_b += 1
        else:
       # One element extra in one list (handled in remaining elements loop)
          if index_a < len(list1_data):
            index_a += 1
          if index_b < len(list2_data):
            index_b += 1

 # Handle remaining elements in lists
    while index_a < len(list1_data):
      mismatch.append((index_a, list1_data[index_a], None, None))
      index_a += 1

    while index_b < len(list2_data):
      mismatch.append((None, None, index_b, list2_data[index_b]))
      index_b += 1

    return mismatch





   list1_data = file1_intervals[1]  
   list2_data = file2_intervals[1]

   #list1 = ['a', 'b', 'f', 'c', 'd', 'e', 'f','e']
   #list2 = ['b', 'c', 'd', 'e', 'k', 'f','e','z','k']

   mismatch_list = comp_lists(list1_data, list2_data)

   for index_a, item_a, index_b, item_b in mismatch_list:
       if index_a is not None:
           print("Mismatch at index {} in list1: {}".format(index_a, item_a))
       if index_b is not None:
           print("Mismatch at index {} in list2: {}".format(index_b, item_b))






file1_intervals = parse_textgrid_file("alignement_Lucile/HC/1HC-ACBC-chevre.wav/1HC-ACBC-chevre_manuel.TextGrid")
file2_intervals = parse_textgrid_file("alignement_Lucile/HC/1HC-ACBC-chevre.wav/ctm.textgrid")

# Comparing intervals
compare_intervals(file1_intervals, file2_intervals)

#file1_intervals = parse_textgrid_file("test1.TextGrid")
#file2_intervals = parse_textgrid_file("test2.TextGrid")









"""
def find_differences(list1, list2):
    mismatches = []  
    i = j = 0  
    count = 0  # Initialize count to track the number of elements to compare
    
    while i < len(list1) and j < len(list2):
        print("Comparing {} and {}".format(list1[i], list2[j]))  # Debug print
        if list1[i] == list2[j]:  
            i += 1
            j += 1
            count = 0  # Reset count
        else:
            count += 1  # Increment count
            if count == 1:  # First mismatch          
                if i + 1 < len(list1) and list1[i + 1] == list2[j]:
                    mismatches.append((i, list1[i], None, None))
                    i += 1
                elif j + 1 < len(list2) and list2[j + 1] == list1[i]:
                    mismatches.append((None, None, j, list2[j]))
                    j += 1
                else:
                    # No match found, move both indices
                    #i += 1
                    #j += 1
                    count+=1

            else:  # More than one mismatch
                if i + count-1 < len(list1) and list1[i + count-1] == list2[j]:
                    # Mismatches in list1
                    for k in range(count):
                        mismatches.append((i+k, list1[i+k], None, None))
                    i += count
                    count -=1
                elif j + count < len(list2) and list1[i] == list2[j + count]:
                    # Mismatches in list2
                    for k in range(count):
                        mismatches.append((None, None, j+k, list2[j+k]))
                    j += count
                    count -=1
                else:
                    count +=1
            count = 0  # Reset count

    # If any remaining elements in list1
    for idx in range(i, len(list1)):
        mismatches.append((idx, list1[idx]))
    
    # If any remaining elements in list2
    for idx in range(j, len(list2)):
        mismatches.append((None, None, idx, list2[idx]))
    
    return mismatches

# Example usage
list1 = [1, 2, 3, 4, 5, 7]
list2 = [1, 3, 5, 8, 7]
differences = find_differences(list1, list2)

for mismatch in differences:
    list1_idx, list1_val, list2_idx, list2_val = mismatch
    if list1_idx is not None:
        print("Mismatch at index {} (list1): {}".format(list1_idx, list1_val))
    if list2_idx is not None:
        print("Mismatch at index {} (list2): {}".format(list2_idx, list2_val))
"""
