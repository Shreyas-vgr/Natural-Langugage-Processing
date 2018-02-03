#!/usr/bin/env python

import sys, fileinput
from tree import Node
import tree


def head_lexicalization(t):

    nodes = list(t.bottomup())
    for node in nodes:
        if len(list(node.children)) > 1:
            children = list(node.children)
            if children[0].label[-1] == '*':
                children[0].label = children[0].label + "&&&" + children[1].label


for line in fileinput.input():
    t = tree.Tree.from_str(line)

    # Binarize, inserting 'X*' nodes.
    t.binarize()

    head_lexicalization(t)

    # Remove unary nodes
    t.remove_unit()

    # The tree is now strictly binary branching, so that the CFG is in Chomsky normal form.

    # Make sure that all the roots still have the same label.
    assert t.root.label == 'TOP'

    print t

