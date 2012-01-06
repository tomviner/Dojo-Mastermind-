import itertools

class Knuth(object):

    def __init__(self, colours, code_len):
        self.colours = colours
        self.code_len = code_len

        self.pos = itertools.product(self.colours, repeat=self.code_len)

    def cull_pos(self, guess, res):
        pass
        

    def guesser(self):   
        guess = ''.join(self.colours[i] for i in (0, 0, 1, 1))
        result = yield guess
        for _ in range(11):
            self.cull_pos(guess, result)
            result = yield 'bbbb'.upper()
