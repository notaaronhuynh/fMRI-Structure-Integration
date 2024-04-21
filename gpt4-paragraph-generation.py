"""
Author: Aaron Huynh
Lab: Computational Neuroscience of Audition / Norman-Haignere Lab
PI: Samuel Norman-Haignere, PhD
Contact: aaron_huynh@urmc.rochester.edu

Last Commit: 18 April 2024
"""


from openai import OpenAI


# client = OpenAI(api_key="[YOUR-OPENAI-KEY]")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
      {
        "role": "system",
        "content": "The user will tell you what style to write in, for example, \"news article.\" Write in that style.\n\nFollow these steps:\n\nStep 1: Write a paragraph of three complete sentences. Each sentence should have nine words. Each sentence should be comprised of a random combination of 3 total noun and verb phrases. Each noun or verb phrase being 3 words each. Avoid having the last word of each 3 word phrase be a preposition, conjunction, or indefinite article; such as \"a\" or \"the\" – otherwise, use these word types when appropriate. Each noun and verb phrase should be semantically and syntactically clear as it's own sentence, separate from the entire nine word sentence. Do not separate phrases within a single sentence with periods. Do not also use commas to separate these noun and verb phrases – there should be a single comma at most per sentence. Do not use 2 commas in a given sentence. When put back together, the three phrases should form 1 clear and coherent sentence with natural prosody. When building each sentence, number every single word, no matter the type, (1) through (9). Shorter words like \"in\" and \"an\" are still considered two separate words and should be counted as such. The number should never appear after a period. Make sure periods only occur at the end of each of the 9-word sentences, and do not artificially split a 9-word sentence with a period. Do not use hyphenated or compound words. Do not use acronyms. When put together, the 3 sentences should form a semantically appropriate and clear paragraph. \n\nStep 2: Check for the following list of items to ensure each condition has been met for a sentence: (A) Make sure the sentence has the correct number of words (nine words) by checking the numbered words. (B) Ensure a period only follows word (9). (C) There should never be periods that are after the numbered words (1) through (8) – 1 period per sentence. (D) Check that the sentence is grammatically correct and that there are no errors with spelling or capitalization. (E) Make sure there are no hyphenated words, compound words, or acronyms. (F) Isolate each of the 3 word phrases and confirm that they are grammatically correct phrases. (G) These 3 word phrases should never end in a preposition, conjunction, or indefinite article such as \"the\" or \"a\". Confirm that words (3), (6), and (9) are not a preposition, conjunction, or indefinite article. (H) Check that the prosody of the text sounds like natural human writing or speech. Thoroughly check the output from Step 1 using items from Step 2 to check, do not write out these steps. If any step is incorrect, rewrite the sentence. Go through the parts in Step 2 and rewrite again if necessary. Make sure each word is numbered. Repeat until you have a sentence that has passed each check. \n\nStep 3: rewrite without numbers, substituting any corrections made in step 2. Enclose your work for this step within triple quotes (\"\"\"). \n\nStep 4: Repeat steps 1 - 3 for the next 2 sentences of the paragraph. After all these steps are completed for each sentence, print out the final paragraph and remove all commas. Repeat steps 1-4 to create 10 total unique paragraphs of 3 sentences with 9 words each that pass each check in step 2. No need to write out the checks (A-H) in step 2 for each sentence, but still confirm each sentence passes. Just print out the final 10 paragraphs after being checked with numbers and commas removed.\n"
      },
      {
        "role": "user",
        "content": "adventure story" # [genre] story, news article, text, tweet, etc. 
      }
    ],
    temperature=1,
    max_tokens=2048,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

print(response.choices[0].message.content)
