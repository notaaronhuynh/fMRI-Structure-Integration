"""
Author: Aaron Huynh
Lab: Computational Neuroscience of Audition / Norman-Haignere Lab
PI: Samuel Norman-Haignere, PhD
Contact: aaron_huynh@urmc.rochester.edu

Last Commit: 18 April 2024
"""


import os
from pydub import AudioSegment
from audiostretchy.stretch import stretch_audio

def change_duration(duration, story_num, target_duration):
    # Directory containing the audio files
    path = f"/Users/ahuynh2/Documents/Norman-Haignere/temporal-window-stimulus-generation-code/stimuli/{duration}ms/Story{story_num}/"
    os.chdir(path)
    
    # Get a list of audio file names in the directory
    audio_files = [filename for filename in os.listdir(path) if filename.endswith("crop_final.wav")]
    
    
    for file in audio_files:
        # Split the string by underscores
        split_string = file.split('_')

        # Extract the word after the second '_'
        word = split_string[2]
        
        audio = AudioSegment.from_file(file)
        # Calculate the ratio to stretch or compress the audio to the target duration
        ratio = target_duration/ len(audio)
#         print(f"Word = \"{word}\" \nDuration: {len(audio)}; Ratio: {ratio}\n")

        # Apply time stretching or compression
        # The stretch ratio, where values greater than 1.0 will extend the audio and 
        # values less than 1.0 will shorten the audio. From 0.5 to 2.0, or with `-d` 
        # from 0.25 to 4.0. Default is 1.0 = no stretching.
        outfile = f"{file[:-15]}_target_dur.wav"
        stretch_audio(file, outfile, ratio = ratio)
    
    audio_files = [filename for filename in os.listdir(path) if filename.endswith("target_dur.wav")]
    
    for file in audio_files:
        audio = AudioSegment.from_file(file)
        outfile = f"{file[:-4]}_clip.wav"
        trim = audio[:target_duration]  # Crop to target duration in milliseconds
        trim.export(outfile, format="wav") 

        
# slow = ["450", "630", "750", "900"]
# fast = ["150", "210", "250", "300"]
# story_slow = ["1"]
# story_fast = ["16"]

# for dur in slow:
#     for story in story_slow:
#         change_duration(dur, story, int(dur))
        
# for dur in fast:
#     for story in story_fast:
#         change_duration(dur, story, int(dur))
