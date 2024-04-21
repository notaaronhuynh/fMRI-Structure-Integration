"""
Author: Aaron Huynh
Lab: Computational Neuroscience of Audition / Norman-Haignere Lab
PI: Samuel Norman-Haignere, PhD
Contact: aaron_huynh@urmc.rochester.edu

Last Commit: 18 April 2024
"""


from utils import text_to_speech
from utils import get_onset
from utils import get_offset
from utils import change_duration
from utils import concatenate_audio
from utils import change_duration


def slow_stimuli_processing():
    paragraphs = []

    slow = ["450", "630", "750", "900"]
    story_slow = ["1"]

    for paragraph in paragraphs:       
        for dur in slow:
            for story in story_slow:
                text_to_speech(paragraph, story, dur)
                get_onset(dur, story, detection_threshold=.025, plot=False, backtrack=False, backtracking_patience=100)
                get_offset(dur, story, detection_threshold=.015, plot=False, backtrack=False, backtracking_patience=0)
                change_duration(dur, story, int(dur))
                concatenate_audio(dur, story)


if __name__ == "__main__":
    main()