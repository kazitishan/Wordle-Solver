import csv

words = []

def fetchWords():
    # Path
    file_path = 'all-wordle-words.csv'

    # Open file
    with open(file_path, mode='r', newline='') as file:
        # CSV reader
        csv_reader = csv.reader(file)
    
        # Add all possible wordle words to words
        for row in csv_reader:
            words.append(row[0])

def filterWords(word, positionValues):
    global words
    
    for i in range(5):
        letter = word[i]
        # Grey Square - If the letter is not in the word
        if positionValues[i] == 0:
            words = list(filter(lambda current_word: letter not in current_word, words))
        # Yellow Square - If the letter is in the word but not the correct position
        elif positionValues[i] == 1:
            words = list(filter(lambda current_word: letter in current_word and letter != current_word[i] and letterCount(current_word, letter) >= letterCount(word, letter), words))
        # Green Square - If the letter is in the correct position
        elif positionValues[i] == 2:
            words = list(filter(lambda current_word: letter == current_word[i], words))

def fetchData(localWords):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    # Initialize Hash Maps
    occurrences = {letter: 0 for letter in alphabet}
    frequencies = {letter: 0 for letter in alphabet}
    positions = {letter: [0] * 5 for letter in alphabet}

    # For every word in the word list
    for word in localWords:
        # Keep track of what letters have been checked in each word
        searched_letters = []
        letter_index = 0
        for letter in word:
            if letter in alphabet:
                # Update frequency and position data
                frequencies[letter] += 1
                positions[letter][letter_index] += 1
                # Update occurrences only if this letter hasn't been counted for this word
                if letter not in searched_letters:
                    occurrences[letter] += 1
                    searched_letters.append(letter)
            letter_index += 1
    
    return {
        "occurrences": occurrences,
        "frequencies": frequencies,
        "positions": positions
    }

def letterCount(word, letter):
    count = 0
    for l in word:
        if l == letter: count += 1
    return count

def wordScore(word, data):
    score = 0
    lettersChecked = []
    for letter in word:
        if letter not in lettersChecked:
            score += data["occurrences"][letter]
            lettersChecked.append(letter)
    return [word, score]

# Console program
def main():
    # Fetch all words from file
    fetchWords()
    print("Total words fetched:", len(words))

    # Main game loop
    while len(words) > 1:
        # User inputs a word and position values
        user_word = input("Enter your word: ").strip().lower()
        position_values = list(map(int, input("Enter the position values (e.g., 1 0 1 0 1): ").strip().split()))

        # Filter words based on user input
        filterWords(user_word, position_values)
        
        # Fetch updated data for remaining words
        data = fetchData(words)
        
        # Sort occurrences dictionary by values in descending order
        sorted_occurrences = dict(sorted(data["occurrences"].items(), key=lambda item: item[1], reverse=True))

        # Display results
        print("\nPossible words it could be:", words)

        print("Top 10 letter occurrences:")
        
        for i, (letter, count) in enumerate(sorted_occurrences.items()):
            if i < 10:
                print(f"{letter}: {count}")
            else:
                break
        
        print("Number of words remaining:", len(words))

        wordCounts = dict(map(lambda x: wordScore(x, data), words))
        best_word = max(wordCounts, key=wordCounts.get)
        print("Chosen Next Word: " + best_word)
        
        if len(words) == 1:
            print("\nThe answer is:", words[0])

if __name__ == "__main__":
    main()