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
from pydub import AudioSegment
from scipy.signal import resample
import matplotlib.pyplot as plt

def get_onset(duration, story_num, detection_threshold, original_sr=16000, low_sr=50, export=True, plot=False, backtrack=False, backtracking_patience=50):
    # Directory containing the audio files
    path = f"/Users/ahuynh2/Documents/Norman-Haignere/temporal-window-stimulus-generation-code/stimuli/{duration}ms/Story{story_num}/"
    os.chdir(path)
    
    # Get a list of audio file names in the directory
    audio_files = [filename for filename in os.listdir(path) if filename.endswith(".aiff")]
    
    for file in audio_files:
        audio = AudioSegment.from_file(file)
        y, sr = librosa.load(file, sr = None)
        
        # Split the string by underscores
        split_string = file.split('_')

        # Extract the word after the second '_'
        word = split_string[2]
        
        # Downsample aggressively to get envelope then resample to original sr
        dur = len(y) / sr
        wav_env = resample(resample(np.abs(y), int(low_sr * dur)), int(original_sr * dur))
        
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
#             ax[0].legend()  # Add legend to distinguish between onset detection method

        # Detect onsets
        onset = np.where(wav_env > detection_threshold)
        if len(onset) == 0:
            print("No detected onset. Consider lowering the detection threshold")
            return onset
        
#         offset = np.where(wav_env > detection_threshold)
#         if len(offset) == 0:
#             print("No detected offset. Consider lowering the detection threshold")
#             return offset

        onset = onset[0][0]
#         offset = offset[0][-1]
        
        # Plot detection threshold
        if plot:
            ax.axhline(detection_threshold, linestyle='dashed', color="black", linewidth=1)

        # Backtrack: from the first detection point, look backwards for changes in slope
        # You may want to set patience > 0 if you find that this is too sentitive to local minima
        if backtrack:
            deltas = np.diff(wav_env[:onset])
            backtracked_onset = np.where(deltas < 0)[0][-1]
            patience = backtracking_patience
            j = backtracked_onset

            while j > 0 and patience > 0:
                current = deltas[j]
                previous = deltas[j - 1]

                if previous < 0:
                    patience -= 1
                    j -= 1
                else:
                    j -= 1
                    backtracked_onset = j
                    patience = backtracking_patience

            # Plot backtracked onset if required
            if plot:
                ax.axvline(backtracked_onset, label="backtracked onset", color="black", linestyle='dashed')
            
            # Export or return backtracked onset
            if export:
#                 print(f"Backtracked Onset for {file} = {backtracked_onset} ms")
                crop = y[backtracked_onset:]
                new_file = f"{file[:-5]}_crop_backtracked.wav"
#                 crop.export(f"{new_file}.wav", format="wav") 
                sf.write(new_file, crop, sr)

            
            else:
                return backtracked_onset

        # Plot detected onset
        if plot:
            ax.axvline(onset, label="onset", color="red", linestyle="dashed")
#             ax.axvline(offset, label="offset", color="green", linestyle="dashed")            
        
        if plot: 
            ax.legend(fontsize=10)  
            
        # Export or return onset onset
        if export:
#             pass
#             print(f"onset Onset for {file} = {onset} ms")
#             print(f"Exporting {word}...")
            crop = y[onset:len(y)]
            new_file = f"{file[:-5]}_crop.wav"
#             crop.export(f"{new_file}.wav", format="wav") 
            sf.write(new_file, crop, sr)
            print(f"Onset detected for {word} in Story {story_num} at {duration}ms\n")

        else:
            return onset

# slow = ["450", "630", "750", "900"]
# fast = ["150", "210", "250", "300"]
# story_slow = ["1"]
# story_fast = ["16"]

# for dur in slow:
#     for story in story_slow:
#         get_onset(dur, story, detection_threshold=.025, plot=False, backtrack=False, backtracking_patience=100)
        
# for dur in fast:
#     for story in story_fast:
#         get_onset("450", "1", detection_threshold=.025, plot=False, backtrack=False, backtracking_patience=100)
