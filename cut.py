import sys
import os
import subprocess

def split_wav(file_path):
    # Use soxi to get the duration of the WAV file
    duration_output = subprocess.check_output(["soxi", "-D", file_path])
    duration = float(duration_output.decode().strip())

    # Calculate the duration of each part
    part_duration = duration / 3

    # Use sox to split the WAV file into two equal parts first
    output_base = os.path.splitext(file_path)[0] + "_part"
    subprocess.run(["sox", file_path, output_base + "_1.wav", "trim", "0", str(part_duration)], check=True)
    subprocess.run(["sox", file_path, output_base + "_2.wav", "trim", str(part_duration), str(part_duration)], check=True)

    # Calculate the duration of the remaining part
    remaining_duration = duration - (2 * part_duration)

    # Save the remaining part as the third part
    subprocess.run(["sox", file_path, output_base + "_3.wav", "trim", str(2 * part_duration), str(remaining_duration)], check=True)

    print("Split {} into three equal parts.".format(file_path))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split_wav.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    split_wav(file_path)

