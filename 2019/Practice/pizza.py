import math
import sys


# Returns: number of rows, number of columns, minimum number of each ingredient cells in a slice, maximum number of cells in a slice
def getParams():
    return map(int, sys.stdin.readline().split())


def getPizza():
    pizza = []
    for row in sys.stdin:
        toAppend = []
        for cell in row:
            toAppend.append(cell)
        pizza.append(toAppend[: len(toAppend) - 1])
    return pizza


def printSlices(S, slices):
    print(S)
    for slice in slices:
        r1, c1, r2, c2 = slice
        print(r1, c1, r2, c2)


def countTM(pizza):
    T, M = 0, 0
    for row in pizza:
        for cell in row:
            if cell == "T":
                T += 1
            else:
                M += 1

    return T, M


def factorize(N):
    n = N
    factors = set()
    factors.add(1)
    while n % 2 == 0:
        factors.add(2)
        n //= 2

    cur_num = 3
    while cur_num**2 <= n:
        if n % cur_num == 0:
            factors.add(cur_num)
            n //= cur_num
        else:
            cur_num += 2

    if len(factors) == 1:
        factors.add(n)

    if n > 1:
        factors.add(n)

    return factors


def getSliceShapes(L, H):
    factors = factorize(H)
    shapes = []
    for x in factors:
        for y in factors:
            if x * y >= L and x * y <= H:
                shapes.append((x, y))
    return shapes


def cutSlices(pizza, R, C, L, H):
    T, M = countTM(pizza)
    maxNSlices = math.floor(min(T / L, M / L))
    sliceShapes = getSliceShapes(L, H)

    ###

    slices = []

    return len(slices), slices


def main():
    R, C, L, H = getParams()
    pizza = getPizza()

    S, slices = cutSlices(pizza, R, C, L, H)

    printSlices(S, slices)


main()
