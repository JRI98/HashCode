import sys


def readInput():
    libraries = []
    numBooks, _, totalDays = list(map(int, sys.stdin.readline().split()))
    bookPoints = list(map(int, sys.stdin.readline().split()))
    booksDict = [0] * numBooks
    i = 0
    while True:
        l1 = list(map(int, sys.stdin.readline().split()))
        l2 = list(map(int, sys.stdin.readline().split()))
        if not l2:
            break
        nB, nD, nBD = l1
        libBooks = sorted(l2, key=lambda x: bookPoints[x], reverse=True)
        for book in libBooks:
            booksDict[book] += 1
        libraries.append([i, int(nD), int(nBD), libBooks, -1, -1])
        i += 1

    print(booksDict)
    for i in range(len(booksDict)):
        if booksDict[i] != 0:
            booksDict[i] = 1 / booksDict[i]

    return libraries, totalDays, bookPoints, booksDict


def pointsInLife(totalDays, nD, nBD, books, bookPoints, booksDict):
    numBooks = (totalDays - nD) * nBD
    points = 0.0
    books2 = books[: min(numBooks, len(books))]
    for book in books2:
        points += bookPoints[book]
    l = len(books2)

    soma = 0
    for book in books2:
        soma += booksDict[book]

    if l == 0:
        return 0, 0

    return points / (l / nBD + nD) * (soma / len(books2)), l


def removeBooks(booksProcessed, libraries):
    for lib in libraries:
        lib[3] = [x for x in lib[3] if x not in booksProcessed]


def main():
    libraries, totalDays, bookPoints, booksDict = readInput()
    res = []
    daysLeft = totalDays
    while len(libraries) > 0 and daysLeft > 0:
        for lib in libraries:
            points, numBooks = pointsInLife(
                daysLeft, lib[1], lib[2], lib[3], bookPoints, booksDict
            )
            lib[4] = points
            lib[5] = numBooks
        bestLib = max(libraries, key=lambda x: x[4])

        if bestLib[4] == 0:
            break

        res.append((bestLib[0], bestLib[3][: bestLib[5]]))

        libraries.remove(bestLib)

        removeBooks(bestLib[3], libraries)
        daysLeft -= bestLib[1]  # Remove signup days from total time

    # Print result
    print(len(res))
    for library in res:
        print(str(library[0]) + " " + str(len(library[1])))
        print(" ".join(list(map(str, library[1]))))


main()
