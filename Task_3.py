import re


# Example usage:
# test_text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. \nLorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."

def normalize_text(text):
    print("text:", text)
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

# def generate_new_sentence(original_text):
#     # Split the original text into sentences
#     sentences = original_text.split('. ')

#     # Extract the last word from each sentence
#     last_words = [sentence.split()[-1] for sentence in sentences if sentence.strip()]

#     # Create a new sentence from the last words
#     new_sentence = ' '.join(last_words)

#     # Capitalize the first letter of the new sentence
#     new_sentence = new_sentence.capitalize()

#     # Append the new sentence to the end of the original text
#     updated_text = original_text + ' ' + new_sentence

#     return updated_text

# def correct_misspelled(text):
#     # Define a regular expression pattern
#     pattern = r'\biz\b(?=(?:[^“”]*“[^“”]*”)*[^“”]*$)'
#     # Replace all matches of the pattern with "is"
#     corrected_text = re.sub(pattern, 'is', text)
#     return corrected_text

# def count_spaces(text):
#     total_whitespace = sum(1 for char in text if char.isspace())

#     return total_whitespace

# def main(text):
#   normalized_text = normalize_text(text)
#   print("Normalized text:", normalized_text)

#   new_sentence = generate_new_sentence(normalized_text)
#   print("New sentence:", new_sentence)

#   corrected_text = correct_misspelled(new_sentence)
#   print("Corrected text:", corrected_text)

#   total_whitespace = count_spaces(corrected_text)
#   print("Total whitespace characters:", total_whitespace)

# main(test_text)