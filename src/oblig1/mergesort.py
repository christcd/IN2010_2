
import sys


def main():
    # Read input
    A = [int(line) for line in sys.stdin]

    A = mergesort(A)

    # Print result
    for num in A:
        print(num)


def mergesort(A):
    return A  # <- Skriv her


if __name__ == "__main__":
    main()
