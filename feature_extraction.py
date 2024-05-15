import numpy as np
import pandas as pd
import parselmouth
from parselmouth.praat import call
import argparse
import os

class Feature_Extraction:
    def __init__(self):
        pass

    def extract_acoustic_features(self, voice_sample, f0_min, f0_max, unit):
        try:
            sound = parselmouth.Sound(voice_sample)
            pitch = call(sound, "To Pitch", 0.0, f0_min, f0_max)
            f0_mean = call(pitch, "Get mean", 0, 0, unit) 
            f0_std_deviation= call(pitch, "Get standard deviation", 0, 0, unit) 
            harmonicity = call(sound, "To Harmonicity (cc)", 0.01, f0_min, 0.1, 1.0)
            hnr = call(harmonicity, "Get mean", 0, 0)
            pointProcess = call(sound, "To PointProcess (periodic, cc)", f0_min, f0_max)
            jitter_relative = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
            jitter_absolute = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
            jitter_rap = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
            jitter_ppq5 = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
            shimmer_relative =  call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
            shimmer_localDb = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
            shimmer_apq3 = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
            shimmer_apq5 = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
            
            features = {
                "f0_mean": f0_mean,
                "f0_std_deviation": f0_std_deviation,
                "hnr": hnr,
                "jitter_relative": jitter_relative,
                "jitter_absolute": jitter_absolute,
                "jitter_rap": jitter_rap,
                "jitter_ppq5": jitter_ppq5,
                "shimmer_relative": shimmer_relative,
                "shimmer_localDb": shimmer_localDb,
                "shimmer_apq3": shimmer_apq3,
                "shimmer_apq5": shimmer_apq5
            }
            
            return features
        except Exception as e:
            print("Unable to process this file:", voice_sample)
            print("Error:", e)
            return None

    def extract_mfcc(self, voice_sample):
        try:
            sound = parselmouth.Sound(voice_sample)
            mfcc_object = sound.to_mfcc(number_of_coefficients=12)
            mfcc_mean = np.mean(mfcc_object.to_array().T, axis=0)
            return mfcc_mean
        except Exception as e:
            print("Unable to extract MFCC for:", voice_sample)
            print("Error:", e)
            return None

    def extract_features(self, voice_sample):
        acoustic_features = self.extract_acoustic_features(voice_sample, 75, 500, "Hertz")
        mfcc_features = self.extract_mfcc(voice_sample)
        return acoustic_features, mfcc_features


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract acoustic features from an audio file")
    parser.add_argument("audio_file", type=str, help="Path to the audio file")
    args = parser.parse_args()

    patient_type = os.path.basename(args.audio_file).split('-')[0][1:]

    feature_extractor = Feature_Extraction()
    acoustic_features, mfcc_features = feature_extractor.extract_features(args.audio_file)
    
    if acoustic_features is not None and mfcc_features is not None:
        features_dict = acoustic_features.copy()
        for i, val in enumerate(mfcc_features):
            features_dict["mfcc_" + str(i)] = val

        #features_dict["patient_type"] = patient_type

        features_df = pd.DataFrame(features_dict, index=[0])

        features_df.insert(0, "audio_file", args.audio_file)
        features_df.insert(1, "patient_type", patient_type)
        with open("features_part.csv", "a") as f:
            features_df.to_csv(f, header=f.tell()==0, index=False)

