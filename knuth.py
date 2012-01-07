import itertools
import random
import math

class Knuth(object):

    def __init__(self, colours, code_len, secret):
        self.colours = colours
        self.code_len = code_len
        self.secret = secret

        pos = itertools.product(self.colours, repeat=self.code_len)
        pos = itertools.imap(''.join, pos)
        pos, all_pos = itertools.tee(pos, 2)
        self.pos = set(pos)
        self.all_pos = set(all_pos)
        #print len(list(self.pos))

    def cull_pos(self, guess, result):
        from mastermind import check_guess
        [self.pos.remove(code) for code in set(self.pos)
            if check_guess(guess, code) != result]

    def guesser(self):
        from mastermind import check_guess
        # algorthm suggests an initial guess of aabb, ie indexes of 0011
        initial_guess_indexs = (0,)*int(math.floor(self.code_len/2.)) \
                             + (1,)*int(math.ceil(self.code_len/2.))
        guess = ''.join(self.colours[i] for i in initial_guess_indexs)
        result = yield guess
        for _ in range(11):
            self.cull_pos(guess, result)
            #print len(list(self.pos))
            #if len(self.pos) < 20:
            #    print [(p, check_guess(p, self.secret)) for p in self.pos]
            
            # even with random choice of available posibilities, we usually  win in 4 to 6 moves
            guess = random.choice(list(self.pos))
            result = yield guess
