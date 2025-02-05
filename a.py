with open('a.txt') as fd:
    print(sum(map(float, fd.readlines())))