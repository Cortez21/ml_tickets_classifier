import sys

from model import Model


def main(language: str):
    model = Model(language)
    model.fit()


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError:
        print('Error: language code need to be passed as argument')
