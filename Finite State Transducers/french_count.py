import sys
from fst import FST
from fsmutils import composewords, trace

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)


def french_count():
    f = FST('french')

    f.add_state('start')
    f.add_state('a')
    f.add_state('a1')
    f.add_state('b0')
    f.add_state('b')
    f.add_state('b1')
    f.add_state('b2')
    f.add_state('b3')
    f.add_state('b4')
    f.add_state('b5')
    f.add_state('b6')
    f.add_state('b7')
    f.add_state('b8')
    f.add_state('b9')

    f.add_state('c')
    f.initial_state = 'start'
    f.set_final('c')

    f.add_arc('start', 'a', ['0'], [])
    f.add_arc('start', 'a1', ['1'], [kFRENCH_TRANS[100]])
    f.add_arc('start', 'a1', ['2'], [kFRENCH_TRANS[2] + " " + kFRENCH_TRANS[100]])
    f.add_arc('start', 'a1', ['3'], [kFRENCH_TRANS[3] + " " + kFRENCH_TRANS[100]])
    f.add_arc('start', 'a1', ['4'], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[100]])
    f.add_arc('start', 'a1', ['5'], [kFRENCH_TRANS[5] + " " + kFRENCH_TRANS[100]])
    f.add_arc('start', 'a1', ['6'], [kFRENCH_TRANS[6] + " " + kFRENCH_TRANS[100]])
    f.add_arc('start', 'a1', ['7'], [kFRENCH_TRANS[7] + " " + kFRENCH_TRANS[100]])
    f.add_arc('start', 'a1', ['8'], [kFRENCH_TRANS[8] + " " + kFRENCH_TRANS[100]])
    f.add_arc('start', 'a1', ['9'], [kFRENCH_TRANS[9] + " " + kFRENCH_TRANS[100]])

    f.add_arc('a', 'b0', ['0'], [])

    f.add_arc('a', 'b1', ['1'], [])
    f.add_arc('a', 'b2', ['2'], [])
    f.add_arc('a', 'b3', ['3'], [])
    f.add_arc('a', 'b4', ['4'], [])
    f.add_arc('a', 'b5', ['5'], [])
    f.add_arc('a', 'b6', ['6'], [])
    f.add_arc('a', 'b7', ['7'], [kFRENCH_TRANS[60]])
    f.add_arc('a', 'b8', ['8'], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])
    f.add_arc('a', 'b9', ['9'], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])

    f.add_arc('a1', 'b', ['0'], [])
    f.add_arc('a1', 'b1', ['1'], [])
    f.add_arc('a1', 'b2', ['2'], [])
    f.add_arc('a1', 'b3', ['3'], [])
    f.add_arc('a1', 'b4', ['4'], [])
    f.add_arc('a1', 'b5', ['5'], [])
    f.add_arc('a1', 'b6', ['6'], [])
    f.add_arc('a1', 'b7', ['7'], [kFRENCH_TRANS[60]])
    f.add_arc('a1', 'b8', ['8'], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])
    f.add_arc('a1', 'b9', ['9'], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])

    f.add_arc('b', 'c', ['0'], [])
    f.add_arc('b2', 'c', ['0'], [kFRENCH_TRANS[20]])
    f.add_arc('b3', 'c', ['0'], [kFRENCH_TRANS[30]])
    f.add_arc('b4', 'c', ['0'], [kFRENCH_TRANS[40]])
    f.add_arc('b5', 'c', ['0'], [kFRENCH_TRANS[50]])
    f.add_arc('b6', 'c', ['0'], [kFRENCH_TRANS[60]])
    f.add_arc('b7', 'c', ['0'], [kFRENCH_TRANS[10]])
    f.add_arc('b8', 'c', ['0'], [])
    f.add_arc('b9', 'c', ['0'], [kFRENCH_TRANS[10]])

    for ii in xrange(10):
        f.add_arc('b0', 'c', [str(ii)], [kFRENCH_TRANS[ii]])
        if ii < 7:
            f.add_arc('b1', 'c', [str(ii)], [kFRENCH_TRANS[10 + ii]])
            f.add_arc('b7', 'c', [str(ii)], [kFRENCH_TRANS[10 + ii]])
            f.add_arc('b9', 'c', [str(ii)], [kFRENCH_TRANS[10 + ii]])

        else:
            f.add_arc('b1', 'c', [str(ii)], [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[ii]])
            f.add_arc('b7', 'c', [str(ii)], [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[ii]])
            f.add_arc('b9', 'c', [str(ii)], [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[ii]])

        if ii != 0:
            f.add_arc('b', 'c', [str(ii)], [kFRENCH_TRANS[ii]])
            f.add_arc('b2', 'c', [str(1)], [kFRENCH_TRANS[20] + " " + kFRENCH_AND + " " + kFRENCH_TRANS[1]])
            f.add_arc('b3', 'c', [str(1)], [kFRENCH_TRANS[30] + " " + kFRENCH_AND + " " + kFRENCH_TRANS[1]])
            f.add_arc('b4', 'c', [str(1)], [kFRENCH_TRANS[40] + " " + kFRENCH_AND + " " + kFRENCH_TRANS[1]])
            f.add_arc('b5', 'c', [str(1)], [kFRENCH_TRANS[50] + " " + kFRENCH_AND + " " + kFRENCH_TRANS[1]])
            f.add_arc('b6', 'c', [str(1)], [kFRENCH_TRANS[60] + " " + kFRENCH_AND + " " + kFRENCH_TRANS[1]])
            f.add_arc('b7', 'c', [str(1)], [kFRENCH_AND + " " + kFRENCH_TRANS[11]])

            f.add_arc('b2', 'c', [str(ii)], [kFRENCH_TRANS[20] + " " + kFRENCH_TRANS[ii]])
            f.add_arc('b3', 'c', [str(ii)], [kFRENCH_TRANS[30] + " " + kFRENCH_TRANS[ii]])
            f.add_arc('b4', 'c', [str(ii)], [kFRENCH_TRANS[40] + " " + kFRENCH_TRANS[ii]])
            f.add_arc('b5', 'c', [str(ii)], [kFRENCH_TRANS[50] + " " + kFRENCH_TRANS[ii]])
            f.add_arc('b6', 'c', [str(ii)], [kFRENCH_TRANS[60] + " " + kFRENCH_TRANS[ii]])

            f.add_arc('b8', 'c', [str(ii)], [kFRENCH_TRANS[ii]])
    return f


if __name__ == '__main__':
    for i in xrange(1000):
        string_input = str(i)
        user_input = int(string_input)
        f = french_count()
        if string_input:
            print user_input, '-->',
            print " ".join(f.transduce(prepare_input(user_input)))
