#!/usr/bin/env python

import subprocess
import argparse


def main(args: argparse.Namespace) -> None:
    subprocess.check_call("ngramsymbols en.tok en.sym", shell=True)
    subprocess.check_call(
        "farcompilestrings --fst_type=compact --symbols=en.sym "
        "--keep_symbols en.tok en.far",
        shell=True,
    )
    subprocess.check_call(
        f"ngramcount --order={args.order} en.far en.cnt", shell=True
    )
    subprocess.check_call(
        f"ngrammake --method={args.method} en.cnt en.lm", shell=True
    )
    subprocess.check_call("ngraminfo en.lm", shell=True)
    subprocess.check_call(
        f"ngramrandgen --max_sents={args.example} en.lm | farprintstrings",
        shell=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("order", help="Specify nth order", type=int)
    parser.add_argument(
        "method", help="Specify smoothing method; e.g. kneser_ney"
    )
    parser.add_argument(
        "example", help="Specify number of example sentences", type=int
    )
    main(parser.parse_args())
