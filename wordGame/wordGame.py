import random
from collections import Counter

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

# English letter frequency (approximate percentages)
LETTER_FREQUENCIES = {
    'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7,
    's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'c': 2.8,
    'u': 2.8, 'm': 2.4, 'w': 2.4, 'f': 2.2, 'g': 2.0, 'y': 2.0,
    'p': 1.9, 'b': 1.5, 'v': 1.0, 'k': 0.8, 'j': 0.2, 'x': 0.2,
    'q': 0.1, 'z': 0.1
}

# Function to partition words by word families based on the guessed letter
def get_word_families(word_list, guess, current_progress):
    families = {}
    for word in word_list:
        family_pattern = "".join([char if char == guess or char in current_progress else "_" for char in word])
        if family_pattern not in families:
            families[family_pattern] = []
        families[family_pattern].append(word)
    return families

# Function to select a weighted family, incorporating letter frequency and traps
def choose_weighted_family(families, guessed_letters, remaining_guesses):
    max_score = -float('inf')
    best_family = None
    best_pattern = ""
    
    for pattern, words in families.items():
        size_weight = len(words)
        reveal_weight = sum(1 for char in pattern if char != '_')
        remaining_letters = [char for char in 'abcdefghijklmnopqrstuvwxyz' if char not in guessed_letters]
        predicted_letter = max(remaining_letters, key=lambda char: LETTER_FREQUENCIES.get(char, 0))
        trap_weight = sum(1 for word in words if predicted_letter in word)
        
        if remaining_guesses > 5:
            score = size_weight - reveal_weight + trap_weight
        else:
            score = size_weight + reveal_weight + trap_weight
        
        if score > max_score:
            max_score = score
            best_family = words
            best_pattern = pattern

    return best_family, best_pattern

# Function to select the largest word family
def choose_largest_family(families):
    if families:
        largest_family_pattern = max(families, key=lambda k: len(families[k]))
        return families[largest_family_pattern], largest_family_pattern
    else:
        return [], "" 

# Function to start the game in EASY mode
def start_easy_mode(word_list, show_families=False):
    word_length = random.randint(4, 12)
    word_family = [word for word in word_list if len(word) == word_length]
    
    if not word_family:
        print(f"\nDEBUG: No words of length {word_length} found in the word list.")
        return

    guessed_word = ["_"] * word_length
    guessed_letters = set()
    remaining_guesses = word_length * 2
    
    print(f"The word is {word_length} letters long.\n")
    print(" ".join(guessed_word) + "\n")
    print(f"You have {remaining_guesses} guesses.\n")
    
    while "_" in guessed_word and remaining_guesses > 0:
        print(f"Letters guessed so far: {', '.join(sorted(guessed_letters))}\n")
        guess = input("Enter a letter: ").lower()
        
        if len(guess) != 1 or not guess.isalpha() or guess in guessed_letters:
            print("Invalid input or already guessed letter. Try again.\n")
            continue
        
        guessed_letters.add(guess)
        
        families = get_word_families(word_family, guess, guessed_word)
        
        if show_families:
            print("\nCurrent Word Families:")
            for pattern, words in families.items():
                print(f"{pattern}: {words}")
            print("\n")
        
        word_family, new_progress_pattern = choose_largest_family(families)
        
        if not word_family:
            remaining_guesses -= 1
            print(f"No words match your guess '{guess}'. You have {remaining_guesses} guesses left.\n")
            continue
        
        if new_progress_pattern == "".join(guessed_word):
            remaining_guesses -= 1
            print(f"Wrong guess! You have {remaining_guesses} guesses left.\n")
        else:
            guessed_word = list(new_progress_pattern)
            print("Good guess!\n")
        
        print(" ".join(guessed_word) + "\n")
    
    if "_" not in guessed_word:
        print(f"Congratulations! You've guessed the word: {''.join(guessed_word)}\n")
    else:
        final_word = random.choice(word_family)
        print(f"Sorry, you've run out of guesses. The word was: {final_word}\n")

# Function for Hard Mode with weighted family selection and trap setting
def start_hard_mode(word_list, show_families=False):
    word_length = random.randint(4, 12)
    word_family = [word for word in word_list if len(word) == word_length]
    
    if not word_family:
        print(f"\nDEBUG: No words of length {word_length} found in the word list.")
        return

    guessed_word = ["_"] * word_length
    guessed_letters = set()
    remaining_guesses = word_length * 2
    
    print(f"The word is {word_length} letters long.\n")
    print(" ".join(guessed_word) + "\n")
    print(f"You have {remaining_guesses} guesses.\n")
    
    while "_" in guessed_word and remaining_guesses > 0:
        print(f"Letters guessed so far: {', '.join(sorted(guessed_letters))}\n")
        guess = input("Enter a letter: ").lower()
        
        if len(guess) != 1 or not guess.isalpha() or guess in guessed_letters:
            print("Invalid input or already guessed letter. Try again.\n")
            continue
        
        guessed_letters.add(guess)
        
        families = get_word_families(word_family, guess, guessed_word)
        
        if show_families:
            print("\nCurrent Word Families:")
            for pattern, words in families.items():
                print(f"{pattern}: {words}")
            print("\n")
        
        word_family, new_progress_pattern = choose_weighted_family(families, guessed_letters, remaining_guesses)
        
        if not word_family:
            remaining_guesses -= 1
            print(f"No words match your guess '{guess}'. You have {remaining_guesses} guesses left.\n")
            continue
        
        if new_progress_pattern == "".join(guessed_word):
            remaining_guesses -= 1
            print(f"Wrong guess! You have {remaining_guesses} guesses left.\n")
        else:
            guessed_word = list(new_progress_pattern)
            print("Good guess!\n")
        
        print(" ".join(guessed_word) + "\n")
    
    if "_" not in guessed_word:
        print(f"Congratulations! You've guessed the word: {''.join(guessed_word)}\n")
    else:
        final_word = random.choice(word_family)
        print(f"Sorry, you've run out of guesses. The word was: {final_word}\n")

# Main function to select difficulty
def main():
    while True:
        difficulty = input("Choose difficulty - Easy (E), Hard (H): ").strip().upper()
        
        if difficulty == "E":
            word_list = load_words()
            start_easy_mode(word_list)
            break
        elif difficulty == "H":
            word_list = load_words()
            start_hard_mode(word_list)
            break
        elif difficulty == "MOD004553":
            test_word_list = load_test_words()
            start_hard_mode(test_word_list, show_families=True)
            break

main()
