# coding=utf-8
import math
import fileinput
import re
import pickle
import time
import sys
from pylab import *
import matplotlib.pyplot as pyplot

rules = list()
rules_term = list()
terminals = set()
result_lines = []
"""
function PROBABILISTIC-CKY(words,grammar) returns most probable parse
and its probability
for j←from 1 to LENGTH(words) do
    for all { A | A → words[ j] ∈ grammar}
        table[j −1, j,A]←P(A → words[ j])
    for i←from j −2 down to 0 do
        for k←i+1 to j −1 do
            for all { A | A → BC ∈ grammar, and table[i, k,B] > 0 and table[k, j,C] > 0 }
            if (table[i,j,A] < P(A → BC) × table[i,k,B] × table[k,j,C]) then
                table[i,j,A]←P(A → BC) × table[i,k,B] × table[k,j,C]
                    back[i,j,A]← {k,B,C}
    return BUILD TREE(back[1, LENGTH(words), S]), table[1, LENGTH(words), S]

"""


def r_gram(w, back, i, j):
    l = back[i][j][w]
    if len(l) == 1:
        return str("(" + w + " " + l[0] + ")")
    k = l[0]
    left = r_gram(l[1], back, i, k)
    right = r_gram(l[2], back, k, j)
    return "(" + w + " " + left + " " + right + ")"


def print_grammar(table, back, l):
    stats = table[0][l - 1]
    if not stats:
        result = " "
    else:
        S = max(stats, key=stats.get)
        result = r_gram(S, back, 0, l - 1)
    result_lines.append(result)
    print result
    # print "The grammar is : {0} and its log probability is {1}".format(result, stats[S])


def prob(word, bool):
    result = dict()
    if not bool:
        for i in rules_term:
            if word == i[1]:
                result[i[0]] = i[2]
    else:
        for i in rules:
            if word == i[1]:
                result[i[0]] = i[2]
    return result


def cky(words):
    words = [0] + words
    table = [[{} for _ in xrange(len(words))] for i in xrange(len(words) - 1)]
    back = [[{} for _ in xrange(len(words))] for i in xrange(len(words) - 1)]
    # print table
    # back = list(list())
    for j in xrange(1, len(words)):
        word = words[j]
        if not words[j] in terminals:
            word = "<unk>"
        table[j - 1][j] = prob(word, False)
        # back[0][1][word] = table[j-1][j]
        result = dict()
        for keys in table[j - 1][j]:
            result[keys] = [word]

        back[j - 1][j].update(result)

        for i in xrange(j - 2, -1, -1):
            for k in xrange(i + 1, j):
                for e in rules:
                    A, B, C = e[0], e[1].split()[0], e[1].split()[1]
                    if table[i][k].get(B, 10) != 10 and table[k][j].get(C, 10) != 10:
                        res = e[2] + table[i][k].get(B, 0) + table[k][j].get(C, 0)
                        if table[i][j].get(A, float("-inf")) < res:
                            table[i][j][A] = res
                            back[i][j][A] = [k, B, C]

    print_grammar(table, back, len(words))


if __name__ == "__main__":
    for line in fileinput.input(sys.argv[1]):
        x, y, p = re.split('->|#', line.strip())
        # print x.strip(),y.strip(),p.strip()
        temp = y.strip().split(" ")
        if len(temp) < 2:
            terminals.add(y.strip())
            rules_term.append([x.strip(), y.strip(), math.log10(float(p.strip()))])
        else:
            rules.append([x.strip(), y.strip(), math.log10(float(p.strip()))])

    Line = list()
    Time = list()

    for line in fileinput.input(sys.argv[2]):
        start = time.clock()
        cky(line.strip().split())
        elapsed = (time.clock() - start)
        Time.append(elapsed)
        Line.append(len(line.strip().split()))

    Time = [i*1000 for i in Time]
    pyplot.plot(Line, Time, "o")
    #plot.title("Parsing Time vs Sentence Length(log Scaled)")
    plot.xlabel('No of words')
    plot.ylabel('Time')
    pyplot.xscale('log')
    pyplot.yscale('log')
    show()

    # with open("dev.parses", "w") as f:
    #     f.writelines(result_lines)
