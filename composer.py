import collections as col
import numpy as np
import pickle


def compose(sentence_begin, sentence_end, second_word, third_word, sentence_length, length):
    story = open('my_story.txt', 'w')
    sentence_begin_flag = 0
    sentence_number = 0
    st = []
    index = 0
    end_flag = False
    while index < length:
        rand_value = np.random.uniform(0, 1, 1)
        total = 0.0
        if sentence_begin_flag == 0:
            rand_length = np.random.uniform(0, 1, 1)
            for size in sentence_length:
                if not size == 0:
                    total += float(sentence_length[size])/sentence_length[0]
                    if total > rand_length:
                        current_length = 3 + int(size)
                        total = 0.0
                        break
            for word in sentence_begin:
                if not word == 0:
                    total += float(sentence_begin[word])/sentence_begin[0]
                    if total > rand_value:
                        story.write(word.capitalize())
                        index += 1
                        sentence_begin_flag = 1
                        st.append(word)
                        break
        elif sentence_begin_flag == 1:
            try:
                for word in second_word[st[-1]]:
                    if not word == 0:
                        total += float(second_word[st[-1]][word])/second_word[st[-1]][0]
                        if total > rand_value:
                            st.append(word)
                            sentence_begin_flag += 1
                            story.write(' ' + word)
                            index += 1
                            break
            except:
                sentence_begin_flag = 0
                st = []
                story.write('. ')
                sentence_number += 1
        elif sentence_begin_flag >= 2:
            try:
                for word in third_word[st[-2] + ' ' + st[-1]]:
                    if not word == 0:
                        total += float(third_word[st[-2] + ' ' + st[-1]][word])/(third_word[st[-2] + ' ' + st[-1]][0])
                        if total > rand_value:
                            st.append(word)
                            story.write(' ' + word)
                            index += 1
                            sentence_begin_flag += 1
                            break
            except:
                sentence_begin_flag = 0
                st = []
                story.write('. ')
                sentence_number += 1
        try:
            if current_length <= sentence_begin_flag and sentence_begin_flag > 0 and not sentence_end[st[-1]] == 0:
                sentence_begin_flag = 0
                st = []
                story.write('. ')
                sentence_number += 1
                if np.random.uniform(0, 1, 1) > 0.85 and sentence_number > 3:
                    sentence_number = 0
                    story.write('\n\n')
        except:
            pass
        if index == length and sentence_begin_flag > 0:
            end_flag = True
            index -= 1
        if end_flag and sentence_begin_flag == 0:
            break
    story.write('The end.')


def main():
    sentence_begin = pickle.load(open('sentence_begin.pickle', 'rb'))
    sentence_end = pickle.load(open('sentence_end.pickle', 'rb'))
    second_word = pickle.load(open('second_word.pickle', 'rb'))
    third_word = pickle.load(open('third_word.pickle', 'rb'))
    sentence_length = pickle.load(open('sentence_length.pickle', 'rb'))

    compose(sentence_begin, sentence_end, second_word, third_word, sentence_length, 10000)
    

if __name__ == '__main__':
    main()
    