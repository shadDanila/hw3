import os


def collect_books():
    all_texts_file = open("alltexts.txt", 'w')
    for dirname, dirnames, filenames in os.walk('corpus'):
        for filename in filenames:
            if '.txt' in filename:
                print(os.path.join(dirname, filename))
                with open(dirname + '/' + filename, 'r') as txtfile:
                    text = txtfile.read()
                    all_texts_file.write(text)


def main():
    all_books = collect_books()


if __name__ == '__main__':
    main()