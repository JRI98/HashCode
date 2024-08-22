import sys


def readInput():
    libraries = []
    sys.stdin.readline()
    bookPoints = list(map(int, sys.stdin.readline().split()))
    while True:
        l1 = list(map(int, sys.stdin.readline().split()))
        l2 = list(map(int, sys.stdin.readline().split()))
        if not l2:
            break
        nB, nD, nBD = l1
        libBooks = sorted(l2, key=lambda x: bookPoints[x])
        libraries.append((int(nD), int(nBD), libraries))


readInput()
