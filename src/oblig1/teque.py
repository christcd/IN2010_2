from sys import stdin


class Teque:

    def __init__(self):
        pass

    def pushback(self, x):
        pass

    def pushfront(self, x):
        pass

    def pushmiddle(self, x):
        pass

    def get(self, i):
        pass


if __name__ == '__main__':
    teque = Teque()
    N = int(stdin.readline())
    for _ in range(N):
        line = stdin.readline().split()
        cmd = line[0]
        num = int(line[1])
        if cmd == "push_back":
            teque.pushback(num)
        elif cmd == "push_front":
            teque.pushfront(num)
        elif cmd == "push_middle":
            teque.pushmiddle(num)
        else:
            print(teque.get(num))
