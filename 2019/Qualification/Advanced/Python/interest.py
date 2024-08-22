# Return the union between two lists of tags
def union(tags1, tags2):
    return tags1 | tags2


# Return the number of common tags between two lists of tags
def numCommon(tags1, tags2):
    return len(tags1 & tags2)


# Return the interest between two lists of tags
def interest(tags1, tags2):
    commonTags = numCommon(tags1, tags2)
    return min(len(tags2) - commonTags, commonTags, len(tags1) - commonTags)


# Return the key/value that owns the maximum interest in the matrix and delete that key from the matrix.
# It is guaranteed that the returned key is not already in the slideshow
def globalMaxKey(mat, matItems):
    bestValue = (-1, -1)
    bestKey = None

    for k, v in matItems:
        while len(v) > 0:
            biggestInterestPair = v[
                -1
            ]  # biggestInterestPair = (photoID, interest(k, photoID))
            # If the photo that owns this interest is already in the slideshow, delete this entry
            if biggestInterestPair[0] in mat:
                if biggestInterestPair[1] > bestValue[1]:
                    bestValue = biggestInterestPair
                    bestKey = k
                break

            del v[-1]

        if bestKey == None:
            bestKey = k

    if bestKey != None:
        del mat[bestKey]

    return bestKey, bestValue


# Return the slideshow that we think is the best, based on the interests matrix
def solve(mat):
    N = len(mat)
    matItems = mat.items()

    slideshow = [None] * (N * 2)
    begin = N - 1  # Aponta para o elemento mais à esquerda
    end = N  # Aponta para o elemento mais à direita

    # Adicionar o primeiro da esquerda e obter o próximo candidato
    toAddEsq, nextEsq = globalMaxKey(mat, matItems)
    slideshow[begin] = toAddEsq

    # Adicionar o primeiro da direita e obter o próximo candidato
    toAddDir, nextDir = globalMaxKey(mat, matItems)
    slideshow[end] = toAddDir

    # Iterar até o slideshow ter todas as fotos
    while end - begin + 1 != N:
        if nextEsq[1] >= nextDir[1]:
            begin -= 1
            slideshow[begin] = nextEsq[0]

            if len(mat[nextEsq[0]]) == 0:
                del mat[nextEsq[0]]
                toAddEsq, nextEsq = globalMaxKey(mat, matItems)
                if toAddEsq == None:
                    continue
                begin -= 1
                slideshow[begin] = toAddEsq
            else:
                aux = nextEsq[0]
                nextEsq = mat[aux].pop()
                del mat[aux]
        else:
            end += 1
            slideshow[end] = nextDir[0]

            if len(mat[nextDir[0]]) == 0:
                del mat[nextDir[0]]
                i_dir, nextDir = globalMaxKey(mat, matItems)
                if i_dir == None:
                    continue
                end += 1
                slideshow[end] = i_dir
            else:
                aux = nextDir[0]
                nextDir = mat[aux].pop()
                del mat[aux]

    return slideshow[begin : end + 1]


def solve_v2(mat):
    N = len(mat)
    matItems = mat.items()

    slideshow = [None] * N
    end = 0  # Aponta para o elemento mais à direita

    # Adicionar o primeiro elemento e obter o próximo candidato
    toAdd, nxt = globalMaxKey(mat, matItems)
    slideshow[end] = toAdd

    # Iterar até o slideshow ter todas as fotos
    while end + 1 != N:
        end += 1
        slideshow[end] = nxt[0]
        if len(mat[nxt[0]]) == 0:
            del mat[nxt[0]]
            toAdd, nxt = globalMaxKey(mat, matItems)
            if toAdd == None:
                continue
            end += 1
            slideshow[end] = toAdd
        else:
            aux = nxt[0]
            nxt = mat[aux].pop()
            del mat[aux]

    return slideshow
