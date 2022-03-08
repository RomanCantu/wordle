from nltk.corpus import words
import numpy as np
import random
import datetime


KEYBOARD_LAYOUT = True

ALL_WORDS = words.words()
FIVE_LETTER_WORDS = [word.lower() for word in ALL_WORDS if len(word) == 5]
ALL_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
KEYBOARD = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']

n_all = len(ALL_WORDS)
n_five = len(FIVE_LETTER_WORDS)
n_letters = len(ALL_LETTERS)

day_integer = int(datetime.date.today().strftime('%Y%m%d'))*2
random.seed(day_integer)

feedback_colors = ('\x1b[0m', '\x1b[1;49;43m', '\x1b[1;39;42m')
# letter colors are for (not used, used, in password and in correct position) respectively
letter_colors = ('\x1b[0m', '\x1b[0;37;40m', '\x1b[1;49;43m', '\x1b[1;39;42m')


def select_word():
    return random.choice(FIVE_LETTER_WORDS)


def does_word_exists(word) -> bool:
    return word in FIVE_LETTER_WORDS


def check_user_input(answer, user_input):
    # Boolean lists containing the feedback
    letter_in_word = np.array([0] * 5)
    letter_in_position = np.array([0] * 5)
    duplicated_letters = set([letter for letter in user_input if user_input.count(letter) > 1])
    duplicated_positions = {dup_letter: [] for dup_letter in duplicated_letters}

    for pos, (letter, correct_letter) in enumerate(zip(user_input, answer)):
        if letter in duplicated_letters:
            duplicated_positions[letter] += [pos]
        if letter in answer:
            letter_in_word[pos] = 1
        if letter == correct_letter:
            letter_in_position[pos] = 1

    for dup_letter in duplicated_positions:
        count_user = user_input.count(dup_letter)
        count_answer = answer.count(dup_letter)
        removal_count = 0
        if count_user > count_answer + removal_count and count_answer != 0:
            print(letter_in_word)
            print(count_user, count_answer, removal_count)
            poss = duplicated_positions[dup_letter]
            for pos in reversed(poss):
                print(letter_in_word)
                if not letter_in_word[pos] == letter_in_position[pos]:
                    letter_in_word[pos] = 0
                    removal_count += 1
                if count_user <= count_answer + removal_count:
                    break

    # on the feedback: 0 means grey, 1 means orange, 2 means green
    feedback = letter_in_word + letter_in_position
    return feedback


def translate_feedback(feedback_numbers, user_input) -> str:
    formatted_feedback = ''
    for number, letter in zip(feedback_numbers, user_input):
        color_string = feedback_colors[number]
        formatted_feedback += color_string + letter
    formatted_feedback += '\x1b[0m'
    return formatted_feedback


def print_gameboard(formatted_feedback, used_letters):
    print('\n'*30)
    print('-'*30)
    if KEYBOARD_LAYOUT:
        for row in KEYBOARD:
            keyboard_row = ''
            for letter in row:
                color_string = letter_colors[used_letters[letter]]
                keyboard_row += color_string + letter
            print(f'{keyboard_row}\x1b[0m')
    else:
        alphabeth = ''
        for letter, letter_feedback in used_letters.items():
            color_string = letter_colors[letter_feedback]
            alphabeth += color_string + letter
        print(f'{alphabeth}\x1b[0m')
    print('-'*30)
    print()
    for line in formatted_feedback:
        if line:
            print(line)


def update_used_letters(used_letters, user_input, feedback):
    for letter, letter_feedback in zip(user_input, feedback):
        current_info_status = used_letters[letter]
        if letter_feedback >= current_info_status:
            used_letters[letter] = letter_feedback + 1


def new_game():
    n_rounds = 5
    formatted_feedback = [''] * n_rounds
    used_letters = dict(zip(ALL_LETTERS, [0] * n_letters))

    answer = select_word().lower()
    # answer = [word for word in five_letter_words if len(set(word)) < 5][0]  # line that selects the first word with a letter repeated (for tests)

    for i in range(n_rounds):
        input_valid = False
        user_input = ''
        while not input_valid:
            user_input = input(f'Give your answer. This is your chance {i+1}/{n_rounds}\n').lower()
            if does_word_exists(user_input):
                input_valid = True
            else:
                print('That word does not exist, asshole (or you do not know how to count, asshole)')
        feedback = check_user_input(answer, user_input)
        update_used_letters(used_letters, user_input, feedback)
        formatted_feedback[i] = translate_feedback(feedback, user_input)
        print_gameboard(formatted_feedback, used_letters)
        if user_input == answer:
            print('\nYou won!')
            break
        if i == n_rounds - 1:
            print(f'\nYou lost. The word was {answer}')


if __name__ == '__main__':
    new_game()
