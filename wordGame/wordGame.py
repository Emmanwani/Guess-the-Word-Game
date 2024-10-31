import random

# Load words from dictionary.txt
def load_words(filename="dictionary.txt"):
    with open(filename, "r") as file:
        words = [line.strip().lower() for line in file if line.strip().isalpha()]
    return words

# Function to partition words by word families based on the guessed letter
def get_word_families(word_list, guess, current_progress):
    families = {}
    for word in word_list:
        # Create a pattern based on the guessed letter and the current progress
        family_pattern = "".join([char if char == guess or char in current_progress else "_" for char in word])
        
        # Add word to the corresponding family
        if family_pattern not in families:
            families[family_pattern] = []
        families[family_pattern].append(word)
    
    return families

# Function to select the largest word family
def choose_largest_family(families):
    # Return the family with the most words
    largest_family_pattern = max(families, key=lambda k: len(families[k]))
    return families[largest_family_pattern], largest_family_pattern

# Function to start the game
def start_game():
    # Load the dictionary and filter by word length
    word_list = load_words()
    word_length = random.randint(4, 12)
    word_family = [word for word in word_list if len(word) == word_length]
    
    # Initialize game state
    guessed_word = ["_"] * word_length
    guessed_letters = set()
    remaining_guesses = word_length * 2
    
    print(f"The word is {word_length} letters long.\n")
    print(" ".join(guessed_word) + "\n")
    print(f"You have {remaining_guesses} guesses.\n")
    
    # Game loop
    while "_" in guessed_word and remaining_guesses > 0:
        print(f"Letters guessed so far: {', '.join(sorted(guessed_letters))}\n")
        guess = input("Enter a letter: ").lower()
        
        # Validate input
        if len(guess) != 1 or not guess.isalpha() or guess in guessed_letters:
            print("Invalid input or already guessed letter. Try again.\n")
            continue
        
        guessed_letters.add(guess)
        
        # Partition words into families based on the guessed letter
        families = get_word_families(word_family, guess, guessed_word)
        
        # Choose the largest word family to maximize ambiguity
        word_family, new_progress_pattern = choose_largest_family(families)
        
        # Check if the new pattern includes the guessed letter
        if new_progress_pattern == "".join(guessed_word):  # No match, wrong guess
            remaining_guesses -= 1
            print(f"Wrong guess! You have {remaining_guesses} guesses left.\n")
        else:
            # Reveal the positions of the guessed letter
            guessed_word = list(new_progress_pattern)
            print("Good guess!\n")
        
        # Display the current state of the word
        print(" ".join(guessed_word) + "\n")
    
    # End of game message
    if "_" not in guessed_word:
        print(f"Congratulations! You've guessed the word: {''.join(guessed_word)}\n")
    else:
        final_word = random.choice(word_family)  # Choose any word from the remaining list
        print(f"Sorry, you've run out of guesses. The word was: {final_word}\n")

# Run the game
start_game()
