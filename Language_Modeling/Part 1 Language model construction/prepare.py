#!/usr/bin/env python

"""Builds an English trigram language model over tokens."""

import gzip
import nltk
import argparse


def main(args: argparse.Namespace) -> None:
    with gzip.GzipFile(args.file) as source:
        with open("en.tok", "w") as sink:
            for line in source:
                str_line = str(line, "UTF-8")
                tokenized_line = nltk.tokenize.word_tokenize(str_line)
                joined_line = " ".join(tokenized_line)
                new_sentence = joined_line.casefold()
                print(new_sentence, file=sink)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "file", help="Input a file name (e.g. news.2007.en.shuffled.gz)"
    )
    main(parser.parse_args())
