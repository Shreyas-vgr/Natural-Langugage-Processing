# coding=utf-8
from collections import Counter

from tree import Tree
import fileinput
import sys

rules = dict()


def count_rules(nodes):
    for node in nodes:
        if node.children:
            parent = node.label.strip()
            s = Counter()
            tmp = ''
            for i in node.children:
                tmp += i.label.strip() + " "
            s[tmp] += 1
            if parent in rules:
                rules[parent] += s
            else:
                rules[parent] = s

            # s = (node.label.strip(),)
            # if len(node.children) < 2:
            #     terminals.add(node.children[0].label.strip())
            # for i in node.children:
            #     s += (i.label.strip(),)
            # if s in rules:
            #     rules[s] += 1
            # else:
            #     rules[s] = 1




def write_to_file():
    with open("q1.output", 'w') as f:
        for key, value in rules.iteritems():
            deno = (sum(value.values()) * 1.0)
            for i in dict(value):
                print(str(key) + " -> " + str() + str(i) + " # " + str(dict(value)[i] / deno))
    f.close()


if __name__ == "__main__":
    for line in fileinput.input(sys.argv[1]):
        t = Tree.from_str(line)
        nodes = list(t.bottomup())
        count_rules(nodes)
    #print rules
    max_value = 0
    fq_rule = list()
    total_no_rules = 0
    for key, item in rules.iteritems():
        if item.most_common(1)[0][1] > max_value:
            max_value = item.most_common(1)[0][1]
            fq_rule = [key, item.most_common(1)]
        total_no_rules += len(item)

    # print "No of rules of grammar : ", total_no_rules
    # print "Most frequent rule " + fq_rule[0] + " -> " + str(fq_rule[1][0][0]) + " and its occurance " + str(fq_rule[1][0][1])

    # write to file q1.output
    write_to_file()

