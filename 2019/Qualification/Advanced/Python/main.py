import concurrent.futures
import math
import multiprocessing
import sys

from interest import *


# Join the vertical photos in pairs of two
def join_verticals(verticais, fotos):
    verticais = sorted(verticais, key=lambda x: len(fotos[x]), reverse=True)

    return [(verticais[i], verticais[i + 1]) for i in range(0, len(verticais), 2)]


# Build the interests matrix
def constroiMatriz(fotos):
    res = {}

    listFotos = list(fotos.items())
    listFotosLen = len(listFotos)

    for f1 in range(listFotosLen):
        fotoF1 = listFotos[f1][0]
        res[fotoF1] = []
        for f2 in range(f1 + 1, listFotosLen):
            fotoF2 = listFotos[f2][0]
            res[fotoF1].append((fotoF2, interest(fotos[fotoF1], fotos[fotoF2])))
        res[fotoF1] = sorted(res[fotoF1], key=lambda x: x[1])

    return res


# Function used by the processes to build their part of the matrix
def buildMatrixOneCore(work):
    begin, end, fotos, resultQueue = work

    res = {}
    listFotos = list(fotos.items())
    listFotosLen = len(listFotos)

    for f1 in range(begin, end):
        fotoF1 = listFotos[f1][0]
        res[fotoF1] = []
        for f2 in range(f1 + 1, listFotosLen):
            fotoF2 = listFotos[f2][0]
            res[fotoF1].append((fotoF2, interest(fotos[fotoF1], fotos[fotoF2])))
        res[fotoF1] = sorted(res[fotoF1], key=lambda x: x[1])

    resultQueue.put(res)


def main():
    # Process the input received from the standard input
    fotos = {}
    verticais = []
    count = 0

    int(sys.stdin.readline())  # Ignore the first line (N)
    for l in sys.stdin:
        x = list(l.split())
        fotos[count] = set(x[2:])
        if x[0] is "V":
            verticais.append(count)
        count += 1

    # Create vertical pairs, add them to the photos' dictionary and removed the verticals from there
    paresVerticais = join_verticals(verticais, fotos)
    for a, b in paresVerticais:
        fotos[(a, b)] = union(fotos[a], fotos[b])
        del fotos[a]
        del fotos[b]

    # Put the cores to work on the matrix
    cores = multiprocessing.cpu_count()
    lenFotos = len(fotos)
    mat = {}
    if lenFotos < cores:
        # Build the matrix using only one core
        mat = constroiMatriz(fotos)
    else:
        numLinesPerCore = math.floor(lenFotos / cores)
        resultQueue = multiprocessing.SimpleQueue()
        processes = []
        for i in range(cores):
            p = multiprocessing.Process(
                target=buildMatrixOneCore,
                args=(
                    (
                        i * numLinesPerCore,
                        (i + 1) * numLinesPerCore,
                        fotos,
                        resultQueue,
                    ),
                ),
            )
            processes.append(p)
            p.start()

        if lenFotos % cores != 0:
            # Add the remaining elements from the division of the lines by the cores
            p = multiprocessing.Process(
                target=buildMatrixOneCore,
                args=((numLinesPerCore * cores, lenFotos, fotos, resultQueue),),
            )
            processes.append(p)
            p.start()

        for p in processes:
            mat.update(resultQueue.get())

    # Compose the slideshow
    slideshow = solve_v2(mat)

    # Print the result to the standard output
    print(len(slideshow))
    for x in slideshow:
        try:
            a, b = x
            print(a, b)
        except:
            print(x)


if __name__ == "__main__":
    main()
