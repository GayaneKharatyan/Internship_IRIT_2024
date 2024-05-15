import librosa
import numpy as np
import argparse

def extract_mfcc_features(audio_path, n_mfcc=13):
    y, sr = librosa.load(audio_path)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)

    mfccs_mean = np.mean(mfccs, axis=1)
    return mfccs_mean.tolist()

def main():
    parser = argparse.ArgumentParser(description='Extract MFCC features from an audio file.')
    parser.add_argument('audio_path', type=str, help='Path to the audio file')

    args = parser.parse_args()

    mfcc_features = extract_mfcc_features(args.audio_path)
    print("MFCC Features:", mfcc_features)

if __name__ == '__main__':
    main()

