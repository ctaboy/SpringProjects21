#!/usr/bin/env python
"""Splits portions of data from 'conll2000.tag' into three separate files."""

import argparse
import random
from typing import Iterator, List


def read_tags(path: str) -> Iterator[List[List[str]]]:
    with open(path, "r") as source:
        lines = []
        for line in source:
            line = line.rstrip()
            if line:  # Line is contentful.
                lines.append(line.split())
            else:  # Line is blank.
                yield lines.copy()
                lines.clear()
    # Just in case someone forgets to put a blank line at the end...
    if lines:
        yield lines


def main(args: argparse.Namespace) -> None:
    random.seed(a=args.seed)
    corpus = list(read_tags(args.input))
    randomizedCorpus = random.sample(corpus, len(corpus))

    eightyPercent = int(len(corpus) * 0.8)
    tenPercent = int(len(corpus) * 0.1)

    trainFile = randomizedCorpus[: eightyPercent]
    devFile = randomizedCorpus[eightyPercent: eightyPercent + tenPercent]
    testFile = randomizedCorpus[eightyPercent + tenPercent:]

    trainTokens = 0
    f = open(args.train, "w")
    for sent in trainFile:
        f.write(str(sent) + "\n")
        for tok in sent:
            trainTokens += 1

    devTokens = 0
    f = open(args.dev, "w")
    for sent in devFile:
        f.write(str(sent) + "\n")
        for tok in sent:
            devTokens += 1

    testTokens = 0
    f = open(args.test, "w")
    for sent in testFile:
        f.write(str(sent) + "\n")
        for tok in sent:
            testTokens += 1

    corpusTokens = 0
    for sent in corpus:
        for tok in sent:
            corpusTokens += 1

    print(
        f"{args.train} \n \t"
        f"Number of sentences: {len(trainFile)} \n \t"
        f"Number of tokens: {trainTokens}"
    )
    print(
        f"{args.dev} \n \t"
        f"Number of sentences: {len(devFile)} \n \t"
        f"Number of tokens: {devTokens}"
    )
    print(
        f"{args.test} \n \t"
        f"Number of sentences: {len(testFile)} \n \t"
        f"Number of tokens: {testTokens}"
    )
    print(
        f"{args.input} (main input) \n \t"
        f"Total number of sentences: {len(corpus)} \n \t"
        f"Total number of tokens: {corpusTokens}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Enter file name for input.")
    parser.add_argument(
        "--seed", type=int, required=True, help="Specify a seed."
    )
    parser.add_argument(
        "train", help="Enter file name to output lines into (i.e. 'train.tag')"
    )
    parser.add_argument(
        "dev", help="Enter file name to output lines into (i.e. 'dev.tag')"
    )
    parser.add_argument(
        "test", help="Enter file name to output lines into (i.e. 'test.tag')"
    )

    args = parser.parse_args()
    main(args)
