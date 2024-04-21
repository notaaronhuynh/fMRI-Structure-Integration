"""
Author: Aaron Huynh
Lab: Computational Neuroscience of Audition / Norman-Haignere Lab
PI: Samuel Norman-Haignere, PhD
Contact: aaron_huynh@urmc.rochester.edu

Last Commit: 18 April 2024
"""


## Text-to-Speech using terminal
# With Prepositions
import os

def text_to_speech(paragraph, story_num, duration):
    path = f'/Users/ahuynh2/Documents/Norman-Haignere/temporal-window-stimulus-generation-code/stimuli/{duration}ms/Story{story_num}'
    os.chdir(path)

    word_list = paragraph.split()
    print(word_list)
    print()
    
#     os.system(f"say -v \"Samantha\" \"{paragraph}\" -o Story{story_num}")

    for num, word in enumerate(word_list):

        print(f"\tConverting \"{word}\" to text-to-speech")

        os.system(f"say -v \"Samantha\" \"{word}\" -o {num+1}_story{story_num}_{word}_{duration}ms")

        print(f"\n\t\t\"{word}\" converted\n")

    print("\nSaved all text-to-speech stimulus!")