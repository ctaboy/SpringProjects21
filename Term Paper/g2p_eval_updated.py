#!/usr/bin/env python
"""French G2P conversion evaluation."""

import french_g2p


def main():
    with open("fre_dev.tsv", "r") as source:
        i = 0
        error = 0
        correct = 0
        for pair in source:
            split_pair = pair.split("\t")
            fre_word = split_pair[0]
            fre_ipa = split_pair[1].replace(" ", "").rstrip()
            ostring = french_g2p.g2p(fre_word)
            if ostring != fre_ipa:
                error += 1
            else:
                correct += 1
            i += 1
        print(f"Correct: {correct}/{i}")
        print(f"Errors: {error}/{i}")
        print(f"Accuracy: {correct/i}")
        print(f"WER: {(error/i)*100}")


if __name__ == "__main__":
    main()
