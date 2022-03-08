import pandas as pd
import numpy as np

appendix_1 = list()
appendix_1.append([])
appendix_1.append(pd.read_csv('Participium_deel_1.csv', index_col=0))
appendix_1.append(pd.read_csv('Participium_deel_2.csv', index_col=0))


def generate_word_list(sections_to_include):
    try:
        word_list_gen = pd.concat(sections_to_include)
    except TypeError:
        word_list_gen = sections_to_include
    return word_list_gen


def ask_a_participium():
    array_infinitives = word_list.index.to_numpy()
    infitinive = np.random.choice(array_infinitives)
    correct_answer = word_list.loc[infitinive, 'participium']
    answer = input(f'Wat is het participium van {infitinive}?\n')

    if answer == 'engels':
        english_word = word_list.loc[infitinive, 'engels']
        answer = input(f'Dat is \"{english_word}\" in het Engels. Wat is zijn participium?\n')

    if answer == correct_answer:
        print(':) Dat klopt!')
    else:
        print(f':( Helaas, is dat niet het juiste antwoord. Het is {correct_answer}')


while True:
    word_list = generate_word_list(appendix_1[2])
    ask_a_participium()