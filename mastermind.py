import random
import sys
from collections import namedtuple

from knuth import Knuth

CODE_LEN = 6
COLOURS = ['R', 'B', 'G', 'Y', 'O', 'P']
secret_pattern = None

class Result(object):
    def __init__(self, exact, elsewhere):
        self.exact = exact
        self.elsewhere = elsewhere        

    def __str__(self):
        return '%s %s' % ('B' * self.exact, 'W' * self.elsewhere)


def main():
    secret_pattern = set_secret_pattern()
    guesses_left = 10
    ai = Knuth(COLOURS, CODE_LEN).guesser()
    result = None
    i = 0
    while guesses_left > 0:
        i += 1
        #guess = get_guess()
        guess = ai.send(result)
        print '%2.d)' % i,
        print guess,
        results = check_guess(guess, secret_pattern)
        print results
        if results.exact == CODE_LEN:
            print "YOU WON!"
            return
        guesses_left -= 1
    print "YOU LOSE"


def get_guess():
    while True:
        print 'guess a combination, eg RGBY'
        try:
            s = raw_input().upper()
        except KeyboardInterrupt:
            print 'Too difficult???'
            print 'BYE!'
            sys.exit()
        else:
            if not len(s) == CODE_LEN or set(s) in set(COLOURS):
                print s, 'is not a valid choice, guess again'
            else:
                return s

def set_secret_pattern():
    pattern = [random.choice(COLOURS) for _ in range(len(COLOURS))]
    print "secret pattern is %s (ssh!)" %  pattern
    return pattern


def check_guess(guess, solution):
    guess = guess.upper()
    exact = 0
    wrong_pos = 0
    exacts = [tup[0]==tup[1] for tup in zip(guess, solution)]
    remaining_solution = list(s for (s, found) in zip(solution, exacts) if not found)
    remaining_guess = list(guess)
    for i in range(len(solution)):
        if guess[i] == solution[i]:
            exact += 1
            del remaining_guess[i]
            del remaining_solution[i]

    remaining_solution2 = list(remaining_solution)
    remaining_guess2 = list(remaining_guess)
    for i in range(len(remaining_solution)):
        if remaining_guess[i] in remaining_solution2:
            wrong_pos += 1
            del remaining_guess2[i]
            remaining_solution2.remove(remaining_guess[i])

    return Result(exact=exact, elsewhere=wrong_pos)


def check_guess(s1, s2):
    """
    >>> check_guess('RGBY', 'RRRR')
    Result(exact=1, elsewhere=0)
    >>> check_guess('RGBY', 'GRRR')
    Result(exact=0, elsewhere=2)
    >>> check_guess('RYYY', 'RYRY')
    Result(exact=3, elsewhere=0)
    >>> check_guess('BGGG', 'GGGQ')
    Result(exact=3, elsewhere=0)
    """
    matches = 0
    colcount = { } # col -> [n1, n2]
    for k1, k2 in zip(s1, s2):
        if k1 == k2:
            matches += 1
        else:
            for k in [k1, k2]:
                if k not in colcount:
                    colcount[k] = [0,0]
            colcount[k1][0] += 1
            colcount[k2][1] += 1
            
    return Result(matches, sum([ min(n1, n2)  for n1, n2 in colcount.values() ]))



if __name__ == '__main__':
    if 'test' in sys.argv[1:]:
        print 'test'
        import doctest
        doctest.testmod(verbose=True)
    else:
        main()



