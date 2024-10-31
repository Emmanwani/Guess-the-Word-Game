import random

# Load words from dictionary.txt for Easy and Hard Modes
def load_words(filename="dictionary.txt"):
    with open(filename, "r") as file:
        words = [line.strip().lower() for line in file if line.strip().isalpha()]
    return words

# Load words from test.txt for Test Level
def load_test_words(filename="test.txt"):
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
    # Ensure families is not empty before finding the largest
    if families:
        largest_family_pattern = max(families, key=lambda k: len(families[k]))
        return families[largest_family_pattern], largest_family_pattern
    else:
        return [], ""  # Return empty list and pattern if families is empty

# Function to start the game in EASY mode
def start_easy_mode(word_list, show_families=False):
    word_length = random.randint(4, 12)
    word_family = [word for word in word_list if len(word) == word_length]
    
    # Ensure word_family is populated
    if not word_family:
        print(f"\nDEBUG: No words of length {word_length} found in the word list.")
        return

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
        
        # Show families if in test mode
        if show_families:
            print("\nCurrent Word Families:")
            for pattern, words in families.items():
                print(f"{pattern}: {words}")
            print("\n")
        
        # Choose the largest word family
        word_family, new_progress_pattern = choose_largest_family(families)
        
        # Handle the case where families is empty
        if not word_family:  # If no valid families found
            remaining_guesses -= 1
            print(f"No words match your guess '{guess}'. You have {remaining_guesses} guesses left.\n")
            continue  # Go to the next guess
        
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

# Function for Hard Mode with predictive family selection (initial setup)
def start_hard_mode(word_list):
    word_length = random.randint(4, 12)
    word_family = [word for word in word_list if len(word) == word_length]
    
    # Ensure word_family is populated
    if not word_family:
        print(f"\nDEBUG: No words of length {word_length} found in the word list.")
        return

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
        
        # Predictive Family Selection Logic (Basic for now, more complex logic to be added)
        # Choose the largest word family
        word_family, new_progress_pattern = choose_largest_family(families)
        
        # Handle the case where families is empty
        if not word_family:  # If no valid families found
            remaining_guesses -= 1
            print(f"No words match your guess '{guess}'. You have {remaining_guesses} guesses left.\n")
            continue  # Go to the next guess
        
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

# Main function to select difficulty
def main():
    # Prompt for difficulty selection
    while True:
        difficulty = input("Choose difficulty - Easy (E), Hard (H), or enter code for Test Level: ").strip().upper()
        
        if difficulty == "E":
            print("Starting Easy Mode...\n")
            word_list = load_words()
            start_easy_mode(word_list)
            break
        elif difficulty == "H":
            print("Starting Hard Mode...\n")
            word_list = load_words()
            start_hard_mode(word_list)
            break
        elif difficulty == "MOD004553":
            print("Starting Test Level...\n")
            test_word_list = load_test_words()
            start_easy_mode(test_word_list, show_families=True)
            break
        else:
            print("Invalid selection. Please choose 'E', 'H', or enter the code for Test Level.\n")

# Run the game
main()
