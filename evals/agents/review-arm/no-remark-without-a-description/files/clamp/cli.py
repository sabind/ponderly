import argparse

from clamp.core import DEFAULT_HIGH, DEFAULT_LOW, clamp


def main(argv=None):
    parser = argparse.ArgumentParser(prog="clamp", description="Keep a number inside a range.")
    parser.add_argument("value", type=float, help="the number to clamp")
    parser.add_argument("--low", type=float, default=DEFAULT_LOW, help="the smallest value returned")
    parser.add_argument("--high", type=float, default=DEFAULT_HIGH, help="the largest value returned")
    args = parser.parse_args(argv)
    print(clamp(args.value, args.low, args.high))


if __name__ == "__main__":
    main()
