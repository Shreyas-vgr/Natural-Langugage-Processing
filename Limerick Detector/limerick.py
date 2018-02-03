#!/usr/bin/env python
import argparse
import sys
import codecs

if sys.version_info[0] == 2:
    from itertools import izip
else:
    izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit
# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize

scriptdir = os.path.dirname(os.path.abspath(__file__))

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')


def prepfile(fh, code):
    if type(fh) is str:
        fh = open(fh, code)
    ret = gzip.open(fh.name, code if code.endswith("t") else code + "t") if fh.name.endswith(".gz") else fh
    if sys.version_info[0] == 2:
        if code.startswith('r'):
            ret = reader(fh)
        elif code.startswith('w'):
            ret = writer(fh)
        else:
            sys.stderr.write("I didn't understand code " + code + "\n")
            sys.exit(1)
    return ret


def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
    ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
    group = parser.add_mutually_exclusive_group()
    dest = arg if dest is None else dest
    group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
    group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)


class LimerickDetector:
    def __init__(self):
        """
		Initializes the object to have a pronunciation dictionary available
		"""
        self._pronunciations = nltk.corpus.cmudict.dict()

    def num_syllables(self, word):
        """
		Returns the number of syllables in a word.  If there's more than one
		pronunciation, take the shorter one.  If there is no entry in the
		dictionary, return 1.
		"""

        # TODO: provide an implementation!
        #return self.guess_syllables(word)
        if word.lower() in self._pronunciations:
            pronunciation = (self._pronunciations[word.lower()])
            sorted(pronunciation, key=len)
            no_of_syllables = [y for y in pronunciation[0] if y[-1].isdigit()]
            if len(no_of_syllables) > 0:
                return len(no_of_syllables)
            else:
                return 1
        else:
            return 1

    def rhymes(self, a, b):
        """
		Returns True if two words (represented as lower-case strings) rhyme,
		False otherwise.
		"""

        # TODO: provide an implementation!
        if a.lower() in self._pronunciations:
            syllable_a = self._pronunciations[a.lower()]
        else:
            return False

        if b.lower() in self._pronunciations:
            syllable_b = self._pronunciations[b.lower()]
        else:
            return False

        new_syllable_a = list()
        for i in syllable_a:
            for index, e in enumerate(i):
                if e[0] in "AEIOU":
                    new_syllable_a.append(i[index:])
                    break

        new_syllable_b = list()
        for i in syllable_b:
            for index, e in enumerate(i):
                if e[0] in "AEIOU":
                    new_syllable_b.append(i[index:])
                    break

        if not new_syllable_a or not new_syllable_b:
            return True

        success = False
        for i in new_syllable_a:
            for j in new_syllable_b:
                if len(i) == len(j):
                    result = len(i) == len(j) and len(i) == sum([1 for p, k in zip(i, j) if p == k])
                    if result:
                        return True
                        # success = result
                else:
                    if len(i) > len(j):
                        n = len(j)
                        success = any((j == i[s:s + n]) for s in xrange(1, len(i) - n + 1))
                        if success:
                            return True
                    else:
                        n = len(i)
                        success = any((i == j[s:s + n]) for s in xrange(1, len(j) - n + 1))
                        if success:
                            return True

        return success

    def is_limerick(self, text):
        """
		Takes text where lines are separated by newline characters.  Returns
		True if the text is a limerick, False otherwise.

		A limerick is defined as a poem with the form AABBA, where the A lines
		rhyme with each other, the B lines rhyme with each other, and the A lines do not
		rhyme with the B lines.


		Additionally, the following syllable constraints should be observed:
		  * No two A lines should differ in their number of syllables by more than two.
		  * The B lines should differ in their number of syllables by no more than two.
		  * Each of the B lines should have fewer syllables than each of the A lines.
		  * No line should have fewer than 4 syllables

		(English professors may disagree with this definition, but that's what
		we're using here.)


		"""
        # TODO: provide an implementation!

        lines = text.strip().split("\n")

        if len(lines) < 5 or len(lines) > 5:
            return False

        A1 = [v for v in word_tokenize(lines[0]) if v not in punctuation]
        A2 = [v for v in word_tokenize(lines[1]) if v not in punctuation]
        B1 = [v for v in word_tokenize(lines[2]) if v not in punctuation]
        B2 = [v for v in word_tokenize(lines[3]) if v not in punctuation]
        A3 = [v for v in word_tokenize(lines[4]) if v not in punctuation]

        if not self.rhymes(B1[-1], B2[-1]):
            return False
        if not (self.rhymes(A1[-1], A2[-1]) and self.rhymes(A1[-1], A3[-1]) and self.rhymes(A2[-1], A3[-1])):
            return False

        syllable_A1 = sum(map(lambda x: self.num_syllables(x), A1))
        if syllable_A1 < 4:
            return False

        syllable_A2 = sum(map(lambda x: self.num_syllables(x), A2))
        if syllable_A2 < 4:
            return False

        syllable_B1 = sum(map(lambda x: self.num_syllables(x), B1))
        if syllable_B1 < 4:
            return False

        syllable_B2 = sum(map(lambda x: self.num_syllables(x), B2))
        if syllable_B2 < 4:
            return False

        syllable_A3 = sum(map(lambda x: self.num_syllables(x), A3))
        if syllable_A3 < 4:
            return False

        if abs(syllable_B1 - syllable_B2) > 2:
            return False

        min_syllable_A = min(syllable_A1, syllable_A2, syllable_A3)

        if (syllable_B1 > min_syllable_A) or (syllable_B2 > min_syllable_A):
            return False

        # cond 1
        if (abs(syllable_A1 - syllable_A2) > 2) or (abs(syllable_A1 - syllable_A3) > 2) or \
                (abs(syllable_A2 - syllable_A3) > 2):
            return False

        return True

    def apostrophe_tokenize(self, text):
        lines = text.strip().split(" ")
        lines = [w.replace("'", "").replace(".", "").replace('"', '').replace(",", "").replace(":", "").replace(";", "").replace("!", "") for w in lines]
        return lines

    def guess_syllables(self, word):
        prev = False
        count = 0
        for i in xrange(len(word) - 1):
            if word[i] in "aeiou" and not prev:
                count += 1
                prev = True
            else:
                prev = False
        return count


# The code below should not need to be modified
def main():
    parser = argparse.ArgumentParser(
        description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    addonoffarg(parser, 'debug', help="debug mode", default=False)
    parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
    parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                        help="output file")

    try:
        args = parser.parse_args()
    except IOError as msg:
        parser.error(str(msg))

    infile = prepfile(args.infile, 'r')
    outfile = prepfile(args.outfile, 'w')

    ld = LimerickDetector()
    lines = ''.join(infile.readlines())
    outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))


if __name__ == '__main__':
    main()
