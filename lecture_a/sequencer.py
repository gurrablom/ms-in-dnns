import argparse
import math


def main(args):
    sequence = []

    if args.sequence == "fibonacci":
        a, b = 0, 1
        for _ in range(args.length):
            sequence.append(a)
            a, b = b, a + b
    elif args.sequence == "prime":
        current_number = 2
        while len(sequence) < args.length:
            if all(current_number % i != 0 for i in range(2, int(math.sqrt(current_number)) + 1)):
                sequence.append(current_number)
            current_number += 1
    elif args.sequence == "square":
        for i in range(1, args.length + 1):
            sequence.append(i**2)
    elif args.sequence == "triangular":
        current_sum = 0
        for i in range(1, args.length + 1):
            current_sum += i
            sequence.append(current_sum)
    elif args.sequence == "factorial":
        for i in range(1, args.length + 1):
            if i == 1:
                sequence.append(1)
            else:
                sequence.append(sequence[i - 2] * i)
    else:
        raise ValueError("Invalid sequence type")

    return sequence


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compute well-known mathematical sequences iteratively."
    )
    parser.add_argument("--length", type=int, required=True, help="Length of the computed sequence")
    parser.add_argument(
        "--sequence",
        type=str,
        required=True,
        choices=["fibonacci", "prime", "square", "triangular", "factorial"],
        help="Name of the sequence",
    )

    args = parser.parse_args()
    result_sequence = main(args)
    print(result_sequence)
