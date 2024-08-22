import sys


def readInput():
    libraries = []
    _, _, totalDays = list(map(int, sys.stdin.readline().split()))
    bookPoints = list(map(int, sys.stdin.readline().split()))
    i = 0
    while True:
        l1 = list(map(int, sys.stdin.readline().split()))
        l2 = list(map(int, sys.stdin.readline().split()))
        if not l2:
            break
        nB, nD, nBD = l1
        libBooks = sorted(l2, key=lambda x: bookPoints[x], reverse=True)
        libraries.append([i, int(nD), int(nBD), libBooks, -1])
        i += 1

    return libraries, totalDays, bookPoints


def pointsInLife(totalDays, nD, nBD, books, bookPoints):
    numBooks = (totalDays - nD) * nBD
    points = 0
    for book in books[: min(numBooks, len(books))]:
        points += bookPoints[book]
    return points, books[: min(numBooks, len(books))]


def removeBooks(booksProcessed, libraries):
    for lib in libraries:
        lib[3] = [x for x in lib[3] if x not in booksProcessed]


def main():
    libraries, totalDays, bookPoints = readInput()
    res = []
    daysLeft = totalDays
    while len(libraries) > 0 and daysLeft > 0:
        for lib in libraries:
            points, books = pointsInLife(daysLeft, lib[1], lib[2], lib[3], bookPoints)
            lib[3] = books
            lib[4] = points
        bestLib = max(libraries, key=lambda x: x[4])

        if bestLib[4] == 0:
            break

        res.append((bestLib[0], bestLib[3]))

        libraries.remove(bestLib)

        removeBooks(bestLib[3], libraries)
        daysLeft -= bestLib[1]  # Remove signup days from total time

    # Print result
    print(len(res))
    for library in res:
        print(str(library[0]) + " " + str(len(library[1])))
        print(" ".join(list(map(str, library[1]))))


main()
