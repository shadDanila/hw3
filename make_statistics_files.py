import re
import collections as col
import pickle


def get_statistics_from_text(text):
    text = text.replace('\n', ' ')
    text = text.replace('\"', '')
    text = text.replace(':', '')
    text = text.replace(';', '')
    text = text.replace('\xe2\x80\x9d', '')
    text = text.replace('\x80\x9c', '')
    text = text.replace('\x80\xa2', '')
    text = text.replace('\x80\xa6', '')
    text = text.replace('\x80\x94', '')
    text = text.replace('\xc2\xa9', '')
    text = text.replace('\xe2', '')
    text = text.replace('[', '')
    text = text.replace(']', '')
    text = text.replace('(', '')
    text = text.replace(')', '')
    text = text.replace(',', '')
    text = text.replace('*', '')
    third_word = {}
    second_word = {}
    words_in_string = []
    sentence_length = col.Counter()
    three_word_counter = col.Counter()
    two_word_counter = col.Counter()
    sentence_begin_counter = col.Counter()
    sentence_end_counter = col.Counter()
    text = re.split('(\W+)', text)
    for index in xrange(len(text) - 1):
        if text[index] == '\x80\x99' or text[index] == '\'':
            if text[index - 1][0].isalpha():
                text[index] = text[index - 1] + '\''
                text[index - 1] = ' '
                if text[index + 1][0].isalpha():
                    text[index + 1] = text[index] + text[index + 1]
                    text[index] = ' '
        elif text[index] == '-':
            text[index + 1] = text[index - 1] + text[index] + text[index + 1]
            text[index] = ' '
            text[index - 1] = ' '
    sentence_begin_flag = 0
    for index in xrange(len(text) - 1):
        if text[index][0].isalpha():
            if sentence_begin_flag == 0:
                sentence_begin_counter[text[index]] += 1
                sentence_begin_flag = 1 
            elif sentence_begin_flag == 1:
                two_word_counter[text[index - 2] + ' ' + text[index]] += 1
                sentence_begin_flag = 2
            elif sentence_begin_flag >= 2:
                three_word_counter[text[index - 4] + ' ' + text[index - 2] + ' ' + text[index]] += 1
                sentence_begin_flag += 1
        elif text[index][0] == '.' or text[index][0] == '!' or text[index][0] == '?':
            sentence_end_counter[text[index - 1]] += 1
            if not sentence_begin_counter == 0:
                sentence_length[sentence_begin_flag] += 1
            sentence_begin_flag = 0

    sentence_end_counter['a'] = 0
    sentence_end_counter['the'] = 0
    for string in three_word_counter:
        word_in_string = []
        word = []
        for symbol in string:
            if not symbol.isspace():
                word.append(symbol)
            else:
                word_in_string.append(''.join(word))
                word = []
        word_in_string.append(''.join(word))
        third_word.setdefault(word_in_string[0] + ' ' + word_in_string[1], {})
        third_word[word_in_string[0] + ' ' + word_in_string[1]][word_in_string[2]] = three_word_counter[string]
    for string in two_word_counter:
        word_in_string = []
        word = []
        for symbol in string:
            if not symbol.isspace():
                word.append(symbol)
            else:
                word_in_string.append(''.join(word))
                word = []
        word_in_string.append(''.join(word))
        second_word.setdefault(word_in_string[0], {})
        second_word[word_in_string[0]][word_in_string[1]] = two_word_counter[string]

    sentence_length_file = open('sentence_length.pickle', 'wb')
    sentence_begin_file = open('sentence_begin.pickle', 'wb')
    sentence_end_file = open('sentence_end.pickle', 'wb')
    second_word_file = open('second_word.pickle', 'wb')
    third_word_file = open('third_word.pickle', 'wb')

    sentence_begin_counter[0] = sum(sentence_begin_counter.itervalues())
    for elements in second_word.values():
        elements[0] = sum(elements.itervalues())
    for elements in third_word.values():
        elements[0] = sum(elements.itervalues())
    sentence_length[0] = sum(sentence_length.itervalues())
    
    pickle.dump(sentence_length, sentence_length_file)
    pickle.dump(sentence_begin_counter, sentence_begin_file)
    pickle.dump(second_word, second_word_file)
    pickle.dump(third_word, third_word_file)
    pickle.dump(sentence_end_counter, sentence_end_file)


def main():
    all_books = open("alltexts.txt", "r")
    data = all_books.read()
    get_statistics_from_text(data)


if __name__ == '__main__':
    main()
    