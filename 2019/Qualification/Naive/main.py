import sys

N = int(sys.stdin.readline())

fotos = {}

verticais = []
horizontais = []


def join_verticals(verticais):
    verticais = sorted(verticais, key=lambda x: len(fotos[x]), reverse=True)

    return [(verticais[i], verticais[i + 1]) for i in range(0, len(verticais), 2)]


def union(tags1, tags2):
    return list(set().union(tags1, tags2))


# Read Input
count = 0
for l in sys.stdin:
    x = list(l.split())
    fotos[count] = x[2:]
    if x[0] == "H":
        horizontais.append(count)
    else:
        verticais.append(count)
    count += 1


paresVerticais = join_verticals(verticais)
for a, b in paresVerticais:
    fotos[(a, b)] = union(fotos[a], fotos[b])


slideshow = sorted(
    horizontais + paresVerticais, key=lambda x: len(fotos[x]), reverse=True
)

# Print output
print(len(slideshow))
for x in slideshow:
    try:
        a, b = x
        print(a, b)
    except:
        print(x)
