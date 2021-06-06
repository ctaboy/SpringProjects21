#!/usr/bin/env python
"""French G2P conversion evaluation."""

import french_g2p


def main():
    with open("fre_dev.tsv", "r") as source:
        i = 0
        error_list = []
        correct_list = []
        for pair in source:
            split_pair = pair.split("\t")
            fre_word = split_pair[0]
            fre_ipa = split_pair[1].replace(" ", "").rstrip()
            ostring = french_g2p.g2p(fre_word)
            if ostring != fre_ipa:
                error_list.append(f"{fre_ipa} ≠ {ostring}")
            else:
                correct_list.append(f"{fre_ipa} = {ostring}")
            i += 1
        print(f"Correct: {len(correct_list)}/{i}")
        print(f"Accuracy: {len(correct_list)/i}")


if __name__ == "__main__":
    main()
