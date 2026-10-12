import sys


def main():
    # Read input
    A = [int(line) for line in sys.stdin]

    insertionsort(A)

    # Print result
    for num in A:
        print(num)


def insertionsort(A):
    pass  # <- Skriv her


if __name__ == "__main__":
    main()
