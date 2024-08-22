from interest import interest, union
import sys

def main():
    fotos = []
    score = 0
    count = 0

    int(sys.stdin.readline())
    for l in sys.stdin:
        x = list(l.split())
        fotos.append(set(x[2:]))

    file = sys.argv[1]
    with open(file) as output:
        int(output.readline())
        prev = list(map(int, output.readline().split()))
        for line in output:
            line = list(map(int, line.split()))
            count += 1
            if len(prev) == 2:
                tagsPrev = union(fotos[prev[0]], fotos[prev[1]])
                if len(line) == 2:
                    score += interest(tagsPrev, union(fotos[line[0]], fotos[line[1]]))
                else:
                    score += interest(tagsPrev, fotos[line[0]])
            elif len(line) == 2:
                score += interest(fotos[prev[0]], union(fotos[line[0]], fotos[line[1]]))
            else:
                score += interest(fotos[prev[0]], fotos[line[0]])
            
            prev = line
    
    print(score)



main()