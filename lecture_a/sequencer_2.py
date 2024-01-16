import argparse


def generate_sequence(length, type):
    sequence = []

    if type == "fibonacci":
        a = 0
        b = 1
        for i in range(length):
            sequence.append(a)
            a = (b,)


def main():
    parse = argparse.Argumentparser(description="Generates some famous sequences")
    parser.add_argument("--length")
    parser.add_argument("--sequence")

    args = parser.parse_args()
    result = generate_sequence(args.length, args.sequence)
    print(result)
