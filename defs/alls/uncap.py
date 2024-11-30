def capitalize_words_in_file(filename):
  try:
    # Read the content of the file
    with open(filename, 'r') as file:
      content = file.read()

    # Split content into words and update capitalized words
    words = content.split()
    modified_words = [word.capitalize() if word.isupper() else word for word in words]

    # Join the modified words back into a single string
    modified_content = ' '.join(modified_words)

    # Write the modified content back to the original file
    with open(filename, 'w') as file:
      file.write(modified_content)

    print(f"The file '{filename}' has been updated successfully.")
  except FileNotFoundError:
    print(f"The file '{filename}' was not found.")
  except Exception as e:
    print(f"An error occurred: {e}")

# Usage example
filename = 'your_text_file.txt' # Replace with your filename
capitalize_words_in_file(filename)
