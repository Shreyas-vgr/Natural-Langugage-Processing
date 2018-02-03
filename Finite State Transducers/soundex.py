from fst import FST
import string, sys
from fsmutils import composechars, trace

def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """

    # Let's define our first FST
    f1 = FST('soundex-generate')

    # Indicate that '1' is the initial state
    f1.add_state('start')
    f1.add_state('vowel')
    f1.add_state('set1')
    f1.add_state('set2')
    f1.add_state('set3')
    f1.add_state('set4')
    f1.add_state('set5')
    f1.add_state('set6')
    f1.initial_state = 'start'

    # Set all the final states
    f1.set_final('set1')
    f1.set_final('set2')
    f1.set_final('set3')
    f1.set_final('set4')
    f1.set_final('set5')
    f1.set_final('set6')
    f1.set_final('vowel')

    # Add the rest of the arcs
    for letter in string.ascii_letters:
        if letter in "aehiouwyAEHIOUWY":
            f1.add_arc('start', 'vowel', (letter), (letter))
            f1.add_arc('vowel', 'vowel', (letter), ())
            f1.add_arc('set1', 'vowel', (letter), ())
            f1.add_arc('set2', 'vowel', (letter), ())
            f1.add_arc('set3', 'vowel', (letter), ())
            f1.add_arc('set4', 'vowel', (letter), ())
            f1.add_arc('set5', 'vowel', (letter), ())
            f1.add_arc('set6', 'vowel', (letter), ())
        elif letter in "bfpvBFPV":
            f1.add_arc('start', 'set1', (letter), (letter))
            f1.add_arc('vowel', 'set1', (letter), ('1'))
            f1.add_arc('set1', 'set1', (letter), ())
            f1.add_arc('set2', 'set1', (letter), ('1'))
            f1.add_arc('set3', 'set1', (letter), ('1'))
            f1.add_arc('set4', 'set1', (letter), ('1'))
            f1.add_arc('set5', 'set1', (letter), ('1'))
            f1.add_arc('set6', 'set1', (letter), ('1'))
        elif letter in "cgjkqsxzCGJKQSXZ":
            f1.add_arc('start', 'set2', (letter), (letter))
            f1.add_arc('vowel', 'set2', (letter), ('2'))
            f1.add_arc('set2', 'set2', (letter), ())
            f1.add_arc('set1', 'set2', (letter), ('2'))
            f1.add_arc('set3', 'set2', (letter), ('2'))
            f1.add_arc('set4', 'set2', (letter), ('2'))
            f1.add_arc('set5', 'set2', (letter), ('2'))
            f1.add_arc('set6', 'set2', (letter), ('2'))
        elif letter in "dtDT":
            f1.add_arc('start', 'set3', (letter), (letter))
            f1.add_arc('vowel', 'set3', (letter), ('3'))
            f1.add_arc('set3', 'set3', (letter), ())
            f1.add_arc('set1', 'set3', (letter), ('3'))
            f1.add_arc('set2', 'set3', (letter), ('3'))
            f1.add_arc('set4', 'set3', (letter), ('3'))
            f1.add_arc('set5', 'set3', (letter), ('3'))
            f1.add_arc('set6', 'set3', (letter), ('3'))
        elif letter in "lL":
            f1.add_arc('start', 'set4', (letter), (letter))
            f1.add_arc('vowel', 'set4', (letter), ('4'))
            f1.add_arc('set4', 'set4', (letter), ())
            f1.add_arc('set1', 'set4', (letter), ('4'))
            f1.add_arc('set2', 'set4', (letter), ('4'))
            f1.add_arc('set3', 'set4', (letter), ('4'))
            f1.add_arc('set5', 'set4', (letter), ('4'))
            f1.add_arc('set6', 'set4', (letter), ('4'))
        elif letter in "mnMN":
            f1.add_arc('start', 'set5', (letter), (letter))
            f1.add_arc('vowel', 'set5', (letter), ('5'))
            f1.add_arc('set5', 'set5', (letter), ())
            f1.add_arc('set1', 'set5', (letter), ('5'))
            f1.add_arc('set2', 'set5', (letter), ('5'))
            f1.add_arc('set3', 'set5', (letter), ('5'))
            f1.add_arc('set4', 'set5', (letter), ('5'))
            f1.add_arc('set6', 'set5', (letter), ('5'))
        elif letter in "rR":
            f1.add_arc('start', 'set6', (letter), (letter))
            f1.add_arc('vowel', 'set6', (letter), ('6'))
            f1.add_arc('set6', 'set6', (letter), ())
            f1.add_arc('set1', 'set6', (letter), ('6'))
            f1.add_arc('set2', 'set6', (letter), ('6'))
            f1.add_arc('set3', 'set6', (letter), ('6'))
            f1.add_arc('set4', 'set6', (letter), ('6'))
            f1.add_arc('set5', 'set6', (letter), ('6'))
    return f1

    # The stub code above converts all letters except the first into '0'.
    # How can you change it to do the right conversion?

def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('1')
    f2.add_state('2')
    f2.add_state('3')
    f2.add_state('4')

    f2.initial_state = '1'
    f2.set_final('2')
    f2.set_final('3')
    f2.set_final('4')


    # Add the arcs
    for letter in string.letters:
        f2.add_arc('1', '1', (letter), (letter))

    for n in range(10):
        f2.add_arc('1', '2', (str(n)), (str(n)))
        f2.add_arc('2', '3', (str(n)), (str(n)))
        f2.add_arc('3', '4', (str(n)), (str(n)))
        f2.add_arc('4', '4', (str(n)), ())

    return f2

    # The above stub code doesn't do any truncating at all -- it passes letter and number input through
    # what changes would make it truncate digits to 3?

def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')

    f3.add_state('1')
    f3.add_state('1a')
    f3.add_state('1b')
    f3.add_state('2')
    
    f3.initial_state = '1'
    f3.set_final('2')

    f3.add_arc('1', '1a', (), ('0'))
    f3.add_arc('1a', '1b', (), ('0'))
    f3.add_arc('1b', '2', (), ('0'))

    for letter in string.letters:
        f3.add_arc('1', '1', (letter), (letter))
    for number in xrange(10):
        f3.add_arc('1', '1a', (str(number)), (str(number)))
        f3.add_arc('1a', '1b', (str(number)), (str(number)))
        f3.add_arc('1b', '2', (str(number)), (str(number)))
        f3.add_arc('2', '2', (str(number)), ())

    return f3

    # The above code adds zeroes but doesn't have any padding logic. Add some!

if __name__ == '__main__':
    user_input = raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()
    # print trace(f1, "Jurafsky")
    # print trace(f2, "J612")
    # print trace(f3, "J612")
    if user_input:
        print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))
