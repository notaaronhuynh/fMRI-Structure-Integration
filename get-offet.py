"""
Author: Aaron Huynh
Lab: Computational Neuroscience of Audition / Norman-Haignere Lab
PI: Samuel Norman-Haignere, PhD
Contact: aaron_huynh@urmc.rochester.edu

Last Commit: 18 April 2024
"""


import os
import librosa
import soundfile as sf
import numpy as np
import math
from scipy.signal import resample
import matplotlib.pyplot as plt

def get_offset(duration, story_num, detection_threshold, original_sr=22500, low_sr=50, export=True, plot=False, backtrack=False, backtracking_patience=50):
    # Directory containing the audio files
    path = f"/Users/ahuynh2/Documents/Norman-Haignere/temporal-window-stimulus-generation-code/stimuli/{duration}ms/Story{story_num}/"
    os.chdir(path)
    
    # Get a list of audio file names in the directory
    audio_files = [filename for filename in os.listdir(path) if filename.endswith("crop.wav")]
    
    for file in audio_files:
        y, sr = librosa.load(file, sr = None)
        
        # Split the string by underscores
        split_string = file.split('_')

        # Extract the word after the second '_'
        word = split_string[2]
        
        # Downsample aggressively to get envelope then resample to original sr
        duration = len(y) / sr
        wav_env = resample(resample(np.abs(y), int(low_sr * duration)), int(original_sr * duration))
        
#         if export:
#             filename = f"{file[:-5]}_ds.wav"
#             sf.write(filename, wav_env, sr)
        
        # Plot original and envelope 
        if plot:
            fig, ax = plt.subplots(1,1)
            ax.plot(y, label="Original Waveform")
            ax.plot(wav_env, label="Envelope")
            ax.set_title(f"Original Waveform and Envelope for \"{word}\"")
            ax.set_xlabel("Time (ms)")
            ax.set_ylabel("Amplitude")
#             ax[0].legend()  # Add legend to distinguish between offset detection method

        # Detect Offsets  
        offset = np.where(wav_env > detection_threshold)
        if len(offset) == 0:
            print("No detected offset. Consider lowering the detection threshold")
            return offset
        
        offset = offset[0][-1]
        
        # Plot detection threshold
        if plot:
            ax.axhline(detection_threshold, linestyle='dashed', color="black", linewidth=1)

        # Backtrack: from the first detection point, look backwards for changes in slope
        # You may want to set patience > 0 if you find that this is too sentitive to local minima
        if backtrack:
            deltas = np.diff(wav_env[:offset])
            backtracked_offset = np.where(deltas < 0)[0][-1]
            patience = backtracking_patience
            j = backtracked_offset

            while j > 0 and patience > 0:
                current = deltas[j]
                previous = deltas[j - 1]

                if previous < 0:
                    patience -= 1
                    j -= 1
                else:
                    j -= 1
                    backtracked_offset = j
                    patience = backtracking_patience

            # Plot backtracked offset if required
            if plot:
                ax.axvline(backtracked_offset, label="backtracked offset", color="black", linestyle='dashed')

            # Export or return backtracked offset
            if export:
#                 print(f"Backtracked offset for {file} = {backtracked_offset} ms")
                crop = y[backtracked_offset:]
                new_file = f"{file[:-4]}_final.wav"
#                 crop.export(f"{new_file}.wav", format="wav") 
                sf.write(new_file, crop, sr)

            
            else:
                return backtracked_offset

        # Plot offset offset
        if plot:
            ax.axvline(offset, label="offset", color="red", linestyle="dashed")            
        
        if plot: 
            ax.legend(fontsize=10)  
            
        # Export or return offset offset
        if export:
#             pass
#             print(f"Exporting \"{word}\"...")
            crop = y[:offset]
            new_file = f"{file[:-4]}_final.wav"
#             crop.export(f"{new_file}.wav", format="wav") 
            sf.write(new_file, crop, sr)
#             print(f"Sucessfully exported \"{word}\"!\n")


        else:
            return offset


# slow = ["450", "630", "750", "900"]
# fast = ["150", "210", "250", "300"]
# story_slow = ["1"]
# story_fast = ["16"]

# for dur in slow:
#     for story in story_slow:
#         get_offset(dur, story, detection_threshold=.015, plot=False, backtrack=False, backtracking_patience=0)
        
# for dur in fast:
#     for story in story_fast:
#         get_offset("450", "1", detection_threshold=.015, plot=True, backtrack=False, backtracking_patience=0)