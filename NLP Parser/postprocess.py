#!/usr/bin/env python

import sys, fileinput
import tree

def remove_head_lexicalization(t):

    nodes = list(t.bottomup())
    for node in nodes:
        if len(list(node.children)) > 1:
            children = list(node.children)
            children[0].label = children[0].label.split("&&&")[0]


for line in fileinput.input():
    t = tree.Tree.from_str(line)
    if t.root is None:
        print
        continue
    t.restore_unit()
    remove_head_lexicalization(t)
    t.unbinarize()

    print t
    
    
