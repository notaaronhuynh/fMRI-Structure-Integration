"""
Author: Aaron Huynh
Lab: Computational Neuroscience of Audition / Norman-Haignere Lab
PI: Samuel Norman-Haignere, PhD
Contact: aaron_huynh@urmc.rochester.edu

Last Commit: 18 April 2024
"""


import pandas as pd
from macOS_text_to_speech import text_to_speech
from get_onset import get_onset
from get_offset import get_offset
from change_wav_duration import change_duration
from concatenate_audio import concatenate_audio

def slow_stimuli_processing():
    stimuli = pd.read_excel('/Users/ahuynh2/Documents/Norman-Haignere/stimuli_tracker.xlsx')
    paragraphs = stimuli['Paragraph'][:15]

    # slow = ["420", "450", "500", "630", "750", "900"]
    slow = ["420", "450", "630"]

    story_slow = []

    story_num = list(range(1, 16))
    for i in story_num:
        story_slow.append(str(i))
    
    for paragraph, story in zip(paragraphs, story_slow):
        cleaned_paragraph = paragraph.replace(",", "").replace(".", "")
    
        for dur in slow:
            text_to_speech(cleaned_paragraph, story, dur)
            get_onset(dur, story, detection_threshold=.025, plot=False, backtrack=False, backtracking_patience=100)
            get_offset(dur, story, detection_threshold=.0125, plot=False, backtrack=False, backtracking_patience=0)
            change_duration(dur, story, int(dur))
            concatenate_audio(dur, story)
