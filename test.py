import pandas as pd

stimuli = pd.read_excel('/Users/ahuynh2/Documents/Norman-Haignere/stimuli_tracker.xlsx')
paragraphs = []
for x in stimuli:
    paragraphs.append(stimuli['Paragraph'])

print(paragraphs)