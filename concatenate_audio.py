"""
Author: Aaron Huynh
Lab: Computational Neuroscience of Audition / Norman-Haignere Lab
PI: Samuel Norman-Haignere, PhD
Contact: aaron_huynh@urmc.rochester.edu

Last Commit: 18 April 2024
"""


import soundfile as sf
import numpy as np
import os
import re

def concatenate_audio(duration, story_num):
    # Directory containing the audio files
    directory = f"/Users/ahuynh2/Documents/Norman-Haignere/temporal-window-stimulus-generation-code/stimuli/{duration}ms/Story{story_num}"
    os.chdir(directory)
    
    # Get a list of audio file names in the directory
    audio_files = [filename for filename in os.listdir(directory) if filename.endswith("clip.wav")]

    # Define a regular expression pattern to extract numeric prefixes
    numeric_pattern = re.compile(r'^(\d+)_')

    # Sort the list of filenames based on the numeric part
    audio_files.sort(key=lambda x: int(numeric_pattern.match(x).group(1)) if numeric_pattern.match(x) else -float('inf'), reverse=False)

    # List to store audio data
    audio_data = []

    # Loop through the sorted list of files
    for filename in audio_files:
        # Load the audio file using soundfile
        file_path = os.path.join(directory, filename)
        data, sample_rate = sf.read(file_path)
        audio_data.append(data)

    # Concatenate audio data
    combined_data = np.concatenate(audio_data)

    # Save the concatenated audio to a file
    combined_file_path = f"/Users/ahuynh2/Documents/Norman-Haignere/temporal-window-stimulus-generation-code/stimuli/{duration}ms/Story{story_num}/Story{story_num}_{duration}ms.wav"
    sf.write(combined_file_path, combined_data, sample_rate)
    print(f"Story {story_num} concatenated!")
    print()


# slow = ["450", "630", "750", "900"]
# fast = ["150", "210", "250", "300"]
# story_slow = ["1"]
# story_fast = ["16"]

# for dur in slow:
#     for story in story_slow:
#         concatenate_audio(dur, story)
        
# for dur in fast:
#     for story in story_fast:
#         concatenate_audio(dur, story)