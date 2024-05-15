import sys
import librosa
import numpy as np
import warnings
import matplotlib.pyplot as plt

def extract_features(audio_file):
    # Load audio file
    y, sr = librosa.load(audio_file)

    # Extract features
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rms = np.sqrt(np.mean(np.square(y)))  # Calculate RMS energy
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y)

    # Reshape RMS energy to match other features
    rms_feature = np.full_like(chroma_stft, rms)

    # Concatenate all features
    features = np.vstack([chroma_stft, rms_feature, spectral_centroid, spectral_bandwidth, spectral_rolloff, zero_crossing_rate])
    
    return features

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_features.py <audio_file>")
        sys.exit(1)

    audio_file = sys.argv[1]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        extracted_features = extract_features(audio_file)

    print("Extracted features shape:", extracted_features.shape)
    print("Extracted features:", extracted_features)

    # Plot extracted features
    plt.figure(figsize=(10, 6))

    # Plot each feature separately
    for i in range(extracted_features.shape[0]):
        plt.subplot(7, 4, i+1)
        plt.plot(extracted_features[i])
        plt.title("Feature {}".format(i+1))


    plt.tight_layout()
    plt.show()

