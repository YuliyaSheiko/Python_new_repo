import re

# Original text provided for the homework
text = """homEwork: tHis iz your homeWork, copy these Text to variable. You NEED TO normalize it fROM letter CASEs 
point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF 
this Paragraph. it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

def normalize_text(text):
# Convert all letters to lowercase
    text = text.lower()

# Split the text into sentences
    sentences = text.split('. ')

# Normalize the first letter of the text
    sentences[0] = sentences[0].capitalize()

# Normalize the beginning of each sentence
    for i in range(1, len(sentences)):
        sentences[i] = sentences[i].capitalize()

# Join the sentences back together
    normalized_text = '. '.join(sentences)

    return normalized_text


normalized_text = normalize_text(text)
print(normalized_text)


def generate_new_sentence(original_text):
    # Split the original text into sentences
    sentences = original_text.split('. ')

# Extract the last word from each sentence
    last_words = [sentence.split()[-1] for sentence in sentences if sentence.strip()]

# Create a new sentence from the last words
    new_sentence = ' '.join(last_words)

# Capitalize the first letter of the new sentence
    new_sentence = new_sentence.capitalize()

# Append the new sentence to the end of the original text
    updated_text = original_text + ' ' + new_sentence

    return updated_text


text_with_new_sentnce = generate_new_sentence(normalized_text)
print(text_with_new_sentnce)


def correct_misspelled(text):
# Define a regular expression pattern
    pattern = r'\biz\b(?=(?:[^“”]*“[^“”]*”)*[^“”]*$)'
# Replace all matches of the pattern with "is"
    corrected_text = re.sub(pattern, 'is', text)
    return corrected_text


corrected_text = correct_misspelled(text_with_new_sentnce)
print(corrected_text)


def count_spaces(text):
# Count total whitespace characters
    total_whitespace = sum(1 for char in text if char.isspace())

    return total_whitespace


total_whitespace = count_spaces(corrected_text)
print("Total whitespace characters:", total_whitespace)