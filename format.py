import chardet

def detect_encoding(filename):
    with open(filename, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    confidence = result['confidence']
    return encoding, confidence

filename = 'alignement_Lucile/HC/1HC-ACBC-chevre.wav/1HC-ACBC-chevre_manuel.TextGrid'  
encoding, confidence = detect_encoding(filename)
print("Detected encoding: {} with confidence {}".format(encoding,confidence))

