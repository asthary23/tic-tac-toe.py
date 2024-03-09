#HASH FUNCTION:
def memoize(f): 
    # Decorator function can be implemented as pleased
    # This inner function has access to memory and 'f'
    def inner(num): 
        if num not in memory:          
            memory[num] = f.board(num) 
        return memory[num] 
    return inner

def fact(n):
    # n * (n-1) ... 1
    return 1 if n <= 1 else n * fact(n-1)

def c(n, k):
    # n choose k
    return fact(n)//fact(k)//fact(n-k)

# s = total number of available slots
# o = total number of Os
# x = total number of Xs
def rearrange(x, o, s):
    # Number of rearrangements for Xs and Os given S slots -- see alternative() for an alternative equivalent expression
    if (x < 0) or (o < 0):
        return 0
    return fact(s)//fact(o)//fact(x)//fact(s - x - o)

def alternative(x, o, s):
    # Another mathematically accurate formula for computing rearrangements
    return c(s, x + o) * c(x + o, x)

def xs_and_os(p):
    # Tuple of the number of Xs and Os, given P pieces
    return (math.ceil(p/2), math.floor(p/2))

def positions(s):
    #Total number of tictactoe positions, given S slots
    all_pos = [xs_and_os(p) for p in range(s + 1)]
    rearrangements = [rearrange(cross, naught, s) for cross, naught in all_pos]
    return sum(rearrangements)

def hashing(string, x, o, s):
    # Combinatorially perfect hash function 
    previous = [xs_and_os(p) for p in range(s-1)]
    biases = [rearrange(cross, naught, s) for cross, naught in previous]
    def condense(string, x, o, s):
        if string:
            first = string[0]
            if first == "-":
                return condense(string[1:], x, o, s-1)
            elif first == "o":
                offset = (0 if len(string) == 1 else (rearrange(x, o, s) - rearrange(x, o-1, s-1) - rearrange(x-1, o, s-1)))
                return offset + condense(string[1:], x, o-1, s-1)
            elif first == "x":
                offset = (0 if len(string) == 1 else (rearrange(x, o, s) - rearrange(x-1, o, s-1)))
                return offset + condense(string[1:], x-1, o, s-1)
        return 0
    return sum(biases) + condense(string, x, o, s) 

"""
Separate implementation of unhashing function (can be made compatible with current hashing format):
    def rearranger_unhash_o_only(s,o,i,bC,oC):
        "Return the unhashed board with S slots, O os, at index I with characters for blank-o bC oC"
        if s == 0:
            return ""
        elif s == o:
            return oC * s ## all os
        elif i < rearranger_o_only(s-1, o): ## no o cause #pos with o first not > i
            return bC + rearranger_unhash_o_only(s-1, o, i, bC, oC)
        else:
            return oC + rearranger_unhash_o_only(s-1, o-1, i-rearranger_o_only(s-1, o), bC, oC)

    def rearranger_unhash(s,o,x,i,bC,oC,xC):
        "Return the unhashed board with S slots, O os, X xs at index I with characters for blank-o-x bC oC xC"
        if s == 0:
            return ""
        elif (o == 0) and (x == 0): ## all blanks
            return bC * s           ## ...so return all blanks
        elif s == o:                ## all Os
            return oC * s           ## ...so return all Os
        elif s == x:                ## all Xs
            return xC * s           ## ...so return all Xs
        elif s == (o + x):          ## no blanks
            return rearranger_unhash_o_only(s,x,i,oC,xC) ## so treat like ox only
        elif o == 0:                ## no Os
            return rearranger_unhash_o_only(s,x,i,bC,xC) ## so treat like -x only
        elif x == 0:                ## no Xs
            return rearranger_unhash_o_only(s,o,i,bC,oC) ## so treat like -o only
        elif i < rearranger(s-1,o,x): ## index hasn't run out of blanks
            return bC + rearranger_unhash(s-1,o,x,i,bC,oC,xC) ## so put a blank there
        elif i < rearranger(s-1,o,x) + rearranger(s-1,o-1,x): ## index hasn't run out of os
            return oC + rearranger_unhash(s-1,o-1,x,i-rearranger(s-1,o,x),bC,oC,xC) ## so put an o there
        else: ## index is bigger than -s and os
            return xC + rearranger_unhash(s-1,o,x-1,i-rearranger(s-1,o,x)-rearranger(s-1,o-1,x),bC,oC,xC)
"""